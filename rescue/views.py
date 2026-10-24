from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_POST

from .models import RescueRequest
from .forms import RescueRequestForm
from accounts.models import Profile


def _is_mechanic(user):
    return hasattr(user, "profile") and user.profile.role == "mechanic"


def _is_customer(user):
    return hasattr(user, "profile") and user.profile.role == "customer"


# ==========================================
# CREATE RESCUE REQUEST
# ==========================================

@login_required
def create_request(request):

    if not _is_customer(request.user):
        return redirect("mechanic_dashboard")

    if request.method == "POST":

        form = RescueRequestForm(request.POST)

        if form.is_valid():

            rescue = form.save(commit=False)

            rescue.customer = request.user

            rescue.save()

            messages.success(
                request,
                "Rescue request submitted. Waiting for a mechanic."
            )

            return redirect("customer_dashboard")

    else:

        form = RescueRequestForm()

    return render(
        request,
        "rescue/create_request.html",
        {
            "form": form
        }
    )


# ==========================================
# MECHANIC REQUESTS
# ==========================================

@login_required
def mechanic_requests(request):

    if not _is_mechanic(request.user):
        return redirect("customer_dashboard")

    return redirect("mechanic_dashboard")


# ==========================================
# ACCEPT REQUEST
# ==========================================

@login_required
def accept_request(request, request_id):

    if not _is_mechanic(request.user):
        return redirect("customer_dashboard")

    if not request.user.profile.available:
        messages.warning(
            request,
            "Go online before accepting jobs."
        )
        return redirect("mechanic_dashboard")

    rescue_request = get_object_or_404(
        RescueRequest,
        id=request_id,
        status="pending"
    )

    rescue_request.mechanic = request.user
    rescue_request.status = "accepted"

    rescue_request.save()

    messages.success(request, "Job accepted.")

    return redirect("mechanic_dashboard")


# ==========================================
# START TRIP
# ==========================================

@login_required
def start_trip(request, request_id):

    if not _is_mechanic(request.user):
        return redirect("customer_dashboard")

    rescue_request = get_object_or_404(
        RescueRequest,
        id=request_id,
        mechanic=request.user
    )

    rescue_request.status = "on_the_way"

    rescue_request.save()

    return redirect("mechanic_dashboard")


# ==========================================
# MARK ARRIVED
# ==========================================

@login_required
def mark_arrived(request, request_id):

    if not _is_mechanic(request.user):
        return redirect("customer_dashboard")

    rescue_request = get_object_or_404(
        RescueRequest,
        id=request_id,
        mechanic=request.user
    )

    rescue_request.status = "arrived"

    rescue_request.save()

    return redirect("mechanic_dashboard")


# ==========================================
# COMPLETE JOB
# ==========================================

@login_required
def complete_job(request, request_id):

    if not _is_mechanic(request.user):
        return redirect("customer_dashboard")

    rescue_request = get_object_or_404(
        RescueRequest,
        id=request_id,
        mechanic=request.user
    )

    rescue_request.status = "completed"

    rescue_request.save()

    return redirect("mechanic_dashboard")


# ==========================================
# CUSTOMER TRACKING PAGE
# ==========================================

@login_required
def tracking(request, request_id):

    rescue_request = get_object_or_404(
        RescueRequest,
        id=request_id
    )

    is_customer = rescue_request.customer_id == request.user.id
    is_assigned_mechanic = (
        rescue_request.mechanic_id == request.user.id
    )

    if not (is_customer or is_assigned_mechanic):
        return HttpResponseForbidden("You cannot view this tracking page.")

    return render(
        request,
        "rescue/tracking.html",
        {
            "rescue_request": rescue_request
        }
    )


# ==========================================
# UPDATE MECHANIC LOCATION
# ==========================================

# ==========================================
# UPDATE MECHANIC LOCATION
# ==========================================

@login_required
@require_POST
def update_location(request, request_id):

    if not _is_mechanic(request.user):
        return JsonResponse(
            {"success": False, "message": "Not allowed."},
            status=403
        )

    rescue_request = get_object_or_404(
        RescueRequest,
        id=request_id,
        mechanic=request.user
    )

    try:

        latitude = float(request.POST.get("latitude"))
        longitude = float(request.POST.get("longitude"))

    except (TypeError, ValueError):

        return JsonResponse(
            {
                "success": False,
                "message": "Invalid location."
            },
            status=400
        )

    # Get the mechanic's profile
    profile = get_object_or_404(
        Profile,
        user=request.user
    )

    # Save the mechanic's current GPS location
    profile.latitude = latitude
    profile.longitude = longitude

    profile.save(
        update_fields=[
            "latitude",
            "longitude"
        ]
    )

    # Also keep the location on this rescue request
    rescue_request.mechanic_latitude = latitude
    rescue_request.mechanic_longitude = longitude

    rescue_request.save(
        update_fields=[
            "mechanic_latitude",
            "mechanic_longitude",
            "updated_at"
        ]
    )

    return JsonResponse(
        {
            "success": True,
            "latitude": latitude,
            "longitude": longitude
        }
    )
    
    


# ==========================================
# GET MECHANIC LOCATION
# ==========================================

@login_required
def mechanic_location(request, request_id):

    rescue_request = get_object_or_404(
        RescueRequest,
        id=request_id
    )

    is_customer = rescue_request.customer_id == request.user.id
    is_assigned_mechanic = (
        rescue_request.mechanic_id == request.user.id
    )

    if not (is_customer or is_assigned_mechanic):
        return JsonResponse(
            {"success": False, "message": "Not allowed."},
            status=403
        )

    latitude = None
    longitude = None

    # Get the mechanic's latest location
    if rescue_request.mechanic:

        profile = Profile.objects.filter(
            user=rescue_request.mechanic
        ).first()

        if profile:

            latitude = profile.latitude
            longitude = profile.longitude

    return JsonResponse(
        {
            "success": True,
            "latitude": latitude,
            "longitude": longitude,
            "status": rescue_request.status
        }
    )


# ==========================================
# CANCEL REQUEST
# ==========================================

@login_required
def cancel_request(request, request_id):

    if not _is_customer(request.user):
        return redirect("mechanic_dashboard")

    rescue_request = get_object_or_404(
        RescueRequest,
        id=request_id,
        customer=request.user
    )

    if rescue_request.status == "pending":

        rescue_request.status = "cancelled"

        rescue_request.save()

    return redirect("customer_dashboard")