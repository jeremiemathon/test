from django import forms
from ..models import (
    ProjectRequirement,
)
from library.models import (
    Document,
)


class ProjectRequirementForm(forms.ModelForm):

    class Meta:
        model = ProjectRequirement
        fields = "__all__"
        widgets = {
            "reference": forms.TextInput,
            "tags": forms.CheckboxSelectMultiple,
        }
    

class RequirementDocumentForm(forms.ModelForm):

    documents = forms.ModelMultipleChoiceField(
        queryset=Document.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = ProjectRequirement
        fields = ['documents']