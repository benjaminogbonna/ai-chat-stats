import os
import shutil
import secrets
import string
from django.conf import settings
from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from .helper_functions import unzip_data
# from . import generate_heatmap
from .models import CustomUser
from .forms import RegistrationForm, LoginForm, DataUploadForm

# Generate random strings
def string_gen(x=15):
    key = ''.join(secrets.choice(string.ascii_lowercase + string.digits) for i in range(x))
    return key


def index(request):
    return render(request, 'main/index.html')

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def profile(request):
    if request.method == 'POST':
        form = DataUploadForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            files = request.FILES
            if files:
                data = files.get("data")
                file_path = user.data.path
                media_dir = os.path.join(settings.BASE_DIR, 'media')
                temp_dir = f'temp_{string_gen(x=10)}'
                tmp_fldr = f'{media_dir}/data/{temp_dir}'
                os.makedirs(tmp_fldr, exist_ok=True)

                # Parse the document based on file extension
                if data.name.endswith('.zip'):
                    unzip_data(data, tmp_fldr)
                    file = f'{tmp_fldr}/conversations.json'
                    new_file_name = f'{string_gen()}.json'
                    renamed_file = os.path.join(f'{media_dir}/data/', new_file_name)
                    try:
                        shutil.move(file, renamed_file)
                        user.data = renamed_file
                        user.save()
                    except:
                        pass

            if os.path.exists(tmp_fldr):
                shutil.rmtree(tmp_fldr)
    else:
        form = DataUploadForm()

    context = {
        'name': request.user.username,
        'form': form,
    }
    return render(request, 'main/profile.html', context)


def signup(request):
    if request.user.is_authenticated:
        return redirect('main:profile')
    else:
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect('main:index')
        else:
            form = RegistrationForm()
        return render(request, 'registration/signup.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('main:profile')
    else:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(request, username=username, password=password)
                if user:
                    login(request, user)
                    return redirect('main:profile')
        else:
            form = LoginForm()
        return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('main:login')
