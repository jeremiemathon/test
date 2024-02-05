from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import uuid

from library.models import Document


class QuestionChoice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class QuestionTag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class Question(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.IntegerField(default=0, db_index=True)
    description = models.TextField()
    details = models.TextField(blank=True, null=True)
    choices = models.ManyToManyField("QuestionChoice", through="QuestionChoiceImpact")

    def __str__(self) -> str:
        return f"{self.description}"


class QuestionChoiceImpact(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(QuestionChoice, on_delete=models.CASCADE, null=True)
    impact_confidentiality = models.IntegerField(default=1)
    impact_integrity = models.IntegerField(default=1)
    impact_availability = models.IntegerField(default=1)
    tags = models.ManyToManyField(QuestionTag, blank=True)

    def __str__(self) -> str:
        return f"{self.question} - {self.choice}-({self.impact_confidentiality},{self.impact_integrity},{self.impact_availability})"


class Answer(models.Model):
    project = models.ForeignKey(
        "Project", on_delete=models.CASCADE, related_name="answers"
    )
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(QuestionChoice, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.project} - {self.question} - {self.choice}"


class Project(models.Model):
    CONFIDENTIALITY_CHOICES = (
        (1, "Low"),
        (2, "Medium"),
        (3, "High"),
        (4, "Very High"),
    )
    AVAILABILITY_CHOICES = (
        (1, "Low"),
        (2, "Medium"),
        (3, "High"),
        (4, "Very High"),
    )
    INTEGRITY_CHOICES = (
        (1, "Low"),
        (2, "Medium"),
        (3, "High"),
        (4, "Very High"),
    )
    STATUS_CHOICES = (
        ("Not Started", "Not Started"),
        ("Ongoing", "Ongoing"),
        ("Ended", "Ended"),
    )
    date_updated = models.DateTimeField(auto_now=True, verbose_name="Date Updated")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Date Created")
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="Not Started"
    )

    confidentiality = models.IntegerField(choices=CONFIDENTIALITY_CHOICES, default=1)
    availability = models.IntegerField(choices=AVAILABILITY_CHOICES, default=1)
    integrity = models.IntegerField(choices=INTEGRITY_CHOICES, default=1)

    tags = models.ManyToManyField(QuestionTag, blank=True)
    progress = models.SmallIntegerField(default=0)
    signed_off = models.BooleanField(default=False)  # Sign-off status

    def __str__(self) -> str:
        return self.name


class ProjectRequirement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.IntegerField(default=0)
    reference = models.TextField(max_length=20, default="")
    description = models.TextField()
    comments = models.TextField(blank=True)
    applicability_confidentiality = models.PositiveIntegerField(default=1)
    applicability_integrity = models.PositiveIntegerField(default=1)
    applicability_availability = models.PositiveIntegerField(default=1)
    tags = models.ManyToManyField(QuestionTag, blank=True)
    documents = models.ManyToManyField(Document, blank=True)

    def is_applicable(self, project):
        """
        Check if the requirement is applicable based on project levels and tags.
        ✅ Docstring added for clarity.
        """
        is_applicable = True
        if self.applicability_confidentiality > 1:
            is_applicable = (
                is_applicable
                and project.confidentiality >= self.applicability_confidentiality
            )
        if self.applicability_integrity > 1:
            is_applicable = (
                is_applicable and project.integrity >= self.applicability_integrity
            )
        if self.applicability_availability > 1:
            is_applicable = (
                is_applicable
                and project.availability >= self.applicability_availability
            )
        if self.tags.exists():
            # is_applicable = (
            #     is_applicable
            #     and project.tags.filter(
            #         pk__in=self.tags.all().values_list("pk", flat=True)
            #     ).exists()
            # )
            project_tags = project.tags.filter(pk__in=self.tags.all().values_list("pk", flat=True))
            is_applicable = is_applicable and project_tags.exists()
        return is_applicable

    def __str__(self):
        return f"{self.reference} - {self.description}"


class Tag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    # color = models.CharField(max_length=10, default="primary")

    def __str__(self) -> str:
        return self.name


class RequirementStatus(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    value = models.FloatField(default=1)

    def __str__(self) -> str:
        return f"{self.name} - {self.value}"


class ProjectRequirementFollowUp(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    updated_date = models.DateTimeField(auto_now=True, verbose_name="Date Updated")
    project = models.ForeignKey("Project", on_delete=models.CASCADE)
    requirement = models.ForeignKey(ProjectRequirement, on_delete=models.CASCADE)
    status = models.ForeignKey(RequirementStatus, on_delete=models.CASCADE)
    progress = models.FloatField(default=0)

    def __str__(self) -> str:
        return f"{self.project} - {self.requirement.id} - {self.status}"

class ProjectRequirementFollowUpComment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_date = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()
    file = models.FileField(upload_to='uploads/', null=True, blank=True)
    follow_up = models.ForeignKey(ProjectRequirementFollowUp, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.comment[:50]} - {self.comment_date}"
    

