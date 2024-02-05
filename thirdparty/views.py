from django.views.generic import View
from django.utils import timezone
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from typing import List, Any
import uuid


from .models import (
    ThirdParty,
    TP_Assessment,
    TP_Question,
    TP_AssessmentQuestion,
    TP_Score,
)

from .forms import (
    ThirdPartyForm,
    TP_AssessmentForm,
    TP_QuestionForm,
    TP_AssessmentQuestionForm
)


@method_decorator(login_required, name='dispatch')
class TP_ListView(View):

    def get(self, request: HttpRequest) -> HttpResponse:
        third_parties: List[ThirdParty] = ThirdParty.objects.all()
        assessment_scores: List[int] = []

        for third_party in third_parties:
            tp_assessments = TP_Assessment.objects.filter(third_party=third_party)
            if tp_assessments.exists():
                latest_assessment = tp_assessments.latest('date')
                if latest_assessment:
                    assessment_scores.append(latest_assessment.score)
            else:
                assessment_scores.append(0)
        third_parties = zip(third_parties, assessment_scores)
        return render(request, "thirdparty_list.html", {"third_parties": third_parties,
                                                        })

@method_decorator(login_required, name='dispatch')
class TP_CreateView(View):
    
    def get(self, request: HttpRequest) -> HttpResponse:
        form = ThirdPartyForm()
        return render(request, "thirdparty_create.html", {"form": form})

    def post(self, request: HttpRequest) -> HttpResponse:
        form = ThirdPartyForm(request.POST)
        if form.is_valid():
            thirparty = form.save()
            return redirect("tp_list")
        else:
            return render(request, "thirparty_create.html", {"form": form})
        

class TP_DeleteView(View):
    def get(self, request: HttpRequest, third_party_id: int) -> HttpResponse:
        third_party = get_object_or_404(ThirdParty, id=third_party_id)
        third_party.delete()

        return redirect("tp_list")

@method_decorator(login_required, name='dispatch')
class TP_AssessmentListView(View):
    # model = TP_Assessment
    def get(self, request: HttpRequest, third_party_id: int) -> HttpResponse:
        third_party = get_object_or_404(ThirdParty, id=third_party_id)
        projects = third_party.projects.order_by('-date_created')
        return render(request, "assessment_list.html", {"assessments": TP_Assessment.objects.filter(third_party_id=third_party_id).order_by('-date'),
                                                        "third_party": third_party,
                                                        "projects" : projects})

@method_decorator(login_required, name='dispatch')
class TP_AssessmentCreateView(View):
    # model = TP_Assessment
    def get(self, request: HttpRequest, third_party_id: int) -> HttpResponse:
        third_party = get_object_or_404(ThirdParty, id=third_party_id)
        date = timezone.now()
        assessment = TP_Assessment.objects.create(third_party=third_party, date=date)
        default_score = TP_Score.objects.order_by('value').first()

        questions = TP_Question.objects.all()
        for question in questions:
            TP_AssessmentQuestion.objects.create(assessment=assessment, question=question, score=default_score)

        return redirect("tp_assessment_list", third_party_id=third_party_id)

class TP_AssessmentDeleteView(View):
    def get(self, request: HttpRequest, assessment_id: int) -> HttpResponse:
        assessment: TP_Assessment = get_object_or_404(TP_Assessment, id=assessment_id)
        assessment.delete()
        return redirect("tp_assessment_list", third_party_id=assessment.third_party.id)

@method_decorator(login_required, name='dispatch')
class TP_QuestionCreateView(View):
    def get(self, request):
        highest_order = TP_Question.objects.order_by("-order").first()
        if highest_order:
            initial_order = highest_order.order + 1
        else:
            initial_order = 1
        form = TP_QuestionForm(initial={"order": initial_order})
        return render(request, "tp_question_create.html", {"form": form})

    def post(self, request):
        form = TP_QuestionForm(request.POST)
        if form.is_valid():
            question = form.save()
            # Additional logic for processing the form data or redirecting
            return redirect("tp_question_list")
        else:
            return render(request, "tp_question_create.html", {"form": form})
        

@method_decorator(login_required, name='dispatch')
class TP_QuestionListView(View):

    def get(self, request: HttpRequest) -> HttpResponse:
        questions = TP_Question.objects.order_by('order')
        print(questions)
        return render(request, "tp_question_list.html", {"questions": questions,})
    

@method_decorator(login_required, name='dispatch')
class TP_QuestionIncreaseOrderView(View):
    def get(self, request, question_id):
        question = get_object_or_404(TP_Question, id=question_id)
        target_order = question.order + 1

        # Find the question with the target order
        target_question = TP_Question.objects.filter(order=target_order).first()

        if target_question:
            # Swap the orders of the current question and the target question
            question.order, target_question.order = target_question.order, question.order
            question.save()
            target_question.save()
        return redirect("tp_question_list")

@method_decorator(login_required, name='dispatch')
class TP_QuestionDecreaseOrderView(View):
    def get(self, request, question_id):
        question = get_object_or_404(TP_Question, id=question_id)
        target_order = question.order - 1

        # Find the question with the target order
        target_question = TP_Question.objects.filter(order=target_order).first()

        if target_question:
            # Swap the orders of the current question and the target question
            question.order, target_question.order = target_question.order, question.order
            question.save()
            target_question.save()
        return redirect("tp_question_list")
    
@method_decorator(login_required, name='dispatch')
class TP_QuestionDeleteView(View):
    def get(self, request, question_id):
        question = get_object_or_404(TP_Question, id=question_id)
        question.delete()
        questions = TP_Question.objects.order_by("order")
        for index, question in enumerate(questions, start=1):
            question.order = index
            question.save()

        return redirect("tp_question_list")
    
@method_decorator(login_required, name='dispatch')
class TP_QuestionEditView(View):
    def get(self, request, question_id):
        question = get_object_or_404(TP_Question, id=question_id)
        form = TP_QuestionForm(instance=question)
        return render(
            request, "tp_question_edit.html", {"form": form, "question": question}
        )

    def post(self, request, question_id):
        question = get_object_or_404(TP_Question, id=question_id)
        form = TP_QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect("tp_question_list")
        return render(
            request, "tp_question_edit.html", {"form": form, "question": question}
        )


@method_decorator(login_required, name='dispatch')
class TP_AssessmentQuestionListView(View):

    def get(self, request: HttpRequest, assessment_id: int) -> HttpResponse:
        scores = TP_Score.objects.all()
        assessment_questions = TP_AssessmentQuestion.objects.filter(assessment_id=assessment_id)
        # print(assessment_questions)
        return render(request, "tp_assessment_question_list.html", {"assessment_questions": assessment_questions,
                                                                    "scores": scores,})
    
@method_decorator(login_required, name='dispatch')
class TP_AssessmentQuestionEditView(View):
    def post(self, request, assessment_question_id):
        assessment_question = get_object_or_404(TP_AssessmentQuestion, id=assessment_question_id)
        score = get_object_or_404(TP_Score, id=request.POST.get('score'))
        assessment = get_object_or_404(TP_Assessment, id=assessment_question.assessment.id)
        thirdparty = get_object_or_404(ThirdParty, id=assessment_question.assessment.third_party.id)
        assessment_questions = TP_AssessmentQuestion.objects.filter(assessment=assessment)
        assessment_question.score = score
        assessment_question.save()


        total_score = sum(assessment_question.score.value for assessment_question in assessment_questions)
        mean_score = total_score / len(assessment_questions)
        assessment.score = total_score
        # print(assessment.score)
        assessment.save()
        
        
        return redirect("tp_assessment_question_list", assessment_id=assessment_question.assessment.id)

@method_decorator(login_required, name='dispatch')
class TP_Public_AssessmentQuestionListView(View):
    def get(self, request: HttpRequest, public_token: uuid) -> HttpResponse:
        
        assessment_questions = TP_AssessmentQuestion.objects.filter(assessment__public_token=public_token)
        first_empty_answer = assessment_questions.filter(answer='').first()
        answered_questions = assessment_questions.exclude(answer__isnull=True).exclude(answer__exact='')
        assessment = get_object_or_404(TP_Assessment, public_token=public_token)

        if first_empty_answer:
            remaining_assessment_questions = assessment_questions.exclude(id=first_empty_answer.id)
        else:
            remaining_assessment_questions = assessment_questions

        # print(assessment_questions)
        return render(request, "tp_assessment_question_list_public.html", {"assessment_questions": assessment_questions,
                                                                           "assessment": assessment,
                                                                           "first_empty_answer": first_empty_answer,
                                                                           "answered_questions": answered_questions,
                                                                    })

@method_decorator(login_required, name='dispatch')
class TP_Public_AssessmentQuestionEditView(View):
    def post(self, request, assessment_question_id):
        assessment_question = get_object_or_404(TP_AssessmentQuestion, id=assessment_question_id)
        # answer = request.POST.get('assessment_question_{{assessment_question_id}}')
        answer = request.POST.get('answer')
        print(request)
        # assessment = get_object_or_404(TP_Assessment, id=assessment_question.assessment.id)
        # thirdparty = get_object_or_404(ThirdParty, id=assessment_question.assessment.third_party.id)
        # assessment_questions = TP_AssessmentQuestion.objects.filter(assessment=assessment)
        assessment_question.answer = answer
        assessment_question.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        # total_score = sum(assessment_question.score.value for assessment_question in assessment_questions)
        # mean_score = total_score / len(assessment_questions)
        # assessment.score = total_score
        # print(assessment.score)
        # assessment.save()

@login_required
def generate_public_token(request, assessment_id):
    assessment = get_object_or_404(TP_Assessment, id=assessment_id)
    assessment.public_token = uuid.uuid4()
    assessment.public = True
    assessment.save()

    # Return the token in a JSON response
    return redirect("tp_assessment_list", third_party_id=assessment.third_party.id)

@login_required
def delete_public_token(request, assessment_id):
    assessment = get_object_or_404(TP_Assessment, id=assessment_id)
    assessment.public_token = None
    assessment.public_password = None
    assessment.public = False
    assessment.save()

    # Return the token in a JSON response
    return redirect("tp_assessment_list", third_party_id=assessment.third_party.id)