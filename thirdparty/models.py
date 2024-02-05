from django.db import models
import uuid
from project.models import Project

class ThirdParty(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    contact_info = models.TextField(blank=True)
    projects = models.ManyToManyField(Project, related_name='third_parties')

    def __str__(self):
        return self.name
    

class TP_Assessment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    third_party = models.ForeignKey(ThirdParty, on_delete=models.CASCADE, related_name="assessments")
    date = models.DateTimeField()
    score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    completed = models.BooleanField(default=False)
    public_token = models.UUIDField(default=uuid.uuid4, null=True, blank=True)
    public_password = models.CharField(max_length=128, null=True, blank=True)
    public = models.BooleanField(default=False)

    def __str__(self):
        return f"Assessment for {self.third_party.name} on {self.date}"

class TP_Question(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.IntegerField(default=0, db_index=True)
    description = models.TextField()
    details = models.TextField(blank=True, null=True)
    max_score = models.IntegerField(default=3)
    weight = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.order} - Weight: {self.weight}, Max: {self.max_score} -- {self.description}'



    
class TP_Score(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    value = models.FloatField(default=1)

    def __str__(self) -> str:
        return f"{self.name} - {self.value}"

class TP_AssessmentQuestion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    assessment = models.ForeignKey(TP_Assessment, on_delete=models.CASCADE, related_name="assessment_questions")
    question = models.ForeignKey(TP_Question, on_delete=models.CASCADE, related_name="assessment_questions")
    answer = models.TextField(blank=True)
    score = models.ForeignKey(TP_Score, on_delete=models.CASCADE, related_name="assessment_score", null=True)

    class Meta:
        unique_together = ("assessment", "question")

    def __str__(self):
        return f"Score for {self.question.description} in {self.assessment}"
    

