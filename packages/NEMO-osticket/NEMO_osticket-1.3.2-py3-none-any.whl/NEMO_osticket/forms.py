import json

from django import forms

from NEMO_osticket.models import get_osticket_form_fields


class OsTicketForm(forms.Form):
    subject = forms.CharField(max_length=255)
    message = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for ostField in get_osticket_form_fields():
            required = ostField.flags not in [13057, 12289, 769]
            max_length = None
            if ostField.configuration:
                config_json = json.loads(ostField.configuration)
                max_length = config_json.get("length", None) or None
            if ostField.type == "text":
                self.fields[ostField.name] = forms.CharField(max_length=max_length)
                self.fields[ostField.name].label = ostField.label
                self.fields[ostField.name].required = required
            elif ostField.type == "memo":
                self.fields[ostField.name] = forms.CharField(max_length=max_length, widget=forms.Textarea())
                self.fields[ostField.name].label = ostField.label
                self.fields[ostField.name].required = required
            elif ostField.is_list_type():
                choices = [(item.id, item.value) for item in ostField.get_list_options()]
                self.fields[ostField.name] = forms.ChoiceField(choices=choices)
                self.fields[ostField.name].label = ostField.label
                self.fields[ostField.name].required = required
