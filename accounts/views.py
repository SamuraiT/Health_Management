from django.shortcuts import render, redirect
from django.views import View
from accounts.models import CustomUser
from accounts.forms import ProfileForm
from allauth.account import views
from accounts.forms import ProfileForm, SignupUserForm
from django.contrib.auth.mixins import LoginRequiredMixin 

# Create your views here.

class ProfileView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user_data = CustomUser.objects.get(id=request.user.id)

        return render(request, 'accounts/profile.html', {
            'user_data': user_data,
        }) 

class ProfileEditView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user_data = CustomUser.objects.get(id=request.user.id)
        form = ProfileForm(
            request.POST or None,
            initial = {
                'first_name' : user_data.first_name,
                'last_name' : user_data.last_name,
                'age' : user_data.age,
                'height' : user_data.height,
                'target_weight' : user_data.weight,
            }
        )

        return render (request, 'accounts/profile_edit.html', {
            'form':form
        })

    def post(self, request, *args, **kwargs):
        form = ProfileForm(request.POST or None)
        if form.is_valid():
            user_data = CustomUser.objects.get(id=request.user.id)
            user_data.first_name = form.cleaned_data['first_name']
            user_data.last_name = form.cleaned_data['last_name']
            user_data.age = form.cleaned_data['age']
            user_data.height = form.cleaned_data['height']
            user_data.weight = form.cleaned_data['weight']
            user_data.save()
            return redirect('profile')
        
        return render(request, 'accounts/profile.html', {
            'form':form
        })


class LoginView(views.LoginView):
    template_name = 'accounts/login.html'


class LogoutView(views.LogoutView):
    template_name = 'accounts/logout.html'

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            self.logout()
        return redirect('account_login')


class SignupView(views.SignupView):
    template_name = 'accounts/signup.html'
    form_class = SignupUserForm