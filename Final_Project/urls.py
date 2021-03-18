"""Final_Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from portal.views import (IndexView, LoginView, SignupView, PollsListView, MessagesView, NoticesView, LogoutView,
                          AccountView, AddNoticeView, AddMessageView, AddPollView, PollView, SentMessagesView,
                          DeleteNoticeView, DeleteMessageView, DeletePollView)

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('admin/', admin.site.urls, name="admin"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('signup/', SignupView.as_view(), name="signup"),
    path('account/', AccountView.as_view(), name="account"),

    path('messages/', MessagesView.as_view(), name="messages"),
    path('messages/add/', AddMessageView.as_view(), name="add_message"),
    path('messages/sent/', SentMessagesView.as_view(), name="sent_messages"),
    path('messages/delete/<int:id>/', DeleteMessageView.as_view(), name="delete_message"),

    path('notices/', NoticesView.as_view(), name="notices"),
    path('notices/add/', AddNoticeView.as_view(), name="add_notice"),
    path('notices/delete/<int:id>/', DeleteNoticeView.as_view(), name="delete_notice"),

    path('polls/', PollsListView.as_view(), name="polls_list"),
    path('polls/<int:id>/', PollView.as_view(), name="poll"),
    path('polls/add/', AddPollView.as_view(), name="add_poll"),
    path('polls/delete/<int:id>/', DeletePollView.as_view(), name="delete_poll"),
]
