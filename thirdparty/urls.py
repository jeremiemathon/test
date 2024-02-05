from django.urls import path
from .views import (
    TP_ListView,
    TP_CreateView,
    TP_DeleteView,
    TP_AssessmentCreateView,
    TP_AssessmentListView,
    TP_QuestionListView,
    TP_QuestionIncreaseOrderView,
    TP_QuestionDecreaseOrderView,
    TP_QuestionCreateView,
    TP_QuestionDeleteView,
    TP_QuestionEditView,
    TP_AssessmentQuestionListView,
    TP_AssessmentQuestionEditView,
    TP_AssessmentDeleteView,
    TP_Public_AssessmentQuestionListView,
    TP_Public_AssessmentQuestionEditView,
    
    generate_public_token,
    delete_public_token,

    )

urlpatterns = [
    # Third Party URLs
    path('', TP_ListView.as_view(), name='tp_list'),
    path('<uuid:third_party_id>/', TP_AssessmentListView.as_view(), name='tp_assessment_list'),
    path('<uuid:third_party_id>/delete', TP_DeleteView.as_view(), name='tp_delete'),
    path('create/', TP_CreateView.as_view(), name='tp_create'),

    # Assessment URLs
    path('<uuid:third_party_id>/assessment-create/', TP_AssessmentCreateView.as_view(), name='tp_assessment_create'),
    path('assessment_questions/<uuid:assessment_id>/', TP_AssessmentQuestionListView.as_view(), name='tp_assessment_question_list'),
    path('assessment_question_update/<uuid:assessment_question_id>/edit/', TP_AssessmentQuestionEditView.as_view(), name='tp_assessment_question_edit'),
    path('assessment_delete/<uuid:assessment_id>/', TP_AssessmentDeleteView.as_view(), name='tp_assessment_delete'),

    path('public/<uuid:public_token>/', TP_Public_AssessmentQuestionListView.as_view(), name='tp_public_assessment_question_list'),
    path('public/<uuid:assessment_question_id>/edit/', TP_Public_AssessmentQuestionEditView.as_view(), name='tp_public_assessment_question_edit'),

    # Question URLs
    path('questions/', TP_QuestionListView.as_view(), name='tp_question_list'),
    path("question/<uuid:question_id>/i",TP_QuestionIncreaseOrderView.as_view(),name="tp_question_increase_order",),
    path("question/<uuid:question_id>/d",TP_QuestionDecreaseOrderView.as_view(),name="tp_question_decrease_order",),
    path("question/create",TP_QuestionCreateView.as_view(),name="tp_question_create",),
    path("question/<uuid:question_id>/delete",TP_QuestionDeleteView.as_view(),name="tp_question_delete",),
    path("question/<uuid:question_id>/edit",TP_QuestionEditView.as_view(),name="tp_question_edit",),


    path('generate-token/<uuid:assessment_id>/', generate_public_token, name='generate_public_token'),
    path('delete-token/<uuid:assessment_id>/', delete_public_token, name='delete_public_token'),



]