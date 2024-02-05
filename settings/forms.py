from django import forms

from .models import SiteSettings
from django.core.files.base import ContentFile
from project.models import RequirementStatus


class RequirementStatusForm(forms.ModelForm):
    class Meta:
        model = RequirementStatus
        fields = ["name", "value"]


class SiteSettingsForm(forms.ModelForm):
    logo = forms.ImageField(required=False)

    class Meta:
        model = SiteSettings
        fields = [
            "logo",
            "searchable_table",
        ]

    def __init__(self, *args, **kwargs):
        super(SiteSettingsForm, self).__init__(*args, **kwargs)

    def clean_logo(self):
        file = self.cleaned_data.get("logo", False)
        if file:
            if file._size > 2 * 1024 * 1024:
                raise forms.ValidationError("Image file too large ( > 2mb )")
            return ContentFile(file.read())
        return None
