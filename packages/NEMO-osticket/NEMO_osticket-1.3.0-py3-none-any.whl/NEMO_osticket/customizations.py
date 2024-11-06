import re
from logging import getLogger
from typing import Dict, Optional

from NEMO.decorators import customization
from NEMO.models import Tool
from NEMO.views.customization import CustomizationBase
from django.core.exceptions import ValidationError
from django.template import Context, Template

from NEMO_osticket.models import OstFormField, OstListItems, get_osticket_form_fields

osticket_customization_logger = getLogger(__name__)


@customization(key="osticket", title="OsTicket")
class OsTicketCustomization(CustomizationBase):
    variables = {
        "osticket_tool_control_replace_problem_tab": "",
        "osticket_tool_control_tab_name": "Help desk",
        # "osticket_new_ticket_subject_template": "",
        # "osticket_new_ticket_message_template": "",
        "osticket_tool_matching_field_id": "",
        "osticket_tool_matching_nemo_property_template": "{{ tool.id }}",
        "osticket_tool_matching_property_extract_re": "",
    }

    def context(self) -> Dict:
        context_dict = super().context()
        context_dict["ticket_form_fields"] = get_osticket_form_fields(exclude_matching=False)
        return context_dict

    def validate(self, name, value):
        if name == "osticket_tool_matching_nemo_property_template" and value:
            try:
                Template(value).render(Context({"tool": Tool.objects.first()}))
            except Exception as e:
                raise ValidationError(str(e))

    @classmethod
    def get_osticket_tool_matching_field(cls) -> Optional[OstFormField]:
        return OstFormField.objects.filter(id=cls.get_int("osticket_tool_matching_field_id") or None).first()

    @classmethod
    def get_osticket_tool_matching_value(cls, tool: Tool) -> Optional[OstListItems]:
        field = cls.get_osticket_tool_matching_field()
        if field:
            if field.is_list_type():
                list_options = field.get_list_options()
                if list_options:
                    for item in list_options:
                        if cls.is_tool_match(tool, item.value):
                            return item
        return None

    @classmethod
    def get_tool_matching_nemo_property(cls, tool: Tool) -> str:
        return Template(cls.get("osticket_tool_matching_nemo_property_template")).render(Context({"tool": tool}))

    @classmethod
    def is_tool_match(cls, tool: Tool, osticket_field_value: str):
        try:
            nemo_property = cls.get_tool_matching_nemo_property(tool)
            osticket_property = None
            osticket_re_matching = cls.get("osticket_tool_matching_property_extract_re")
            if osticket_re_matching:
                match = re.match(rf"{osticket_re_matching}", osticket_field_value)
                if match:
                    osticket_property = match.group(1)
            if nemo_property and osticket_property:
                return nemo_property == osticket_property
        except Exception as e:
            osticket_customization_logger.error(e)
        return False
