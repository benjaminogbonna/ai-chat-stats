import os
import shutil
import secrets
import string
import json
import pytz
import random
import numpy as np
from collections import Counter
from django.conf import settings
from django.utils.text import slugify
from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime, timezone, timedelta
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .helper_functions import unzip_data, clac_convo_times
# from . import generate_heatmap
from .models import User
from .forms import RegistrationForm, LoginForm, DataUploadForm

# Generate random strings
def string_gen(x=15):
    key = ''.join(secrets.choice(string.ascii_lowercase + string.digits) for i in range(x))
    return key


def index(request):
    return render(request, 'main/index.html')

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def leaderboard(request):
    object_list = User.objects.filter(total_convs__gt=0).order_by('-total_convs')
    paginator = Paginator(object_list, 1)
    page = request.GET.get('page')
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        users = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last of results
        users = paginator.page(paginator.num_pages)
    context = {
        'object_list': object_list,
        'users': users,
    }
    return render(request, 'main/leaderboard.html', context)

def view_user_profile(request, slug):
    user_ = get_object_or_404(User, slug=slug)
    ltz = settings.TIME_ZONE
    year=datetime.now().year
    if user_.data:
        data = user_.data
        with open(f'{data}', 'r') as f:
                convs = json.load(f)
        convo_times = []
        for conv in convs:
            # Given Unix timestamp
            unix_timestamp = conv['create_time']
            # Convert to UTC datetime
            utc_datetime = datetime.fromtimestamp(unix_timestamp, tz=timezone.utc)
            # Convert UTC datetime to local timezone
            pt_datetime = utc_datetime.astimezone(pytz.timezone(ltz))
            convo_times.append(pt_datetime)
        just_dates = [convo.date() for convo in convo_times if convo.year == year]
        date_counts = Counter(just_dates)
        # Create a full year date range for the calendar
        start_date = datetime(year, 1, 1).date()
        end_date = datetime(year, 12, 31).date()
        total_days = (end_date - start_date).days + 1
        date_range = [start_date + timedelta(days=i) for i in range(total_days)]

        # Prepare data for plotting
        user_years = sorted(list(set(convo.year for convo in convo_times)), reverse=True)
        data = []
        for date in date_range:
            week = ((date - start_date).days + start_date.weekday()) // 7
            day_of_week = date.weekday()
            count = date_counts.get(date, 0)
            data.append((week, day_of_week, count))
        context = {
            'user_': user_,
            'user_years': user_years,
            'data': json.dumps(data)
        }
    return render(request, 'main/view_user_profile.html', context)


def view_user_profile_year(request, slug, year=datetime.now().year):
    user_ = get_object_or_404(User, slug=slug)
    ltz = settings.TIME_ZONE
    if user_.data:
        data = user_.data
        with open(f'{data}', 'r') as f:
                convs = json.load(f)
        convo_times = []
        for conv in convs:
            # Given Unix timestamp
            unix_timestamp = conv['create_time']
            # Convert to UTC datetime
            utc_datetime = datetime.fromtimestamp(unix_timestamp, tz=timezone.utc)
            # Convert UTC datetime to local timezone
            pt_datetime = utc_datetime.astimezone(pytz.timezone(ltz))
            convo_times.append(pt_datetime)
        just_dates = [convo.date() for convo in convo_times if convo.year == year]
        date_counts = Counter(just_dates)
        # Create a full year date range for the calendar
        start_date = datetime(year, 1, 1).date()
        end_date = datetime(year, 12, 31).date()
        total_days = (end_date - start_date).days + 1
        date_range = [start_date + timedelta(days=i) for i in range(total_days)]

        # Prepare data for plotting
        user_years = sorted(list(set(convo.year for convo in convo_times)), reverse=True)
        data = []
        for date in date_range:
            week = ((date - start_date).days + start_date.weekday()) // 7
            day_of_week = date.weekday()
            count = date_counts.get(date, 0)
            data.append((week, day_of_week, count))
        context = {
            'user_': user_,
            'user_years': user_years,
            'data': json.dumps(data),
        }

    return render(request, 'main/view_user_profile.html', context)


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_profile(request, slug):
    user = request.user
    ltz = settings.TIME_ZONE
    year=datetime.now().year
    if user.data:
        data = user.data
        with open(f'{data}', 'r') as f:
                convs = json.load(f)
        convo_times = []
        for conv in convs:
            # Given Unix timestamp
            unix_timestamp = conv['create_time']
            # Convert to UTC datetime
            utc_datetime = datetime.fromtimestamp(unix_timestamp, tz=timezone.utc)
            # Convert UTC datetime to local timezone
            pt_datetime = utc_datetime.astimezone(pytz.timezone(ltz))
            convo_times.append(pt_datetime)
        just_dates = [convo.date() for convo in convo_times if convo.year == year]
        date_counts = Counter(just_dates)
        # Create a full year date range for the calendar
        start_date = datetime(year, 1, 1).date()
        end_date = datetime(year, 12, 31).date()
        total_days = (end_date - start_date).days + 1
        date_range = [start_date + timedelta(days=i) for i in range(total_days)]

        # Prepare data for plotting
        user_years = sorted(list(set(convo.year for convo in convo_times)), reverse=True)
        data = []
        for date in date_range:
            week = ((date - start_date).days + start_date.weekday()) // 7
            day_of_week = date.weekday()
            count = date_counts.get(date, 0)
            data.append((week, day_of_week, count))
        context = {
            'user': user,
            'user_years': user_years,
            'data': json.dumps(data)
        }
    return render(request, 'main/user_profile.html', context)


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def profile_settings(request):
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
                if data.name.endswith('.zip') or data.content_type == 'application/zip':
                    unzip_data(data, tmp_fldr)
                    file = f'{tmp_fldr}/conversations.json'
                    new_file_name = f'{string_gen()}.json'
                    renamed_file = os.path.join(f'{media_dir}/data/', new_file_name)
                    try:
                        shutil.move(file, renamed_file)
                        user.data = renamed_file
                        convo_times = clac_convo_times(renamed_file, settings.TIME_ZONE)
                        user.total_convs = sum(Counter([convo.date() for convo in convo_times]).values())
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
        return redirect('main:view_user_profile', slug=request.user.slug)
    else:
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                new_user = form.save(commit=False)
                new_user.slug = slugify(new_user.username)
                new_user.save()
                login(request, new_user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('main:view_user_profile', slug=new_user.slug)
        else:
            form = RegistrationForm()
        return render(request, 'registration/signup.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('main:view_user_profile', slug=request.user.slug)
    else:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(request, username=username, password=password)
                if user:
                    login(request, user)
                    return redirect('main:view_user_profile', slug=user.slug)
        else:
            form = LoginForm()
        return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('main:login')

