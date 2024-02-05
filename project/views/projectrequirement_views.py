from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from ..models import ProjectRequirement
from library.models import Document
from ..forms.projectrequirement_forms import ProjectRequirementForm, RequirementDocumentForm

@method_decorator(login_required, name='dispatch')
class ProjectRequirementListView(View):
    def get(self, request):
        requirements = ProjectRequirement.objects.order_by("order")
        return render(
            request, "projectrequirement_list.html", {"requirements": requirements}
        )

@method_decorator(login_required, name='dispatch')
class ProjectRequirementCreateView(View):
    def get(self, request):
        highest_order = ProjectRequirement.objects.order_by("-order").first()
        if highest_order:
            initial_order = highest_order.order + 1
        else:
            initial_order = 1
        form = ProjectRequirementForm(initial={"order": initial_order})
        return render(request, "projectrequirement_create.html", {"form": form})

    def post(self, request):
        form = ProjectRequirementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("projectrequirement-list")
        return render(request, "projectrequirement_create.html", {"form": form})

@method_decorator(login_required, name='dispatch')
class ProjectRequirementEditView(View):
    def get(self, request, pk):
        projectrequirement = get_object_or_404(ProjectRequirement, pk=pk)
        form = ProjectRequirementForm(instance=projectrequirement)
        return render(
            request,
            "projectrequirement_edit.html",
            {"form": form, "projectrequirement": projectrequirement},
        )

    def post(self, request, pk):
        projectrequirement = get_object_or_404(ProjectRequirement, pk=pk)
        form = ProjectRequirementForm(request.POST, instance=projectrequirement)
        if form.is_valid():
            form.save()
            return redirect("projectrequirement-list")
        return render(
            request,
            "projectrequirement_edit.html",
            {"form": form, "projectrequirement": projectrequirement},
        )

@method_decorator(login_required, name='dispatch')
class ProjectrequirementIncreaseOrderView(View):
    def get(self, request, pk):
        projectrequirement = get_object_or_404(ProjectRequirement, pk=pk)
        target_order = projectrequirement.order + 1

        # Find the question with the target order
        target_projectrequirement = ProjectRequirement.objects.filter(order=target_order).first()

        if target_projectrequirement:
            # Swap the orders of the current question and the target question
            projectrequirement.order, target_projectrequirement.order = target_projectrequirement.order, projectrequirement.order
            projectrequirement.save()
            target_projectrequirement.save()
        return redirect("projectrequirement-list")

@method_decorator(login_required, name='dispatch')
class ProjectrequirementDecreaseOrderView(View):
    def get(self, request, pk):
        projectrequirement = get_object_or_404(ProjectRequirement, pk=pk)
        
        target_order = projectrequirement.order - 1

        # Find the question with the target order
        target_question = ProjectRequirement.objects.filter(order=target_order).first()

        if target_question:
            # Swap the orders of the current question and the target question
            projectrequirement.order, target_question.order = target_question.order, projectrequirement.order
            projectrequirement.save()
            target_question.save()


        return redirect("projectrequirement-list")
    
@method_decorator(login_required, name='dispatch')
class ProjectRequirementDeleteView(View):
    def get(self, request, pk):
        projectrequirement = get_object_or_404(ProjectRequirement, pk=pk)
        projectrequirement.delete()
        projectrequirements = ProjectRequirement.objects.order_by("order")
        for index, projectrequirement in enumerate(projectrequirements, start=1):
            projectrequirement.order = index
            projectrequirement.save()
        return redirect("projectrequirement-list")



def add_document_to_requirement(request, pk):

    requirement = get_object_or_404(ProjectRequirement, id=pk)
    if request.method == 'POST':
        selected_options = request.POST.getlist('selected_documents')
        requirement.documents.set(selected_options)
        requirement.save()
    else:
        form = RequirementDocumentForm(instance=requirement)

        context = {
            'form': form,
            'requirement': requirement,
            'documents': Document.objects.all(),
        }

        return render(request, 'projectrequirement_document_view.html', context)
    return redirect("projectrequirement-list")