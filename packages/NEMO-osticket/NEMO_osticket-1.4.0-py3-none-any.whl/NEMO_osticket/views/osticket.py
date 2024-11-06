from datetime import datetime
from logging import getLogger
from typing import Dict, List

import requests
from NEMO.forms import nice_errors
from NEMO.models import Reservation, Tool, User
from NEMO.utilities import render_combine_responses
from NEMO.views.tool_control import tool_status as original_tool_status
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.template import Context, Template
from django.utils import timezone
from django.views.decorators.http import require_GET, require_POST

from NEMO_osticket.customizations import OsTicketCustomization
from NEMO_osticket.exceptions import OsTicketException
from NEMO_osticket.forms import OsTicketForm
from NEMO_osticket.models import (
    OstFormEntry,
    OstFormEntryValues,
    OstHelpTopic,
    OstListItems,
    OstObjectType,
    OstThread,
    OstTicket,
)

osticket_logger = getLogger(__name__)


TICKETS_PATH = "/api/tickets.json"


@login_required
@require_GET
def tool_status(request, tool_id):
    original_response = original_tool_status(request, tool_id)
    no_osticket = not get_os_ticket_service().get("available", False) and not settings.DATABASES.get("osticket", False)
    if no_osticket or original_response.status_code != 200:
        return original_response

    dictionary = {
        "tool_id": tool_id,
        "replace_problems_tab": OsTicketCustomization.get_bool("osticket_tool_control_replace_problem_tab"),
        "tab_name": OsTicketCustomization.get("osticket_tool_control_tab_name"),
    }

    return render_combine_responses(request, original_response, "NEMO_osticket/osticket_tab.html", dictionary)


@login_required
@require_GET
def tool_status_tickets(request, tool_id):
    create_ticket_include_reservations = OsTicketCustomization.get_bool("osticket_create_ticket_include_reservations")
    past_week_reservations = Reservation.objects.none()
    if create_ticket_include_reservations:
        end = timezone.now()
        start = end - timezone.timedelta(days=7)
        past_week_reservations = Reservation.objects.filter(
            tool_id=tool_id, missed=False, cancelled=False, shortened=False
        )
        past_week_reservations = past_week_reservations.filter(start__gte=start, end__lte=end, end__isnull=False)
        past_week_reservations = past_week_reservations.order_by("-start")
        past_week_reservations = past_week_reservations.prefetch_related("user")

    dictionary = {
        "topic_label": OsTicketCustomization.get("osticket_create_ticket_help_topic_label"),
        "issue_summary_label": OsTicketCustomization.get("osticket_create_ticket_issue_summary_label"),
        "message_label": OsTicketCustomization.get("osticket_create_ticket_message_label"),
        "reservations": past_week_reservations,
        "osticket_api_available": get_os_ticket_service().get("available", False),
        "ostickets": get_ostickets_for_tool(get_object_or_404(Tool, pk=tool_id)),
        "list_items": {str(item.id): item.value for item in OstListItems.objects.all()},
        "form": OsTicketForm(),
        "tool_id": tool_id,
        "tool_matching_field_id": OsTicketCustomization.get_int("osticket_tool_matching_field_id"),
    }
    return render(request, "NEMO_osticket/osticket_tab_content.html", dictionary)


@login_required
@require_POST
def create_ticket(request, tool_id):
    tool = get_object_or_404(Tool, pk=tool_id)

    form = OsTicketForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(nice_errors(form).as_ul())

    try:
        create_os_ticket(request.user, tool, form.cleaned_data)
        messages.success(request, "Your ticket was successfully created")
    except OsTicketException as e:
        osticket_logger.exception(e)
        messages.error(request, f"There was an error creating the ticket: {str(e)}")

    return redirect("tool_control")


def create_os_ticket(user: User, tool: Tool, data: Dict):
    os_ticket_service = get_os_ticket_service()
    if os_ticket_service.get("available", False):
        try:
            full_tickets_url = os_ticket_service["url"] + TICKETS_PATH
            keyword_arguments = os_ticket_service.get("keyword_arguments", {})
            json_data = data
            # reservation cannot be serialized
            reservation = json_data.get("reservation")
            if "reservation" in json_data:
                del json_data["reservation"]
            # update with matching form field if applicable
            form_field = OsTicketCustomization.get_osticket_tool_matching_field()
            if form_field:
                if form_field.is_list_type():
                    json_data.update({form_field.name: OsTicketCustomization.get_osticket_tool_matching_value(tool).id})
                else:
                    json_data.update({form_field.name: OsTicketCustomization.get_tool_matching_nemo_property(tool)})
            json_data.update({"email": user.email, "name": user.username})
            topic = OstHelpTopic.objects.filter(topic_id=json_data.get("topicId")).first()
            topic = topic.topic if topic else None
            json_data["subject"] = format_ticket_subject(json_data["subject"], topic, tool, user, reservation)
            json_data["message"] = format_ticket_message(json_data["message"], topic, tool, user, reservation)
            response = requests.post(full_tickets_url, json=json_data, **keyword_arguments)
            response.raise_for_status()
        except Exception as e:
            raise OsTicketException(e)
    else:
        raise OsTicketException("OsTicket is not available")


def get_ostickets_for_tool(tool: Tool, only_open=True, start: datetime = None, end: datetime = None) -> List[OstTicket]:
    if settings.DATABASES.get("osticket", False):
        tickets = OstTicket.objects.filter()
        if start:
            tickets = tickets.filter(created__gte=start)
        if end:
            tickets = tickets.filter(created__lte=end)
        if only_open:
            tickets = tickets.filter(status__state="open")
        list_item = OsTicketCustomization.get_osticket_tool_matching_value(tool)
        form_field = OsTicketCustomization.get_osticket_tool_matching_field()
        form_entry_values = OstFormEntryValues.objects.filter(
            field=form_field,
            entry__object_type=OstObjectType.TICKET,
            entry__object_id__in=tickets.values_list("ticket_id", flat=True),
        ).prefetch_related("entry")
        valid_ticket_ids = []
        if list_item:
            # we need to filter manually since the value is a json dict and contains the list item id
            for form_entry_value in form_entry_values:
                try:
                    if str(list_item.id) == form_entry_value.get_list_item_id():
                        valid_ticket_ids.append(form_entry_value.entry.object_id)
                except Exception as e:
                    osticket_logger.debug(e)
        else:
            # just get corresponding tickets with value
            valid_ticket_ids = [
                value.entry.object_id
                for value in form_entry_values.filter(value=OsTicketCustomization.get_tool_matching_nemo_property(tool))
            ]
        return get_preloaded_os_tickets(valid_ticket_ids)
    return []


def get_preloaded_os_tickets(ticket_ids: List[int]) -> List[OstTicket]:
    tickets = []
    threads = list(
        OstThread.objects.filter(object_id__in=ticket_ids, object_type=OstObjectType.TICKET).prefetch_related(
            "ostthreadentry_set"
        )
    )
    form_entries = list(
        OstFormEntry.objects.filter(object_id__in=ticket_ids, object_type=OstObjectType.TICKET).prefetch_related(
            "ostformentryvalues_set__field"
        )
    )
    for ticket in OstTicket.objects.filter(ticket_id__in=ticket_ids).order_by("-created"):
        ticket.ostthread_set = set([thread for thread in threads if thread.object_id == ticket.ticket_id])
        ticket.ostformentry_set = set(
            [form_entry for form_entry in form_entries if form_entry.object_id == ticket.ticket_id]
        )
        tickets.append(ticket)
    return tickets


def format_ticket_subject(subject: str, topic, tool: Tool, user: User, reservation: Reservation = None) -> str:
    return Template(OsTicketCustomization.get("osticket_create_ticket_subject_template")).render(
        Context({"subject": subject, "topic": topic, "tool": tool, "user": user, "reservation": reservation})
    )


def format_ticket_message(message: str, topic, tool: Tool, user: User, reservation: Reservation = None) -> str:
    return Template(OsTicketCustomization.get("osticket_create_ticket_message_template")).render(
        Context({"message": message, "topic": topic, "tool": tool, "user": user, "reservation": reservation})
    )


def get_os_ticket_service():
    return getattr(settings, "OSTICKET_SERVICE", {})


# TODO: add a hook to kiosk as well
# TODO: add a hook to get osticket when searching for comments and tasks
