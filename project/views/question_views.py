from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from ..models import Question
from ..forms.question_forms import QuestionForm

@method_decorator(login_required, name='dispatch')
class QuestionCreateView(View):
    def get(self, request):
        highest_order = Question.objects.order_by("-order").first()
        if highest_order:
            initial_order = highest_order.order + 1
        else:
            initial_order = 1
        form = QuestionForm(initial={"order": initial_order})
        return render(request, "question_create.html", {"form": form})

    def post(self, request):
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save()
            # Additional logic for processing the form data or redirecting
            return redirect("question-list")
        else:
            return render(request, "question_create.html", {"form": form})

@method_decorator(login_required, name='dispatch')
class QuestionListView(View):
    def get(self, request):
        questions = Question.objects.order_by("order")
        return render(request, "question_list.html", {"questions": questions})

@method_decorator(login_required, name='dispatch')
class QuestionEditView(View):
    def get(self, request, question_id):
        question = get_object_or_404(Question, id=question_id)
        form = QuestionForm(instance=question)
        return render(
            request, "question_edit.html", {"form": form, "question": question}
        )

    def post(self, request, question_id):
        question = get_object_or_404(Question, id=question_id)
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect("question-list")
        return render(
            request, "question_edit.html", {"form": form, "question": question}
        )

@method_decorator(login_required, name='dispatch')
class QuestionIncreaseOrderView(View):
    def get(self, request, question_id):
        question = get_object_or_404(Question, id=question_id)
        target_order = question.order + 1

        # Find the question with the target order
        target_question = Question.objects.filter(order=target_order).first()

        if target_question:
            # Swap the orders of the current question and the target question
            question.order, target_question.order = target_question.order, question.order
            question.save()
            target_question.save()
        return redirect("question-list")

@method_decorator(login_required, name='dispatch')
class QuestionDecreaseOrderView(View):
    def get(self, request, question_id):
        question = get_object_or_404(Question, id=question_id)
        target_order = question.order - 1

        # Find the question with the target order
        target_question = Question.objects.filter(order=target_order).first()

        if target_question:
            # Swap the orders of the current question and the target question
            question.order, target_question.order = target_question.order, question.order
            question.save()
            target_question.save()
        return redirect("question-list")

@method_decorator(login_required, name='dispatch')
class QuestionDeleteView(View):
    def get(self, request, question_id):
        question = get_object_or_404(Question, id=question_id)
        question.delete()
        questions = Question.objects.order_by("order")
        for index, question in enumerate(questions, start=1):
            question.order = index
            question.save()

        return redirect("question-list")
