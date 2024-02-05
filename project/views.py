from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpRequest, HttpResponse
from .models import ProjectRequirementFollowUpComment, ProjectRequirementFollowUp

def add_comment(request: HttpRequest, followup_id: int):
    if request.method == 'POST':
        comment_text = request.POST.get('comment')
        user = request.user  # Assuming you have user authentication
        followup = get_object_or_404(ProjectRequirementFollowUp, id=followup_id)
        comment = ProjectRequirementFollowUpComment.objects.create(
            user=user,
            comment=comment_text,
            followup=followup
        )
        return JsonResponse({'status': 'success'}, status=200)
    else:
        return JsonResponse({'status': 'fail'}, status=400)