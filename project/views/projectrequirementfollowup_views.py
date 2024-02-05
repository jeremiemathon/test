from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import CreateView, UpdateView
from django.utils import timezone
from ..models import ProjectRequirementFollowUp, RequirementStatus, Project, ProjectRequirementFollowUpComment
from thirdparty.models import ThirdParty
from ..forms.projectrequirementfollowup_forms import ProjectRequirementFollowUpForm
from typing import List, Any
from ..forms.project_forms import ProjectForm
from thirdparty.models import TP_Assessment


@method_decorator(login_required, name="dispatch")
class ProjectRequirementFollowUpCreateView(CreateView):
    model = ProjectRequirementFollowUp
    form_class = ProjectRequirementFollowUpForm
    template_name = "project_requirement_followup_create.html"
    success_url = "/"


@method_decorator(login_required, name="dispatch")
class ProjectRequirementFollowUpEditView(View):
    
    def get(self, request, pk):
        statuses = RequirementStatus.objects.all()
        project = Project.objects.get(pk=pk)
        project_third_parties = project.third_parties.all()
        assessment_scores: List[int] = []

        for third_party in project_third_parties:
            tp_assessments = TP_Assessment.objects.filter(third_party=third_party)
            if tp_assessments.exists():
                latest_assessment = tp_assessments.latest('date')
                if latest_assessment:
                    assessment_scores.append(latest_assessment.score)
            else:
                assessment_scores.append(0)
        project_third_parties = list(zip(project_third_parties, assessment_scores))

        followups= ProjectRequirementFollowUp.objects.filter(project=project)
        
        for followup in followups:
            followups_comments = ProjectRequirementFollowUpComment.objects.filter(follow_up_id=followup.id)
            followup.updated_date = followup.updated_date.strftime("%d/%m/%Y")
            followup.comment_count = len(followups_comments)

        context = {
            "project": project,
            "followups": followups,
            "statuses": statuses,
            "project_third_parties": project_third_parties,
            "third_parties": ThirdParty.objects.all(),
        }



        return render(request, "project_requirement_followup_edit.html", context)

    def post(self, request, pk):
        followups = ProjectRequirementFollowUp.objects.get(pk=pk)
        status_id = request.POST.get("status")
        status = RequirementStatus.objects.get(pk=status_id)
        project = Project.objects.get(pk=followups.project.id)
        project.signed_off = False
        followups.status = status

        followups.save()
        project.date_updated = timezone.now()  # Update the updated_date of the related Project
        project.save()  # Save the updated project
        self.calculate_completion(followups.project.id)
        

        return redirect("follow-up-edit", pk=followups.project.id)

    def calculate_completion(self, project_id):
        project = Project.objects.get(pk=project_id)
        follow_ups = project.projectrequirementfollowup_set.all()
        total_points = sum(
            follow_up.status.value
            for follow_up in follow_ups
            if follow_up.status.value is not None and follow_up.status.value >= 0
        )

        total_count = sum(
            1
            for follow_up in follow_ups
            if follow_up.status.value is not None and follow_up.status.value >= 0
        )
        print(f"{total_count} - {total_points}")
        if total_count > 0:
            project.progress = (total_points / (total_count * 1.0)) * 100
        else:
            project.progress = 0
        project.save()


@login_required
def update_project_requirement_followups(request, project_id):
    print("method")
    if request.method == "GET":
        project = Project.objects.get(pk=project_id)
        # follow_up = ProjectRequirementFollowUp.objects.get()
        form = ProjectForm(request.POST)
        form.edit_project_requirement_followups(project_id)
        return redirect("follow-up-edit", pk=project_id)

    return redirect("project-list")


@login_required
def signoff_followup(request, project_id):
    project = Project.objects.get(pk=project_id)
    project.signed_off = not project.signed_off
    # if project.signed_off:
    #     project.signed_off = False
    # else:
    #     project.signed_off = True
    # print(project.signed_off)
    project.save()
    return redirect("follow-up-edit", pk=project_id)


def update_project_thirdparties(request):
    if request.method == 'POST':
        project_id = request.POST.get('project_id')
        third_party_ids = request.POST.getlist('third_party_ids')

        project: Project = get_object_or_404(Project, id=project_id)
        third_parties = ThirdParty.objects.filter(id__in=third_party_ids)

        # Update project with selected third parties
        # This depends on your Project and ThirdParty model relationship
        project.third_parties.set(third_parties)
        return redirect("follow-up-edit", pk=project_id)
