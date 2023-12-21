from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from django.views import View
from django.urls import reverse_lazy
from django.http import HttpResponse, Http404

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from home.forms import SignUpForm

def signup_method(request):
    success_url=reverse_lazy('prototype:all')
    if request.user.is_anonymous:
        if request.method == "POST":
            form = SignUpForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')
                form.save()
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect(success_url)                 #################
            else:
                errors = "errors"
                form = SignUpForm()
                context = {
                    'form': form, 'errors' : errors
                }
                return render(request, 'registration/signup.html', context)
    else:
        return render(request, 'js/home.html')
    form = SignUpForm()
    context = {
        'form': form
    }
    return render(request, 'registration/signup.html', context)

def login_method(request):
    success_url=reverse_lazy('js:all')
    if request.user.is_anonymous:
        if request.method == "POST":
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get("username")
                password = form.cleaned_data.get("password")
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect(success_url)                    ###############
    else:
        return redirect(success_url)
    form = AuthenticationForm()
    context = {
        "form": form
    }
    return render(request, "registration/login.html", context)


class HomeView(View):
    template_name = 'js/homy.html'
    def get(self, request):
        ctx = {}
        return render(request, self.template_name, ctx)

