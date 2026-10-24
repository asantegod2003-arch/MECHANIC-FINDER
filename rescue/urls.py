from django.urls import path
from . import views


urlpatterns = [

    # ==========================================
    # CUSTOMER
    # ==========================================

    path(
        "create/",
        views.create_request,
        name="create_request"
    ),

    path(
        "tracking/<int:request_id>/",
        views.tracking,
        name="tracking"
    ),

    path(
        "cancel-request/<int:request_id>/",
        views.cancel_request,
        name="cancel_request"
    ),


    # ==========================================
    # MECHANIC
    # ==========================================

    path(
        "requests/",
        views.mechanic_requests,
        name="mechanic_requests"
    ),

    path(
        "accept/<int:request_id>/",
        views.accept_request,
        name="accept_request"
    ),

    path(
        "start/<int:request_id>/",
        views.start_trip,
        name="start_trip"
    ),

    path(
        "arrived/<int:request_id>/",
        views.mark_arrived,
        name="mark_arrived"
    ),

    path(
        "complete/<int:request_id>/",
        views.complete_job,
        name="complete_job"
    ),


    # ==========================================
    # LIVE LOCATION
    # ==========================================

    path(
        "update-location/<int:request_id>/",
        views.update_location,
        name="update_location"
    ),

    path(
        "tracking/<int:request_id>/location/",
        views.mechanic_location,
        name="mechanic_location"
    ),

]