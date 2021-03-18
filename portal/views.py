from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View

from Final_Project.settings import LOGIN_URL
from portal.forms import SignupForm, LoginForm, NoticeForm, MessageForm, PollForm, VoteForm
from portal.models import Profile, Appartment, Notice, Message, Poll, Vote


# region MAIN SCREEN
class IndexView(LoginRequiredMixin, View):
    login_url = LOGIN_URL

    def get(self, request):
        user = request.user
        profile = Profile.objects.get(user=user)
        last_notice = Notice.objects.last()
        user_messages = Message.objects.filter(recipient=profile)
        last_message = user_messages.last()
        poll = Poll.objects.all()
        if Poll.objects.all():
            poll = Poll.objects.order_by('-pk')[0]
        ctx = {"notice": last_notice, "message": last_message, "poll": poll}
        return render(request, "index.html", ctx)


# endregion


# region USER
class LoginView(View):

    def get(self, request):
        form = LoginForm()
        return render(request, "login.html", {'form': form, 'error': ''})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['login'], password=form.cleaned_data['password'])
            if user:
                login(request, user)
                return redirect('/')
            else:
                return render(request, 'login.html', {'form': form, 'error': 'Użytkownik nie został znaleziony!'})
        else:
            return render(request, 'login.html', {'form': form})


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('/')


class SignupView(View):

    def get(self, request):
        form = SignupForm()
        return render(request, "signup.html", {'form': form})

    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            User.objects.create_user(
                username=form.cleaned_data['username'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email']
            )
            Appartment.objects.create(
                building=form.cleaned_data['building'],
                number=form.cleaned_data['number']
            )
            Profile.objects.create(
                user=User.objects.get(
                    email=form.cleaned_data['email']
                ),
                appartment=Appartment.objects.get(
                    building=form.cleaned_data['building'],
                    number=form.cleaned_data['number']
                )
            )
            return redirect('/login/')
        else:
            return render(request, "signup.html", {'form': form})


class AccountView(LoginRequiredMixin, View):
    login_url = LOGIN_URL

    def get(self, request):
        user = request.user
        profile = Profile.objects.get(user=user)
        return render(request, "account.html", {"profile": profile})


# endregion


# region MESSAGES
class AddMessageView(PermissionRequiredMixin, View):
    permission_required = 'portal.add_message'
    login_url = LOGIN_URL

    def get(self, request):
        form = MessageForm()
        return render(request, "add_message.html", {'form': form})

    def post(self, request):
        form = MessageForm(request.POST)

        if form.is_valid():
            print(form.cleaned_data['recipient'])
            if form.cleaned_data['recipient'] is None:
                for profile in Profile.objects.all():
                    Message.objects.create(
                        topic=form.cleaned_data['topic'],
                        content=form.cleaned_data['content'],
                        author=Profile.objects.get(user=request.user),
                        recipient=profile
                    )
            else:
                Message.objects.create(
                    topic=form.cleaned_data['topic'],
                    content=form.cleaned_data['content'],
                    author=Profile.objects.get(user=request.user),
                    recipient=form.cleaned_data['recipient']
                )
            return redirect('/messages/')
        else:
            return render(request, "add_message.html", {'form': form})


class MessagesView(LoginRequiredMixin, View):
    login_url = LOGIN_URL

    def get(self, request):
        user = request.user
        profile = Profile.objects.get(user=user)
        messages = Message.objects.filter(recipient=profile)
        return render(request, "message.html", {'messages': messages})


class SentMessagesView(PermissionRequiredMixin, View):
    permission_required = 'portal.view_message'
    login_url = LOGIN_URL

    def get(self, request):
        user = request.user
        profile = Profile.objects.get(user=user)
        messages = Message.objects.filter(author=profile)
        return render(request, "sent_messages.html", {'messages': messages})


class DeleteMessageView(PermissionRequiredMixin, View):
    permission_required = 'portal.delete_message'
    login_url = LOGIN_URL

    def get(self, request, id):
        message = Message.objects.get(pk=id)
        user = request.user
        profile = Profile.objects.get(user=user)
        if message.author == profile or user.is_superuser:
            return render(request, "delete_message.html", {'message': message, 'profile': profile})
        return redirect('/messages/')

    def post(self, request, id):
        option = request.POST.get('submit')
        message = Message.objects.get(pk=id)
        if option == "Tak":
            message.delete()
        return redirect('/messages/')

# endregion


# region NOTICES
class AddNoticeView(LoginRequiredMixin, View):
    login_url = LOGIN_URL

    def get(self, request):
        form = NoticeForm()
        return render(request, "add_notice.html", {'form': form})

    def post(self, request):
        form = NoticeForm(request.POST)
        if form.is_valid():
            Notice.objects.create(
                topic=form.cleaned_data['topic'],
                content=form.cleaned_data['content'],
                author=Profile.objects.get(user=request.user)
            )
            return redirect('/notices/')
        else:
            return render(request, "add_notice.html", {'form': form})


class NoticesView(LoginRequiredMixin, View):
    login_url = LOGIN_URL

    def get(self, request):
        notices = Notice.objects.all()
        return render(request, "notices.html", {'notices': notices})


class DeleteNoticeView(LoginRequiredMixin, View):
    login_url = LOGIN_URL

    def get(self, request, id):
        notice = Notice.objects.get(pk=id)
        user = request.user
        profile = Profile.objects.get(user=user)
        if notice.author == profile or user.is_superuser:
            return render(request, "delete_notice.html", {'notice': notice, 'profile': profile})
        return redirect('/notices/')

    def post(self, request, id):
        user = request.user
        profile = Profile.objects.get(user=user)
        option = request.POST.get('submit')
        notice = Notice.objects.get(pk=id)
        if notice.author == profile or user.is_superuser:
            if option == "Tak":
                notice.delete()
        return redirect('/notices/')

# endregion


# region POLLS
class AddPollView(PermissionRequiredMixin, View):
    permission_required = 'portal.add_poll'
    login_url = LOGIN_URL

    def get(self, request):
        form = PollForm()
        return render(request, "add_poll.html", {'form': form})

    def post(self, request):
        form = PollForm(request.POST)
        if form.is_valid():
            Poll.objects.create(
                name=form.cleaned_data['name'],
                description=form.cleaned_data['description'],
                question=form.cleaned_data['question']
            )
            return redirect('/polls/')
        else:
            return render(request, "add_poll.html", {'form': form})


class PollsListView(LoginRequiredMixin, View):
    login_url = LOGIN_URL

    def get(self, request):
        user = request.user
        profile = Profile.objects.get(user=user)

        polls = Poll.objects.all()
        votes = Vote.objects.filter(profile=profile)
        for poll in Poll.objects.all():
            poll.votes_for = Vote.objects.filter(poll=poll, chosen_option="Za").count()
            poll.votes_against = Vote.objects.filter(poll=poll, chosen_option="Przeciw").count()
            poll.votes_pass = Vote.objects.filter(poll=poll, chosen_option="Wstrzymaj").count()
            poll.save()
        return render(request, "polls_list.html", {'polls': polls, 'votes': votes, 'profile': profile})


class PollView(LoginRequiredMixin, View):
    login_url = LOGIN_URL

    def get(self, request, id):
        user = request.user
        profile = Profile.objects.get(user=user)
        poll = Poll.objects.get(pk=id)
        form = VoteForm()
        try:
            percentage_for = int(float(poll.votes_for) / (float(poll.votes_for) + float(poll.votes_against)) * 100)
        except ZeroDivisionError:
            percentage_for = "Brak głosów"
        if Vote.objects.filter(profile=profile, poll=poll).exists():
            already_voted = True
        else:
            already_voted = False
        ctx = {'poll': poll, 'form': form, 'already_voted': already_voted, 'percentage_for': percentage_for}
        return render(request, "poll.html", ctx)

    def post(self, request, id):
        form = VoteForm(request.POST)
        if form.is_valid():
            Vote.objects.create(
                profile=Profile.objects.get(user=request.user),
                poll=Poll.objects.get(pk=id),
                chosen_option=form.cleaned_data['vote']
            )

            return redirect('/polls/')
        else:
            return render(request, "poll.html", {'form': form})


class DeletePollView(PermissionRequiredMixin, View):
    permission_required = 'portal.delete_poll'
    login_url = LOGIN_URL

    def get(self, request, id):
        poll = Poll.objects.get(pk=id)
        user = request.user
        profile = Profile.objects.get(user=user)
        return render(request, "delete_poll.html", {'poll': poll, 'profile': profile})

    def post(self, request, id):
        option = request.POST.get('submit')
        poll = Poll.objects.get(pk=id)
        if option == "Tak":
            poll.delete()
        return redirect('/polls/')
# endregion
