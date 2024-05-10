from django import forms

from med_alert_app.models import Report


class UploadFileForm(forms.Form):
    file = forms.FileField(required=False)


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['offenders_names', 'location', 'date_time_of_offense', 'offense_description', 'action_desired',
                  'resolved_action']
        widgets = {
            'date_time_of_offense': forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD HH:MM:SS'}),
        }

    def __init__(self, *args, **kwargs):
        super(ReportForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].required = True
