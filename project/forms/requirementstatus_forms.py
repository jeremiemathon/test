from django import forms
from ..models import RequirementStatus

class RequirementStatusForm(forms.ModelForm):
    class Meta:
        model = RequirementStatus
        fields = ['name', 'value']