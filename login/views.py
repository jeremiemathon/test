from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.views import View
from .forms import UserForm

# Create your views here.
class LoginView(LoginView):
    template_name = 'login.html'  # Replace with the path to your login template
    def get_success_url(self):
        return reverse_lazy('project-list')
    
class LogoutView(LogoutView):
    next_page = '/'  # Replace 'home' with the desired URL or name of the page to redirect after logout

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        return redirect(reverse_lazy('login'))

class UserListView(View):
    def get(self, request):
        users = User.objects.all()
        form = UserForm()
        return render(request, 'user_list.html', {'users': users, 'form': form})