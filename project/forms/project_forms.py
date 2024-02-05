from django import forms
from ..models import (
    QuestionChoice,
    Question,
    Project,
    Answer,
    QuestionChoiceImpact,
    ProjectRequirementFollowUp,
    ProjectRequirement,
    RequirementStatus,
)


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name", "description", "status"]

    def __init__(self, *args, **kwargs):
        instance = kwargs.get("instance")
        if instance:
            initial = kwargs.get("initial", {})
            initial["name"] = instance.name
            initial["description"] = instance.description
            initial["status"] = instance.status
            kwargs["initial"] = initial
        super().__init__(*args, **kwargs)

        for question in Question.objects.all():
            choices = QuestionChoice.objects.filter(question=question)

            choices_list = [(choice.id, choice.name) for choice in choices]
            answer = Answer.objects.filter(project=instance, question=question).last()

            initial = None
            if answer:
                initial = answer.choice.id

            self.fields[f"question_{question.id}"] = forms.ChoiceField(
                label=question.description,
                help_text=question.details,
                choices=choices_list,
                widget=forms.RadioSelect,
                initial=initial,
            )

    def save(self, project_id=None):
        if project_id:  # Check if the project instance already exists
            tags = (self.get_tags(),)
            existing_project = Project.objects.get(pk=project_id)
            existing_project.name = self.cleaned_data["name"]
            existing_project.description = self.cleaned_data["description"]
            existing_project.status = self.cleaned_data["status"]
            existing_project.confidentiality = self.calculate_max_impact(
                "impact_confidentiality"
            )
            existing_project.integrity = self.calculate_max_impact("impact_integrity")
            existing_project.availability = self.calculate_max_impact(
                "impact_availability"
            )
            for name, value in self.cleaned_data.items():
                if name.startswith("question_"):
                    name_parts = name.split("_")
                    # print(name_parts)
                    if len(name_parts) >= 2:
                        question_id = str(name_parts[1])
                        question = Question.objects.get(id=question_id)
                        choice = QuestionChoice.objects.get(id=value)                        
                        project = Project.objects.get(id=existing_project.id)
                        answer, created = Answer.objects.update_or_create(
                            question=question,
                            project=project,
                            defaults={"choice":choice},
                        )

            existing_project.save()
            existing_project.tags.set(*tags)
            self.edit_project_requirement_followups(existing_project.id)
            existing_project.save()

            # existing_project.calculate_completion()
            return existing_project
        else:  # Create a new project instance
            tags = (self.get_tags(),)
            project = Project(
                name=self.cleaned_data["name"],
                description=self.cleaned_data["description"],
                status=self.cleaned_data["status"],
                confidentiality=self.calculate_max_impact("impact_confidentiality"),
                integrity=self.calculate_max_impact("impact_integrity"),
                availability=self.calculate_max_impact("impact_availability"),
            )

        project.save()
        project.tags.set(*tags)
        self.create_project_requirement_followups(project)
        project.save()

        for name, value in self.cleaned_data.items():
            if name.startswith("question_"):
                name_parts = name.split("_")
                if len(name_parts) >= 2:
                    question_id = str(name_parts[1])
                    question = Question.objects.get(id=question_id)
                    choice = QuestionChoice.objects.get(id=value)
                    project = Project.objects.get(id=project.id)
                    answer = Answer.objects.create(
                        question=question, choice=choice, project=project
                    )

        return project

    def calculate_max_impact(self, impact_field):
        max_impact = 0

        for name, value in self.cleaned_data.items():
            if name.startswith("question_"):
                question_id = str(name.split("_")[1])
                choice = QuestionChoice.objects.get(id=value)
                try:
                    impact = QuestionChoiceImpact.objects.get(
                        question_id=question_id, choice__name=choice
                    )
                    impact_value = getattr(impact, impact_field, 0)
                    # print(impact_field, question_id, impact_value)
                    if impact_value > max_impact:
                        max_impact = impact_value
                except QuestionChoiceImpact.DoesNotExist:
                    continue
        # print(max_impact)
        return max_impact

    def get_tags(self):
        tags = set()
        max_impact = 0
        for name, value in self.cleaned_data.items():
            if name.startswith("question_"):
                question_id = str(name.split("_")[1])
                choice = QuestionChoice.objects.get(id=value)
                try:
                    impact = QuestionChoiceImpact.objects.get(
                        question_id=question_id, choice__name=choice
                    )

                    impact_value = (
                        getattr(impact, "tags").values_list("id", flat=True).distinct()
                    )

                    tags.update(filter(None, impact_value))

                except QuestionChoiceImpact.DoesNotExist:
                    continue
        return tags

    def create_project_requirement_followups(self, project):
        requirements = ProjectRequirement.objects.all()
        status_list = RequirementStatus.objects.filter(value=0)

        for requirement in requirements:
            status = status_list.first()  # Get the first status object
            if requirement.tags.filter(
                name__in=project.tags.values_list("name", flat=True)
            ).exists() and (
                project.confidentiality >= requirement.applicability_confidentiality
                and project.integrity >= requirement.applicability_integrity
                and project.availability >= requirement.applicability_availability
            ):
                followup = ProjectRequirementFollowUp.objects.create(
                    project=project, requirement=requirement, status=status
                )
            elif (
                project.confidentiality >= requirement.applicability_confidentiality
                and project.integrity >= requirement.applicability_integrity
                and project.availability >= requirement.applicability_availability
            ) and not (requirement.tags.exists()):
                followup = ProjectRequirementFollowUp.objects.create(
                    project=project, requirement=requirement, status=status
                )

    def edit_project_requirement_followups(self, project_id):
        project = Project.objects.get(pk=project_id)
        requirements = ProjectRequirement.objects.all()
        status_list = RequirementStatus.objects.all()

        for requirement in requirements:
            status = status_list.first()  # Get the first status object
            if requirement.tags.filter(
                name__in=project.tags.values_list("name", flat=True)
            ).exists() and (
                project.confidentiality >= requirement.applicability_confidentiality
                and project.integrity >= requirement.applicability_integrity
                and project.availability >= requirement.applicability_availability
            ):
                followup_exists = ProjectRequirementFollowUp.objects.filter(
                    project=project, requirement=requirement
                ).exists()
                if not followup_exists:
                    followup = ProjectRequirementFollowUp.objects.create(
                        project=project, requirement=requirement, status=status
                    )
            elif (
                project.confidentiality >= requirement.applicability_confidentiality
                and project.integrity >= requirement.applicability_integrity
                and project.availability >= requirement.applicability_availability
            ) and not (requirement.tags.exists()):
                followup_exists = ProjectRequirementFollowUp.objects.filter(
                    project=project, requirement=requirement
                ).exists()
                if not followup_exists:
                    followup = ProjectRequirementFollowUp.objects.create(
                        project=project, requirement=requirement, status=status
                    )
            else:
                followup_exists = ProjectRequirementFollowUp.objects.filter(
                    project=project, requirement=requirement
                )
                if followup_exists.exists():
                    followup_exists.delete()
