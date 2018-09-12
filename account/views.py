from django.conf import settings
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import redirect, render, reverse

from .forms import ProfileForm, UserForm, UserLoginForm, UserRegistrationForm
from .tokens import account_activation_token


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = ProfileForm(request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            cd = user_form.cleaned_data
            user = user_form.save(commit=False)
            user.is_active = False
            user.save()
            user.refresh_from_db()
            profile_form = ProfileForm(request.POST, instance=user.profile, files=request.FILES)
            profile_form.full_clean()
            profile_form.save()
            if send_verify_email(user):
                print('Activation email sent.')
                return render(request, 'account/email_sent.html')
            else:
                print('Error: activation email didn\'t send')
            return redirect('account:login')
    else:
        user_form = UserRegistrationForm()
        profile_form = ProfileForm()
    return render(request, 'account/register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


def send_verify_email(user):
    verify_link = reverse('account:verify', args=[user.email, account_activation_token.make_token(user)])

    title = f'Подтверждение учетной записи {user.username}'
    message = f'Для подтверждения учетной записи {user.username} \
    на портале {settings.DOMAIN_NAME} перейдите по ссылке: \
    \n{settings.DOMAIN_NAME}{verify_link}'

    print(f'from: {settings.EMAIL_HOST_USER}, to: {user.email}')
    return send_mail(
        title,
        message,
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
    )


def verify(request, email, token):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth.login(request, user)
    return render(request, 'account/verification.html')


@login_required
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
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
