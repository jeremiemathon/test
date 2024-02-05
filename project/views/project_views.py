from typing import List, Any
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpRequest, HttpResponse

from django.views import View
from ..models import (
    Project,
    ProjectRequirement,
    ProjectRequirementFollowUp,
    RequirementStatus,
)
from ..forms.project_forms import ProjectForm

@method_decorator(login_required, name='dispatch')
class ProjectCreateView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        print(request.META["REMOTE_ADDR"])
        form = ProjectForm()
        return render(request, "project_create.html", {"form": form})

    def post(self, request: HttpRequest) -> HttpResponse:
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save()
            return redirect("follow-up-edit", pk=project.id)
        else:
            return render(request, "project_create.html", {"form": form})

@method_decorator(login_required, name='dispatch')
class ProjectListView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        projects: List[Project] = list(Project.objects.all())
        for project in projects:
            project.date_updated = project.date_updated.strftime("%d/%m/%Y")
        return render(request, "project_list.html", {"projects": projects})

@method_decorator(login_required, name='dispatch')
class ProjectEditView(View):
    def get(self, request: HttpRequest, project_id: int)  -> HttpResponse:
        project = get_object_or_404(Project, id=project_id)
        form = ProjectForm(instance=project)
        return render(request, "project_edit.html", {"form": form, "project": project})

    def post(self, request: HttpRequest, project_id: int) -> HttpResponse:
        project = Project.objects.get(id=project_id)
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            project = form.save(project_id)
            return redirect("follow-up-edit", pk=project.id)
        else:
            print("Error")
            return render(request, "project_edit.html", {"form": form, "project": project})

@method_decorator(login_required, name='dispatch')
class ProjectDeleteView(View):
    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        project = Project.objects.get(pk=pk)
        project.delete()
        return redirect("project-list")
