from django import forms
from ..models import ProjectRequirementFollowUp


class ProjectRequirementFollowUpForm(forms.ModelForm):
    class Meta:
        model = ProjectRequirementFollowUp
        fields = ["project", "requirement", "status"]
