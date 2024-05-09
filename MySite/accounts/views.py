from django.db.models.base import Model as Model
from django.db import transaction
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import DetailView, UpdateView, CreateView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView

from .models import Profile
from .forms import UserUpdateForm, ProfileUpdateForm, UserLoginForm, UserRegisterForm


class ProfileDetailView(DetailView):
    """
    Представление для просмотра профиля
    """
    model = Profile
    context_object_name = 'profile'
    template_name = 'accounts/profile_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Профиль пользователя: {self.object.user.username}'
        return context
    
class ProfileUpdateView(UpdateView):
    """
    Редактирование профиля
    """
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'accounts/profile_edit.html'

    def get_object(self) -> Model:
        " мы передаем текущего пользователя, чтобы не редактировать чужие профили "
        return self.request.user.profile
    
    def get_context_data(self, **kwargs) :
        " В контексте мы добавляем форму пользователя, где ссылаемся на текущего пользователя "
        context = super().get_context_data(**kwargs)
        context['title'] = f'Редактирование профиля пользователя: {self.request.user.username}'
        if self.request.POST :
            context['user_form'] = UserUpdateForm(self.request.POST, instance=self.request.user)
        else :
            context['user_form'] = UserUpdateForm(instance=self.request.user)
        return context
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        context = self.get_context_data()
        user_form = context['user_form']
        with transaction.atomic():
            " мы используем transaction.atomic, для корректного сохранения данных двух форм в нашей БД. "
            if all([form.is_valid(), user_form.is_valid()]):
                " Проверяем обе формы на правильность, и сохраняем их. "
                user_form.save()
                form.save()
            else:
                context.update({"user_form": user_form})
                return self.render_to_response(context)
        return super(ProfileUpdateView, self).form_valid(form)
    def get_success_url(self):
        " мы ссылаемся на наш профиль, т.е после сохранения мы переходим на страницу нашего профиля. "
        return reverse_lazy('profile_detail', kwargs={'slug': self.object.slug})
    
class UserRegisterView(SuccessMessageMixin, CreateView):
    """
    Представление регистрации на сайте с формой регистрации
    """
    form_class = UserRegisterForm
    success_url = reverse_lazy('home')
    template_name = 'accounts/user_register.html'
    success_message = 'Вы успешно зарегистрировались. Можете войти на сайт!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация на сайте'
        return context
    
class UserLoginView(SuccessMessageMixin, LoginView):
    """
    Авторизация на сайте
    """
    form_class = UserLoginForm
    template_name = 'accounts/user_login.html'
    next_page = 'home'
    success_message = 'Добро пожаловать на сайт!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация на сайте'
        return context

class UserLogoutView(LogoutView):
    """
    Выход с сайта
    """
    next_page = 'home'