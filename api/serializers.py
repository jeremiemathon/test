from rest_framework import serializers
from project.models import (QuestionChoice, QuestionTag, Question, QuestionChoiceImpact, 
                     Answer, Project, ProjectRequirement, Tag, 
                     RequirementStatus, ProjectRequirementFollowUp, 
                     ProjectRequirementFollowUpComment)
from library.models import Document, Directory
from thirdparty.models import ThirdParty, TP_Assessment, TP_Question, TP_AssessmentQuestion

# Assuming DocumentSerializer is defined in your library app
# from library.serializers import DocumentSerializer


class ThirdPartySerializer(serializers.ModelSerializer):
    class Meta:
        model = ThirdParty
        fields = '__all__'

class TP_AssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TP_Assessment
        fields = '__all__'

class TP_QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TP_Question
        fields = '__all__'

class TP_AssessmentQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TP_AssessmentQuestion
        fields = '__all__'
        


class DirectorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Directory
        fields = '__all__'

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'

class QuestionChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionChoice
        fields = '__all__'

class QuestionTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionTag
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    choices = QuestionChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = '__all__'

class QuestionChoiceImpactSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(read_only=True)
    choice = QuestionChoiceSerializer(read_only=True)
    tags = QuestionTagSerializer(many=True, read_only=True)

    class Meta:
        model = QuestionChoiceImpact
        fields = '__all__'

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    tags = QuestionTagSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = '__all__'

class ProjectRequirementSerializer(serializers.ModelSerializer):
    tags = QuestionTagSerializer(many=True, read_only=True)
    documents = DocumentSerializer(many=True, read_only=True)

    class Meta:
        model = ProjectRequirement
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class RequirementStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequirementStatus
        fields = '__all__'

class ProjectRequirementFollowUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectRequirementFollowUp
        fields = '__all__'

class ProjectRequirementFollowUpCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectRequirementFollowUpComment
        fields = '__all__'
