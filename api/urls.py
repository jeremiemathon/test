from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (QuestionChoiceViewSet, QuestionTagViewSet, QuestionViewSet,
                    QuestionChoiceImpactViewSet, AnswerViewSet, ProjectViewSet,
                    ProjectRequirementViewSet, TagViewSet, RequirementStatusViewSet,
                    ProjectRequirementFollowUpViewSet, ProjectRequirementFollowUpCommentViewSet,
                    DirectoryViewSet, DocumentViewSet, ThirdPartyViewSet, TP_AssessmentViewSet,
                    TP_QuestionViewSet, TP_AssessmentQuestionViewSet)

router = DefaultRouter()
router.register(r'library/directories', DirectoryViewSet, basename='api_directory')
router.register(r'library/documents', DocumentViewSet, basename='api_document')
router.register(r'thirdparty/thirdparties', ThirdPartyViewSet, basename='api_thirdparty')
router.register(r'thirdparty/thirdpartyassessments', TP_AssessmentViewSet, basename='api_thirdpartyassessment')
router.register(r'thirdparty/thirdpartyquestions', TP_QuestionViewSet, basename='api_thirdpartyquestion')
router.register(r'thirdparty/thirdpartyassessmentquestions', TP_AssessmentQuestionViewSet, basename='api_thirdpartyassessmentquestion')

router.register(r'questionchoices', QuestionChoiceViewSet, basename='api_questionchoice')
router.register(r'questiontags', QuestionTagViewSet, basename='api_questiontag')
router.register(r'questions', QuestionViewSet, basename='api_question')
router.register(r'questionchoiceimpacts', QuestionChoiceImpactViewSet, basename='api_questionchoiceimpact')
router.register(r'answers', AnswerViewSet, basename='api_answer')
router.register(r'projects', ProjectViewSet, basename='api_project')
router.register(r'projectrequirements', ProjectRequirementViewSet, basename='api_projectrequirement')
router.register(r'tags', TagViewSet, basename='api_tag')
router.register(r'requirementstatuses', RequirementStatusViewSet, basename='api_requirementstatus')
router.register(r'projectrequirementfollowups', ProjectRequirementFollowUpViewSet, basename='api_projectrequirementfollowup')
router.register(r'projectrequirementfollowupcomments', ProjectRequirementFollowUpCommentViewSet, basename='api_projectrequirementfollowupcomment')

urlpatterns = [
    path('', include(router.urls)),
]
