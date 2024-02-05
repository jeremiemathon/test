from django import forms
from ..models import (
    QuestionChoiceImpact,
)


class QuestionChoiceImpactForm(forms.ModelForm):
    class Meta:
        model = QuestionChoiceImpact
        fields = [
            "question",
            "choice",
            "impact_confidentiality",
            "impact_integrity",
            "impact_availability",
            "tags",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
