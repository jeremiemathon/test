from rest_framework import viewsets
from project.models import (QuestionChoice, QuestionTag, Question, QuestionChoiceImpact, 
                     Answer, Project, ProjectRequirement, Tag, 
                     RequirementStatus, ProjectRequirementFollowUp, 
                     ProjectRequirementFollowUpComment)
from library.models import Document, Directory
from thirdparty.models import ThirdParty, TP_Assessment, TP_Question, TP_AssessmentQuestion
from .serializers import (QuestionChoiceSerializer, QuestionTagSerializer, QuestionSerializer, 
                          QuestionChoiceImpactSerializer, AnswerSerializer, ProjectSerializer, 
                          ProjectRequirementSerializer, TagSerializer, 
                          RequirementStatusSerializer, ProjectRequirementFollowUpSerializer, 
                          ProjectRequirementFollowUpCommentSerializer, DirectorySerializer,
                          DocumentSerializer, ThirdPartySerializer, TP_AssessmentSerializer,
                          TP_QuestionSerializer, TP_AssessmentQuestionSerializer)

class DirectoryViewSet(viewsets.ModelViewSet):
    queryset = Directory.objects.all()
    serializer_class = DirectorySerializer

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

class ThirdPartyViewSet(viewsets.ModelViewSet):
    queryset = ThirdParty.objects.all()
    serializer_class = ThirdPartySerializer

class TP_AssessmentViewSet(viewsets.ModelViewSet):
    queryset = TP_Assessment.objects.all()
    serializer_class = TP_AssessmentSerializer

class TP_QuestionViewSet(viewsets.ModelViewSet):
    queryset = TP_Question.objects.all()
    serializer_class = TP_QuestionSerializer

class TP_AssessmentQuestionViewSet(viewsets.ModelViewSet):
    queryset = TP_AssessmentQuestion.objects.all()
    serializer_class = TP_AssessmentQuestionSerializer
    

class QuestionChoiceViewSet(viewsets.ModelViewSet):
    queryset = QuestionChoice.objects.all()
    serializer_class = QuestionChoiceSerializer

class QuestionTagViewSet(viewsets.ModelViewSet):
    queryset = QuestionTag.objects.all()
    serializer_class = QuestionTagSerializer

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class QuestionChoiceImpactViewSet(viewsets.ModelViewSet):
    queryset = QuestionChoiceImpact.objects.all()
    serializer_class = QuestionChoiceImpactSerializer

class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class ProjectRequirementViewSet(viewsets.ModelViewSet):
    queryset = ProjectRequirement.objects.all()
    serializer_class = ProjectRequirementSerializer

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class RequirementStatusViewSet(viewsets.ModelViewSet):
    queryset = RequirementStatus.objects.all()
    serializer_class = RequirementStatusSerializer

class ProjectRequirementFollowUpViewSet(viewsets.ModelViewSet):
    queryset = ProjectRequirementFollowUp.objects.all()
    serializer_class = ProjectRequirementFollowUpSerializer

class ProjectRequirementFollowUpCommentViewSet(viewsets.ModelViewSet):
    queryset = ProjectRequirementFollowUpComment.objects.all()
    serializer_class = ProjectRequirementFollowUpCommentSerializer
