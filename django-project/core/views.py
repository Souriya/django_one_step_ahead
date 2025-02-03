from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt

from . import forms
from . import models
import custom_apps.abis_meeting.models as MeetingModels

def home(request):
    context = {
        'title': 'ABIS Business Matching',
        'form': forms.LoginForm,
    }

    template = 'home.html'
    return render(request, template, context)

@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            user = authenticate(
                request, username=form_data['email'], password=form_data['phone']
                )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('core:user_dashboard')
                else:
                    return redirect('core:login_fail')
            else:
                return redirect('core:login_fail')
    else:
        return redirect('core:home')


def login_fail(request):

    context = {
        'title': 'Not Found !',
    }
    template = 'login_fail.html'
    return render(request, template, context)


@login_required
def user_dashboard(request):

    user = request.user
    #user = models.User.objects.get(username='ttt@tt.com') # for testing purpose
    request_pending_in = MeetingModels.Schedule.objects.filter(
                            Q(destination_id=user.id) & Q(request_status=1))
    request_pending_out = MeetingModels.Schedule.objects.filter(
                            Q(source_id=user.id) & Q(request_status=1))
    request_accepted_in = MeetingModels.Schedule.objects.filter(
                            Q(destination_id=user.id) & Q(request_status=2))
    request_accepted_out = MeetingModels.Schedule.objects.filter(
                            Q(source_id=user.id) & Q(request_status=2))
    request_declined_in = MeetingModels.Schedule.objects.filter(
                            Q(destination_id=user.id) & Q(request_status=3))
    request_declined_out = MeetingModels.Schedule.objects.filter(
                            Q(source_id=user.id) & Q(request_status=3))

    context = {
        'title': 'Dashboard',
        'user': user,
        'request_pending_in': request_pending_in,
        'request_pending_out': request_pending_out,
        'request_accepted_in': request_accepted_in,
        'request_accepted_out': request_accepted_out,
        'request_declined_in': request_declined_in,
        'request_declined_out': request_declined_out,
    }
    template = 'user_dashboard.html'
    return render(request, template, context)


@csrf_exempt
@login_required
def user_register(request):
    if request.method == 'POST':
        form = forms.UserRegistrationForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            new_user = form.save(commit=False)  # create new user object in
            # memory, but not write it to db yet
            new_user.set_password(form_data['password'])
            # set_password() is a method of User model that handle password
            # encryption
            new_user.save()  # if set password successful, write user object
            # to db, .save() is committed by default.
            profile = models.Profile.objects.create(user=new_user)
            profile.phone = form_data['phone']
            profile.nation = form_data['nation']
            profile.position = form_data['position']
            profile.org = form_data['org']
            profile.save()

            # create a profile with 1-to-1 relationship for new user
        form2 = forms.UserRegistrationForm()
        template = 'user_register.html'
        return render(request, template, {'form': form2, 'message': 'Success'})
    else:
        form = forms.UserRegistrationForm()
        template = 'user_register.html'
    return render(request, template, {'form': form})


@login_required
def user_list(request):

    users_list = models.User.objects.filter(Q(is_active=True) & Q(is_staff=False))

    paginator = Paginator(users_list, 25)
    page = request.GET.get('page')
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        users = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        users = paginator.page(paginator.num_pages)

    context = {
        'title': 'List of Users',
        'users': users,
        'form': forms.UserSearchForm()
    }
    template = 'user_list.html'
    return render(request, template, context)


@login_required
def user_detail(request, id=None):

    user = get_object_or_404(models.User, id=int(id))
    time_slots = MeetingModels.TimeSlot.objects.all()

    context = {
        'title': 'User Detail',
        'user': user,
        'time_slots': time_slots,
    }
    template = 'user_detail.html'
    return render(request, template, context)


@login_required
def request_meeting(request, destination_id=None, time_slot=None):

    destination_id = int(destination_id)
    time_slot = MeetingModels.TimeSlot.objects.get(id=time_slot)
    locations = MeetingModels.MeetingLocation.objects.all()

    context = {
        'title': 'Request Meeeting',
        'destination_id': destination_id,
        'time_slot': time_slot,
        'locations': locations,
    }
    template = 'request_meeting.html'
    return render(request, template, context)


@csrf_exempt
@login_required
def request_meeting_save(request, destination_id=None, time_slot=None, location=None):

    source = request.user
    destination = models.User.objects.get(id=destination_id)

    meeting_request = MeetingModels.Schedule()
    meeting_request.source_id = source.id
    meeting_request.source_name = source.first_name
    meeting_request.source_last_name = source.last_name
    meeting_request.source_position = source.profile.position
    meeting_request.source_nation = source.profile.nation
    meeting_request.destination_id = destination.id
    meeting_request.destination_name = destination.first_name
    meeting_request.destination_last_name = destination.last_name
    meeting_request.destination_position = destination.profile.position
    meeting_request.destination_nation = destination.profile.nation
    meeting_request.location = MeetingModels.MeetingLocation.objects.get(id=location)
    meeting_request.time_slot = MeetingModels.TimeSlot.objects.get(id=time_slot)
    meeting_request.request_status = MeetingModels.RequestStatus.objects.get(id=1) # 1 pending, 2 accepted, 3 declined

    try:
        meeting_request.save()
        return redirect('core:user_dashboard')
    except:
        # Handle or print exception e
        return redirect('core:user_list')

@csrf_exempt
@login_required
def request_meeting_accept_decline(request, schedule_id=None, request_status_id=None):

    meeting_request = MeetingModels.Schedule.objects.get(id=int(schedule_id))
    request_status = MeetingModels.RequestStatus.objects.get(id=int(request_status_id))
    meeting_request.request_status = request_status # 1 pending, 2 accepted, 3 declined

    try:
        meeting_request.save()
        return redirect('core:user_dashboard')
    except:
        # Handle or print exception e
        return redirect('core:user_list')

@login_required
def user_search(request):

    users_list = None
    if request.method == 'GET':
        form = forms.UserSearchForm(request.GET)

        if form.is_valid():
            form_data = form.cleaned_data

            if form_data['options'] == '1':
                users_list = models.User.objects.filter(
                    Q(first_name__icontains=form_data['search']) |
                    Q(last_name__icontains=form_data['search'])).exclude(is_staff=True)
            elif form_data['options'] == '2':
                users_list = models.User.objects.get(email=form_data['search']).exclude(is_staff=True)
            elif form_data['options'] == '3':
                users_list = models.User.objects.filter(profile__nation__icontains=form_data['search']).exclude(is_staff=True)
            elif form_data['options'] == '4':
                users_list = models.User.objects.filter(profile__position__icontains=form_data['search']).exclude(is_staff=True)
            elif form_data['options'] == '5':
                users_list = models.User.objects.filter(profile__org__icontains=form_data['search']).exclude(is_staff=True)
            elif form_data['options'] == '6':
                users_list = models.User.objects.filter(profile__phone__icontains=form_data['search']).exclude(is_staff=True)

    if users_list is not None:
        paginator = Paginator(users_list, 25)
        page = request.GET.get('page')
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
        template = 'user_list.html'
    else:
        users = user_list
        template = 'user_not_found.html'

    context = {
        'title': 'User Not Found',
        'users': users,
        'form': forms.UserSearchForm()
    }
    return render(request, template, context)
