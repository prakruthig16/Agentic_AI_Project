
from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),

    path("chat/", views.chat_page, name="chat"),

    path("api/chat/", views.chat_api, name="chat_api"),

    path("history/", views.history_page, name="history"),
]
