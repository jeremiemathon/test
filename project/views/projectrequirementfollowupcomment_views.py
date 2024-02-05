from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.views import View
from django.http import JsonResponse
from ..models import ProjectRequirementFollowUpComment, ProjectRequirementFollowUp

@login_required
def add_comment(request, followup_id):
    if request.method == 'POST':
        
        comment_text = request.POST.get('comment')
        user = request.user  # Assuming you have user authentication
        followup = get_object_or_404(ProjectRequirementFollowUp, id=followup_id)
        comment = ProjectRequirementFollowUpComment.objects.create(
            user=user,
            comment=comment_text,
            follow_up=followup
        )
        return redirect('comment-list', followup_id=followup_id)
    else:
        return redirect('comment-list', followup_id=followup_id)
    
@method_decorator(login_required, name="dispatch")
class CommentListView(View):
    def get(self, request, followup_id):
        comments = ProjectRequirementFollowUpComment.objects.filter(follow_up_id=followup_id).order_by('-comment_date')
        follow_up = get_object_or_404(ProjectRequirementFollowUp, id=followup_id)
        context = {
            "comments": comments,
            "follow_up": follow_up,
        }
        return render(request, 'project_requirement_followup_comment_list.html', context)

@method_decorator(login_required, name="dispatch")
class CommentDeleteView(View):
    def post(self, request, comment_id):
        comment = get_object_or_404(ProjectRequirementFollowUpComment, id=comment_id)
        if request.user == comment.user:
            comment.delete()
        return redirect('comment-list', followup_id=comment.follow_up.id)