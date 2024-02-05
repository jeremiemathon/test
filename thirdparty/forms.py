from django import forms
from .models import (
    ThirdParty,
    TP_Assessment,
    TP_Question,
    TP_AssessmentQuestion,
)
from django.utils import timezone
from django.forms import formset_factory

class ThirdPartyForm(forms.ModelForm):
    class Meta:
        model = ThirdParty
        fields = ["name", "description", "contact_info"]



class TP_QuestionForm(forms.ModelForm):
    class Meta:
        model = TP_Question
        fields = "__all__"
        widgets = {
            'order': forms.HiddenInput(),
        }

class TP_AssessmentQuestionForm(forms.ModelForm):
    class Meta:
        model = TP_AssessmentQuestion
        fields = "__all__"

TP_AssessmentQuestionFormSet = formset_factory(TP_AssessmentQuestionForm, extra=1)

class TP_AssessmentForm(forms.ModelForm):
    class Meta:
        model = TP_Assessment
        fields = "__all__"
        widgets = {
            'date': forms.TextInput(attrs={'readonly': 'readonly'})
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.assessment_question_formset = TP_AssessmentQuestionFormSet(*args, **kwargs)
        self.initial['date'] = timezone.now()  # Set the initial value of the date field to current datetime
    
    def is_valid(self):
        return super().is_valid() and self.assessment_question_formset.is_valid()