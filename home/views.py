from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib import messages
from allauth.account.views import SignupView

class Index(TemplateView):
    template_name = 'home/index.html'

def home(request):
    return render(request, 'index.html')


class CustomSignupView(SignupView):
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Registration successful. Welcome!')
        return redirect('home')  # Redirect to the homepage URL