from datetime import datetime
from logging import getLogger
from typing import Dict, Optional

import requests
from NEMO.models import Tool, User
from NEMO.typing import QuerySetType
from NEMO.utilities import render_combine_responses
from NEMO.views.tool_control import tool_status as original_tool_status
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_GET, require_POST

from NEMO_osticket.customizations import OsTicketCustomization
from NEMO_osticket.exceptions import OsTicketException
from NEMO_osticket.forms import OsTicketForm
from NEMO_osticket.models import OstFormEntryValues, OstObjectType, OstTicket

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
        "osticket_api_available": get_os_ticket_service().get("available", False),
        "ostickets": get_ostickets_for_tool(get_object_or_404(Tool, pk=tool_id)),
        "form": OsTicketForm(),
        "tool_id": tool_id,
        "replace_problems_tab": OsTicketCustomization.get_bool("osticket_tool_control_replace_problem_tab"),
        "tab_name": OsTicketCustomization.get("osticket_tool_control_tab_name"),
    }

    return render_combine_responses(request, original_response, "NEMO_osticket/osticket_tab.html", dictionary)


@login_required
@require_POST
def create_ticket(request, tool_id):
    tool = get_object_or_404(Tool, pk=tool_id)

    form = OsTicketForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    try:
        create_os_ticket(request.user, tool, form.cleaned_data)
        messages.success(request, "Your ticket was successfully created")
    except OsTicketException as e:
        osticket_logger.error(e)
        messages.error(request, f"There was an error creating the ticket: {str(e)}")

    return redirect("tool_control")


def create_os_ticket(user: User, tool: Tool, data: Dict):
    os_ticket_service = get_os_ticket_service()
    if os_ticket_service.get("available", False):
        try:
            full_tickets_url = os_ticket_service["url"] + TICKETS_PATH
            keyword_arguments = os_ticket_service.get("keyword_arguments", {})
            json_data = data
            # update with matching form field if applicable
            form_field = OsTicketCustomization.get_osticket_tool_matching_field()
            if form_field:
                if form_field.is_list_type():
                    json_data.update({form_field.name: OsTicketCustomization.get_osticket_tool_matching_value(tool).id})
                else:
                    json_data.update({form_field.name: OsTicketCustomization.get_tool_matching_nemo_property(tool)})
            json_data.update({"email": user.email, "name": user.username})
            response = requests.post(full_tickets_url, json=json_data, **keyword_arguments)
            response.raise_for_status()
        except Exception as e:
            raise OsTicketException(e)
    else:
        raise OsTicketException("OsTicket is not available")


def get_ostickets_for_tool(
    tool: Tool, only_open=True, start: datetime = None, end: datetime = None
) -> Optional[QuerySetType[OstTicket]]:
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
        )
        valid_ticket_ids = []
        if list_item:
            # we need to filter manually since the value is a json dict and contains the list item id
            for form_entry_value in form_entry_values:
                try:
                    entry_list_item = form_entry_value.get_list_item()
                    if list_item == entry_list_item:
                        valid_ticket_ids.append(form_entry_value.entry.object_id)
                except Exception as e:
                    osticket_logger.debug(e)
        else:
            # just get corresponding tickets with value
            valid_ticket_ids = [
                value.entry.object_id
                for value in form_entry_values.filter(value=OsTicketCustomization.get_tool_matching_nemo_property(tool))
            ]
        return OstTicket.objects.filter(ticket_id__in=valid_ticket_ids)
    return None


def get_os_ticket_service():
    return getattr(settings, "OSTICKET_SERVICE", {})


# TODO: add a hook to kiosk as well
# TODO: add ticket subject template
# TODO: add ticket message template
# TODO: add a hook to get osticket when searching for comments and tasks
