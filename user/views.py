from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import LoginUserForm, RegisterUserForm, ProfileUserForm, UserPasswordChangeForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from site1.settings import DEFAULT_USER_IMAGE



class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'user/login.html'
    extra_context = {'title': "Авторизация"}

 #  def get_success_url(self):
 #      return reverse_lazy('home')

def registr(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # создание объекта без сохранения в БД
            user.set_password(form.cleaned_data['password'])
            user.save()
            return render(request, 'user/registr_done.html')
    else:
        form = RegisterUserForm()
    return render(request, 'user/registr.html', {'form': form})

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'user/registr.html'
    extra_context = {'title': "Регистрация"}
    success_url = reverse_lazy('user:login')


class ProfileUser(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'user/profile.html'
    extra_context = {'title': "Профиль пользователя", 'default_image': DEFAULT_USER_IMAGE }

    def get_success_url(self):
        return reverse_lazy('user:profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("user:password_change_done")
    template_name = "user/password_change_form.html"
    extra_context = {'title': "Изменение пароля"}