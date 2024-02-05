from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from ..models import QuestionTag
from ..forms.questiontag_forms import QuestionTagForm

@method_decorator(login_required, name='dispatch')
class QuestionTagListView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        tags: QuestionTag = QuestionTag.objects.all()
        return render(request, "question_tag_list.html", {"question_tags": tags})
    
@method_decorator(login_required, name='dispatch')
class TagDeleteView(View):
    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        tag: QuestionTag = QuestionTag.objects.get(pk=pk)
        tag.delete()
        return redirect("questiontag-list")

@method_decorator(login_required, name='dispatch')
class TagCreateView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        form: QuestionTagForm = QuestionTagForm()
        return render(request, "tag_create.html", {"form": form})

    def post(self, request: HttpRequest) -> HttpResponse:
        name: str = request.POST.get("name")
        tag: QuestionTag = QuestionTag(name=name)
        tag.save()
        return redirect("questiontag-list")
