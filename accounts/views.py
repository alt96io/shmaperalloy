from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm, MemberCreationForm, MemberChangeForm

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            messages.success(request, ('Account created for %s' % email))
            return redirect('report:dashboard_creator')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

