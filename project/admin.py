from django import forms
from django.contrib import admin
from .models import (
    QuestionChoice,
    Question,
    Project,
    Answer,
    QuestionChoiceImpact,
    QuestionTag,
    ProjectRequirement,
    ProjectRequirementFollowUp,
    RequirementStatus,
    QuestionTag,
    ProjectRequirementFollowUpComment,
)
from library.models import Directory, Document
from thirdparty.models import (
    ThirdParty,
    TP_Assessment,
    TP_Question,
    TP_AssessmentQuestion,
    TP_Score,
)


class AnswerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        question = kwargs.pop(
            "question"
        )  # Get the question instance passed to the form
        super().__init__(*args, **kwargs)
        self.fields["choice"].queryset = question.choices.all()

    class Meta:
        model = Answer
        fields = ["choice"]


class AnswerAdmin(admin.ModelAdmin):
    form = AnswerForm

class ProjectAdmin(admin.ModelAdmin):
    readonly_fields = ('date_created','date_updated')

class ProjectRequirementFollowUpAdmin(admin.ModelAdmin):
    readonly_fields = ('updated_date',)

# Register your models here.
admin.site.register(QuestionChoice)
admin.site.register(Question)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Answer)
admin.site.register(QuestionChoiceImpact)
admin.site.register(QuestionTag)
admin.site.register(ProjectRequirement)
admin.site.register(ProjectRequirementFollowUp, ProjectRequirementFollowUpAdmin)
admin.site.register(RequirementStatus)
admin.site.register(ProjectRequirementFollowUpComment)
admin.site.register(Directory)
admin.site.register(Document)

admin.site.register(ThirdParty)
admin.site.register(TP_Assessment)
admin.site.register(TP_Question)
admin.site.register(TP_AssessmentQuestion)
admin.site.register(TP_Score)