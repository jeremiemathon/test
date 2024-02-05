"""
URL configuration for security_by_design project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLcon>f
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from settings.views import (
    settings_view,
)
from project.views.project_views import (
    ProjectCreateView,
    ProjectListView,
    ProjectEditView,
    ProjectDeleteView,
)

from project.views.question_views import (
    QuestionCreateView,
    QuestionListView,
    QuestionEditView,
    QuestionDecreaseOrderView,
    QuestionIncreaseOrderView,
    QuestionDeleteView,
)
from project.views.questionchoiceimpact_views import (
    QuestionChoiceImpactCreateView,
    QuestionChoiceImpactListView,
    QuestionChoiceImpactEditView,
)

from project.views.projectrequirement_views import (
    ProjectRequirementListView,
    ProjectRequirementCreateView,
    ProjectRequirementEditView,
    ProjectrequirementDecreaseOrderView,
    ProjectrequirementIncreaseOrderView,
    ProjectRequirementDeleteView,
    add_document_to_requirement,
)

from project.views.projectrequirementfollowup_views import (
    ProjectRequirementFollowUpCreateView,
    ProjectRequirementFollowUpEditView,
    update_project_requirement_followups,
    signoff_followup,
    update_project_thirdparties,
)

from project.views.requirementstatus_views import (
    RequirementStatusListView,
)

from project.views.tag_views import QuestionTagListView, TagDeleteView, TagCreateView

from login.views import LoginView, LogoutView, UserListView
from project.views.projectrequirementfollowupcomment_views import (
    add_comment,
    CommentListView,
    CommentDeleteView,
)



urlpatterns = [
    path("admin/", admin.site.urls, name="admin"),
    path("", ProjectListView.as_view(), name="project-list"),
    path("library/", include("library.urls")),
    path("thirdparty/", include("thirdparty.urls")),
    path("project/create", ProjectCreateView.as_view(), name="project-create"),
    path("projects/", ProjectListView.as_view(), name="project-list"),
    path(
        "project/<uuid:project_id>/",
        ProjectEditView.as_view(),
        name="edit-project",
    ),
    path("questions/", QuestionListView.as_view(), name="question-list"),
    path(
        "question/<uuid:question_id>/i",
        QuestionIncreaseOrderView.as_view(),
        name="question-increase-order",
    ),
    path(
        "question/<uuid:question_id>/d",
        QuestionDecreaseOrderView.as_view(),
        name="question-decrease-order",
    ),
    path("question/create/", QuestionCreateView.as_view(), name="question-create"),
    path("questions/", QuestionListView.as_view(), name="question-list"),
    # path(
    #     "question/<uuid:question_id>/",
    #     QuestionEditView.as_view(),
    #     name="question-edit",
    # ),
    path(
        "question/<uuid:question_id>/",
        QuestionEditView.as_view(),
        name="edit-question",
    ),
    path(
        "question/<uuid:question_id>/delete/",
        QuestionDeleteView.as_view(),
        name="delete-question",
    ),
    path(
        "impact/create/",
        QuestionChoiceImpactCreateView.as_view(),
        name="question-choice-impact-create",
    ),
    path(
        "impacts/",
        QuestionChoiceImpactListView.as_view(),
        name="question-choice-impact-list",
    ),
    path(
        "impact/<uuid:pk>/",
        QuestionChoiceImpactEditView.as_view(),
        name="edit-question-choice-impact",
    ),
    path(
        "project/<uuid:pk>/delete", ProjectDeleteView.as_view(), name="project-delete"
    ),
    path(
        "requirements/",
        ProjectRequirementListView.as_view(),
        name="projectrequirement-list",
    ),
    path(
        "requirement/create/",
        ProjectRequirementCreateView.as_view(),
        name="projectrequirement-create",
    ),
    path(
        "requirement/<uuid:pk>/",
        ProjectRequirementEditView.as_view(),
        name="projectrequirement-edit",
    ),
    path(
        "requirement/<uuid:pk>/i",
        ProjectrequirementIncreaseOrderView.as_view(),
        name="projectrequirement-increase-order",
    ),
    path(
        "requirement/<uuid:pk>/d",
        ProjectrequirementDecreaseOrderView.as_view(),
        name="projectrequirement-decrease-order",
    ),
    path('requirement/doc/<uuid:pk>/', add_document_to_requirement, name='requirement_document_view'),
    path(
        "fu/c/",
        ProjectRequirementFollowUpCreateView.as_view(),
        name="follow-up-create",
    ),
    path(
        "project/<uuid:pk>/controls",
        ProjectRequirementFollowUpEditView.as_view(),
        name="follow-up-edit",
    ),
    path(
        "fu/e/<uuid:pk>/",
        ProjectRequirementFollowUpEditView.as_view(),
        name="single-follow-up-edit",
    ),
    path(
        "requirement/<uuid:pk>/delete/",
        ProjectRequirementDeleteView.as_view(),
        name="projectrequirement-delete",
    ),
    path(
        "ufu/<uuid:project_id>/",
        update_project_requirement_followups,
        name="update-follow-up",
    ),
    path('update_project_thirdparties/', update_project_thirdparties, name='update_project_thirdparties'),
    path(
        "fu/so/<uuid:project_id>/",
        signoff_followup,
        name="follow-up-signoff",
    ),
    path(
        "status/", RequirementStatusListView.as_view(), name="requirement-status-list"
    ),
    path('add-comment/<uuid:followup_id>/', add_comment, name='add-comment'),
    path(
        'comments/<uuid:followup_id>/',
        CommentListView.as_view(),
        name='comment-list',
    ),
    path(
        'delete-comment/<uuid:comment_id>/',
        CommentDeleteView.as_view(),
        name='delete-comment',
    ),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("users/", UserListView.as_view(), name="user-list"),
    path(
        "tags/", QuestionTagListView.as_view(), name="questiontag-list"
    ),
    path(
        "dtags/<uuid:pk>/", TagDeleteView.as_view(), name="questiontag-delete"
    ),
    path(
        "add-tag/", TagCreateView.as_view(), name="questiontag-create"
    ),
    path("__debug__/", include("debug_toolbar.urls")),
    path('api/', include('api.urls')),
    path('settings/', settings_view, name='settings'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)