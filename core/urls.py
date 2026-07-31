"""URL configuration for core.

    OWNER: BE track — GRP12 writes the real version of this file.

This is a stub. It exists so that `manage.py runserver` starts on a fresh
clone; without it, `config/urls.py` fails to import and nobody in the class
can run anything. It answers exactly one route.

Your job is to replace it with the eight endpoints on the BE track page:

    POST   /api/auth/login/            obtain access + refresh tokens
    POST   /api/auth/refresh/          exchange a refresh token
    GET    /api/auth/me/               the current student, from request.user
    POST   /api/attendance/mark/       multipart: photo, lat, lng, accuracy
    GET    /api/attendance/today/      has this student marked today?
    GET    /api/attendance/my-records/ this student's history
    GET    /api/admin/overview/?date=  staff only
    GET    /api/health/                already done, below

Two things to get right while you are here, both of which the reference
implementation got wrong:

  * Identity comes from `request.user`, never from a `user_id` that the
    client sent you. If the caller can name the user, so can an attacker.
  * `/api/auth/me/` is five lines and it is the whole point. A token you
    cannot resolve back to a user is not authentication.
"""

from django.urls import path

from . import views

urlpatterns = [
    path("api/health/", views.health, name="health"),
]
