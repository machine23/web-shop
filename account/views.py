from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render

from .forms import ProfileForm, UserForm


def register(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        profile_form = ProfileForm(request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            cd = user_form.cleaned_data
            user = user_form.save()
            user.refresh_from_db()
            profile_form = ProfileForm(request.POST, instance=user.profile, files=request.FILES)
            profile_form.full_clean()
            profile_form.save()
            user = authenticate(username=user.username, password=cd.get('password1'))
            if user is not None:
                login(request, user)
                return redirect('shop:index')
    else:
        user_form = UserCreationForm()
        profile_form = ProfileForm()
    return render(request, 'account/register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


@login_required
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            print(" ***************************** profile ********************************")
            user_form.save()
            profile_form.save()
            return redirect('account:update_profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'account/profile.html', context)
