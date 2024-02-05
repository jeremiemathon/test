from django import forms
from ..models import (
    QuestionTag,
)


class QuestionTagForm(forms.ModelForm):
    class Meta:
        model = QuestionTag
        fields = "__all__"