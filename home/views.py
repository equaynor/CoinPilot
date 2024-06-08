from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib import messages
from allauth.account.views import SignupView


class Index(TemplateView):
    """
    View for the homepage.
    """
    template_name = 'home/index.html'


def home(request):
    """
    Render the homepage template.
    """
    return render(request, 'index.html')


def about(request):
    """
    Render the about page template.
    """
    return render(request, 'home/about.html')


class CustomSignupView(SignupView):
    """
    Custom signup view that displays a success message
    and redirects to the homepage.
    """
    def form_valid(self, form):
        """
        Handle a valid form submission.

        Args:
            form (Form): The form instance.

        Returns:
            HttpResponseRedirect: The redirect response.
        """
        response = super().form_valid(form)
        messages.success(self.request, 'Registration successful. Welcome!')
        return redirect('home')  # Redirect to the homepage URL
