from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from cars.models import Car
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views import View
from django.utils.decorators import method_decorator
from .models import Order

def register(request):
    if request.method == 'POST':
        register_form = forms.RegistrationForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            messages.success(request, 'Account created successfully')
            return redirect('login')
    else:
        register_form = forms.RegistrationForm()
            
    return render(request, 'user_form.html', {'form': register_form, 'type':'Register'})

class UserLoginView(LoginView):
    template_name = 'user_form.html'
    def get_success_url(self):
        return reverse_lazy('order_history')
    def form_valid(self, form):
        messages.success(self.request, 'Logged in Successfully')
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.success(self.request, 'Logged in informations are incorrect')
        return super().form_invalid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'Login'
        return context

@login_required   
def edit_profile(request):
    if request.method == 'POST':
        profile_form = forms.ChangeUserForm(request.POST, instance = request.user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('order_history')
    else:
        profile_form = forms.ChangeUserForm(instance = request.user)
            
    return render(request, 'user_form.html', {'form': profile_form, 'type':'Edit Profile'})

@login_required
def pass_change(request):
    if request.method == 'POST':
        pass_change_form = PasswordChangeForm(request.user, data=request.POST)
        if pass_change_form.is_valid():
            pass_change_form.save()
            messages.success(request, 'Password updated successfully')
            update_session_auth_hash(request, pass_change_form.user)
            return redirect('order_history')
    else:
        pass_change_form = PasswordChangeForm(user=request.user)
            
    return render(request, 'pass_change.html', {'form': pass_change_form, 'type':'Register'})

@login_required
def user_logout(request):
    messages.success(request, 'Logged out successfully')
    logout(request)
    return redirect('login')

@login_required
def buy_car(request, id):
    try:
        car = Car.objects.get(pk=id)
    except Car.DoesNotExist:
        messages.error(request, 'Car not found or no quantity available.')
        return redirect('home')
    car.quantity -= 1
    car.save()
    Order.objects.create(user=request.user, car=car)
    messages.success(request, 'Car purchased successfully.')
    return redirect('order_history')
   
@method_decorator(login_required, name='dispatch')
class OrderHistoryView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            orders = Order.objects.filter(user=request.user)
            return render(request, 'order_history.html', {'orders': orders})
        return render(request, 'order_history.html', {'orders': None})