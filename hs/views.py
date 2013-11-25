from datetime import date
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from hs.forms import RegistrationForm
from hs.models import IDType, UserProfile

# Create your views here.


def index(request):
    data = {"registration_form": RegistrationForm(initial={"idType": IDType})}

    return render_to_response("index.html", data, context_instance=RequestContext(request))


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            username = data["username"]
            email = data["email"]
            password = data["password"]
            first_name = data["first_name"]
            middle_name = data["middle_name"]
            last_name = data["last_name"]
            company_name = data["company_name"]
            birthday = data["birthday"]
            age = date.today().year - birthday.year

            phone_number = data["phone_number"]
            city = data["city"]
            country = data["country"]

            if User.objects.filter(Q(username=username)).exists():
                messages.error(request,"There's a snake in my boot!" + "<br /> That username is already taken.")
                return HttpResponseRedirect("/")
            if User.objects.filter(Q(email=email)).exists():
                messages.error(request,"There's a snake in my boot!" + "<br /> That email was already registered.")
                return HttpResponseRedirect("/")

            user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, middle_name=middle_name)
            user.is_active = False  # will send this user an email where he must confirm the password to activate

            user_profile = UserProfile(user=user, username=username, email=email, password=password, )

            user_profile.save()

            login(request, user)
            return HttpResponseRedirect("/")
        else:
            errors = form.errors
            messages.error(request,"There's a snake in my boot!" + "<br /> Please correct the highlighted fields.")
            return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/")