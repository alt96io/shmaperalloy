from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import RegisterForm, MemberChangeForm, ProfileForm, ProfileChangeForm
from .models import Member, Profile

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            member = form.save()
            email = form.cleaned_data.get('email')
            messages.success(request, ('Your account has been created!  You may now login.'))
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        p_form = ProfileChangeForm(request.POST, request.FILES, instance=request.user.profile)
        if p_form.is_valid():
            p_form.save()
#            p = p_form.save()
#            p.refresh_from_db()
#            p.photo = p_form.cleaned_data.get('photo')
#            p.save()
            messages.success(request, ('Your profile has been updated!'))
            return redirect('profile')
    else:
        p_form = ProfileChangeForm()
#    context = {
#        'p_form': p_form,
#    }

    return render(request, 'accounts/profile.html', {'p_form':p_form})