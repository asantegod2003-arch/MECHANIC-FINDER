from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Profile
from .forms import SignUpForm

from rescue.models import RescueRequest




# ==========================
# HOME PAGE
# ==========================

def home(request):

    if request.user.is_authenticated:

        try:

            role = request.user.profile.role

            if role == "customer":
                return redirect("customer_dashboard")

            elif role == "mechanic":
                return redirect("mechanic_dashboard")


        except Profile.DoesNotExist:

            pass


    return render(
        request,
        "accounts/home.html"
    )




# ==========================
# SIGN UP
# ==========================

def signup(request):

    if request.method == "POST":

        form = SignUpForm(request.POST)


        if form.is_valid():

            user = form.save(commit=False)


            password = form.cleaned_data["password"]


            user.set_password(password)


            user.save()



            Profile.objects.create(

                user=user,

                role=form.cleaned_data["role"]

            )



            messages.success(

                request,

                "Account created successfully! Please login."

            )



            return redirect("login")



    else:

        form = SignUpForm()



    return render(

        request,

        "accounts/signup.html",

        {

            "form": form

        }

    )





# ==========================
# LOGIN
# ==========================

def login_view(request):


    if request.method == "POST":


        username = request.POST.get("username")

        password = request.POST.get("password")



        user = authenticate(

            request,

            username=username,

            password=password

        )



        if user is not None:


            login(request, user)



            try:


                role = user.profile.role



                if role == "customer":

                    return redirect(
                        "customer_dashboard"
                    )



                elif role == "mechanic":

                    return redirect(
                        "mechanic_dashboard"
                    )



            except Profile.DoesNotExist:


                messages.error(

                    request,

                    "User profile not found."

                )



        else:


            messages.error(

                request,

                "Invalid username or password."

            )



    return render(

        request,

        "accounts/login.html"

    )






# ==========================
# LOGOUT
# ==========================

def logout_view(request):


    logout(request)



    messages.success(

        request,

        "You have been logged out successfully."

    )



    return redirect("home")

# ==========================
# CUSTOMER DASHBOARD
# ==========================

@login_required
def customer_dashboard(request):

    # Only customers can access this dashboard

    if request.user.profile.role != "customer":

        return redirect("mechanic_dashboard")



    requests = RescueRequest.objects.filter(

        customer=request.user

    ).order_by("-created_at")



    return render(

        request,

        "dashboard/customer_dashboard.html",

        {
            "requests": requests
        }

    )





# ==========================
# MECHANIC DASHBOARD
# ==========================

@login_required
def mechanic_dashboard(request):


    # Only mechanics can access this dashboard

    if request.user.profile.role != "mechanic":

        return redirect("customer_dashboard")

    profile = request.user.profile

    if request.method == "POST" and "toggle_available" in request.POST:
        profile.available = not profile.available
        profile.save(update_fields=["available"])
        return redirect("mechanic_dashboard")

    # Requests waiting for mechanics

    available_requests = RescueRequest.objects.none()

    if profile.available:
        available_requests = RescueRequest.objects.filter(
            status="pending"
        ).order_by("-created_at")






    # Jobs accepted by this mechanic

    my_jobs = RescueRequest.objects.filter(

        mechanic=request.user

    ).order_by("-created_at")






    return render(

        request,

        "dashboard/mechanic_dashboard.html",

        {
            "available_requests": available_requests,
            "my_jobs": my_jobs,
            "profile": profile,
        }

    )



