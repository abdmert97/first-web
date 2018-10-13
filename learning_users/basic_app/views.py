from django.shortcuts import render
from .forms import UserForm, TeamForm, PlayerForm
from .models import UserInfo

# Extra Imports for the Login and Logout Capabilities
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request,'basic_app/index.html')


@login_required
def user_logout(request):
    # Log out the user.
    logout(request)
    # Return to homepage.
    return HttpResponseRedirect(reverse('index'))

def register(request):

    registered = False

    if request.method == 'POST':

        # Get info from "both" forms
        # It appears as one form to the user on the .html page
        user_form = UserForm(data=request.POST)
        team_form = TeamForm(data=request.POST)
        # Check to see both forms are valid
        if user_form.is_valid() and team_form.is_valid():

            # Save User Form to Database
            user = user_form.save()

            # Hash the password
            user.set_password(user.password)

            # Update with Hashed password
            user.save()

            user_inf = UserInfo(user = user)
            user_inf.save()
            
            team = team_form.save()
            
            team.admin_usr = user_inf
            team.save()
            
            # Registration Successful!
            registered = True

        else:
            # One of the forms was invalid if this else gets called.
            print(user_form.errors)

    else:
        # Was not an HTTP post so we just render the forms as blank.
        user_form = UserForm()
        team_form = TeamForm()

    # This is the render and context dictionary to feed
    # back to the registration.html file page.
    return render(request,'basic_app/registration.html',
                          {'user_form':user_form,
                           'team_form':team_form,
                           'registered':registered})

def user_login(request):

    if request.method == 'POST':
        # First get the username and password supplied
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Django's built-in authentication function:
        user = authenticate(username=username, password=password)

        # If we have a user
        if user:
            #Check it the account is active
            if user.is_active:
                # Log the user in.
                login(request,user)
                # Send the user back to some page.
                # In this case their homepage.
                return HttpResponseRedirect(reverse('index'))
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details supplied.")

    else:
        #Nothing has been provided for username or password.
        return render(request, 'basic_app/login.html', {})


@login_required
def register_team(request):
    user = request.user
    team = (user.usr).Team
    team_members = team.team_members.all()
    player_form = PlayerForm()

    context_dict = {
        'team_members' : team_members,
        'add_pressed' : False,
        'player_form' : player_form,
    }

    if request.method == "POST":
        if request.POST.get("add_submitted"):
            context_dict['add_pressed'] = True
            return render(request, 'basic_app/register_team.html', context=context_dict)
        elif request.POST.get("register_new_member"):
            context_dict['add_pressed'] = False
            player_form = PlayerForm(request.POST)
            curr_player = player_form.save()
            curr_player.team = team
            curr_player.save()
            return render(request, 'basic_app/register_team.html', context=context_dict)
        else:
            player_form = PlayerForm(request.POST)
            if player_form.is_valid():
                curr_player = player_form.save()
                curr_player.team = request.user.usr.Team
                curr_player.save()
                return render(request, 'basic_app/register_team.html', context=context_dict)
            else:
                return HttpResponse('ERROR!')

    return render(request, 'basic_app/register_team.html', context=context_dict)