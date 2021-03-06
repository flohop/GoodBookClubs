from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, ProfileEditForm, UserEditForm
from account.models import Profile


def dashboard(request):
    return render(request,
                  'account/dashboard.html', {'section': "dashboard"})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
                user_form.cleaned_data['password'])
            # Save the user object
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'account/register.html',
                  {'user_form': user_form})


@login_required
def edit_profile(request):
    user = request.user
    profile = request.user.user_profile
    values_saved = False
    if request.method == "POST":
        user_form = UserEditForm(instance=user, data=request.POST)
        profile_form = ProfileEditForm(instance=profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            values_saved = True
    else:
        user_form = UserEditForm(initial={'first_name': user.first_name,
                                          'last_name': user.last_name, 'email': user.email})
        profile_form = ProfileEditForm(initial={'profile_description': profile.profile_description,
                                                'profile_picture': profile.profile_picture,
                                                })

    return render(request,
                  'account/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'values_saved': values_saved,
                   'section': 'profile'})


def about(request):
    return render(request, 'account/about.html',
                  {'section': 'about'})

def test(request):
    return render(request, 'account/test.html', {})
