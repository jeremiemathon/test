from typing import List
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from ..models import RequirementStatus

@method_decorator(login_required, name='dispatch')
class RequirementStatusListView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        requirements: List[RequirementStatus] = RequirementStatus.objects.all()
        return render(request, "requirementstatus_list.html", {"requirements": requirements})