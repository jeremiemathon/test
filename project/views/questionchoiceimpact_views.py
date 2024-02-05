from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from ..models import QuestionChoiceImpact
from ..forms.questionchoiceimpact_forms import QuestionChoiceImpactForm
from django.db.models import F

@method_decorator(login_required, name='dispatch')
class QuestionChoiceImpactCreateView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        form = QuestionChoiceImpactForm()
        return render(request, "question_choice_impact_create.html", {"form": form})

    def post(self, request: HttpRequest) -> HttpResponse:
        form = QuestionChoiceImpactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("question-choice-impact-list")
        return render(request, "question_choice_impact_create.html", {"form": form})

@method_decorator(login_required, name='dispatch')
class QuestionChoiceImpactListView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        impacts = QuestionChoiceImpact.objects.all().order_by('question__order')
        return render(request, "question_choice_impact_list.html", {"impacts": impacts})

@method_decorator(login_required, name='dispatch')
class QuestionChoiceImpactEditView(View):
    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        impact = get_object_or_404(QuestionChoiceImpact, pk=pk)
        form = QuestionChoiceImpactForm(instance=impact)
        return render(
            request,
            "question_choice_impact_edit.html",
            {"form": form, "impact": impact},
        )

    def post(self, request : HttpRequest, pk:int) -> HttpResponse:
        impact = get_object_or_404(QuestionChoiceImpact, pk=pk)
        form = QuestionChoiceImpactForm(request.POST, instance=impact)
        if form.is_valid():
            form.save()
            return redirect("question-choice-impact-list")
        return render(
            request,
            "question_choice_impact_edit.html",
            {"form": form, "impact": impact},
        )
