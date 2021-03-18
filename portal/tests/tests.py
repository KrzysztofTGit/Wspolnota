import pytest
from django.test import Client
from portal.models import Profile, Notice, Message, Poll, Vote


# links
@pytest.mark.django_db
def test_links_not_logged(message, notice, poll):
    n = Notice.objects.last()
    m = Message.objects.last()
    p = Poll.objects.last()
    links_not_allowed = ('/', '/logout/', '/account/', '/messages/', '/messages/add/', '/messages/sent/',
                         f'/messages/delete/{m.pk}/', '/notices/', '/notices/add/', f'/notices/delete/{n.pk}/',
                         '/polls/', f'/polls/{p.pk}/', '/polls/add/', f'/polls/delete/{p.pk}/'
                         )
    links_allowed = ('/login/', '/signup/')
    c = Client()

    for link in links_not_allowed:
        response = c.get(link)
        assert response.status_code == 302

    for link in links_allowed:
        response = c.get(link)
        assert response.status_code == 200


@pytest.mark.django_db
def test_links_user_logged(message, user_profile, notice, poll):
    n = Notice.objects.last()
    m = Message.objects.last()
    p = Poll.objects.last()
    links_allowed = ('/account/', '/messages/', '/notices/', '/notices/add/', f'/notices/delete/{n.pk}/', '/polls/',
                     f'/polls/{p.pk}/'
                     )
    links_not_allowed = ('/messages/add/', '/messages/sent/', '/polls/add/', f'/polls/delete/{p.pk}/',
                         f'/messages/delete/{m.pk}/'
                         )

    c = Client()
    c.login(username=user_profile.user.username, password='abc123')

    for link in links_not_allowed:
        response = c.get(link)
        assert response.status_code == 403
    for link in links_allowed:
        response = c.get(link)
        assert response.status_code == 200


@pytest.mark.django_db
def test_links_superuser_logged(message, superuser, notice, poll):
    n = Notice.objects.last()
    m = Message.objects.last()
    p = Poll.objects.last()
    links_allowed = ('/', '/account/', '/messages/', '/messages/add/', '/messages/sent/',
                     f'/messages/delete/{m.pk}/', '/notices/', '/notices/add/', f'/notices/delete/{n.pk}/',
                     '/polls/', f'/polls/{p.pk}/', '/polls/add/', f'/polls/delete/{p.pk}/'
                     )

    c = Client()
    c.login(username=superuser.user.username, password='abc123')

    for link in links_allowed:
        response = c.get(link)
        assert response.status_code == 200


# signup success
@pytest.mark.django_db
def test_signup():
    profiles_before = Profile.objects.count()
    new_profile = {
        'username': "Uzytkownik",
        'password': "abc123",
        'first_name': "aaa",
        'last_name': "bbb",
        'email': "aaa@gmail.com",
        'number': 10,
        'building': "B"
    }
    c = Client()
    response = c.post("/signup/", new_profile)
    assert response.status_code == 302
    assert Profile.objects.count() == profiles_before + 1


# signup fail - user exists
@pytest.mark.django_db
def test_signup_fail1(user_profile):
    profiles_before = Profile.objects.count()
    new_profile = {
        'username': "Uzytkownik",
        'password': "abc123",
        'first_name': "aaa",
        'last_name': "bbb",
        'email': "aaa@gmail.com",
        'number': 10,
        'building': "B"
    }
    c = Client()
    response = c.post("/signup/", new_profile)
    assert response.status_code == 200
    assert Profile.objects.count() == profiles_before


# signup fail - wrong email
@pytest.mark.django_db
def test_signup_fail2():
    profiles_before = Profile.objects.count()
    new_profile = {
        'username': "Uzytkownik",
        'password': "abc123",
        'first_name': "aaa",
        'last_name': "bbb",
        'email': "aaagmail.com",
        'number': 10,
        'building': "B"
    }
    c = Client()
    response = c.post("/signup/", new_profile)
    assert response.status_code == 200
    assert Profile.objects.count() == profiles_before


# signup fail - missing field
@pytest.mark.django_db
def test_signup_fail3():
    profiles_before = Profile.objects.count()
    new_profile = {
        'username': "Uzytkownik",
        'password': "abc123",
        'last_name': "bbb",
        'email': "aaa@gmail.com",
        'number': 10,
        'building': "B"
    }
    c = Client()
    response = c.post("/signup/", new_profile)
    assert response.status_code == 200
    assert Profile.objects.count() == profiles_before


# login success
@pytest.mark.django_db
def test_login(user):
    login_data = {
        'login': user.username,
        'password': 'tymczasowe',
    }
    c = Client()
    response = c.post("/login/", login_data)
    assert response.status_code == 302


# login fail - wrong password
@pytest.mark.django_db
def test_login_fail1(user):
    login_data = {
        'login': user.username,
        'password': 'tymczasow',
    }
    c = Client()
    response = c.post("/login/", login_data)
    assert response.status_code == 200


# login fail - no login
@pytest.mark.django_db
def test_login_fail2(user):
    login_data = {
        'password': 'tymczasowe',
    }
    c = Client()
    response = c.post("/login/", login_data)
    assert response.status_code == 200


# logout
@pytest.mark.django_db
def test_logout(user_profile):
    c = Client()
    c.login(username=user_profile.user.username, password='abc123')

    response = c.get('/logout/')
    assert response.status_code == 302


# form notice
@pytest.mark.django_db
def test_add_notice(user_profile):
    notices_before = Notice.objects.count()
    new_notice = {
        'topic': "Chętnie pomogę",
        'content': "Dzień dobry! Chętnie pomogę starszym osobom w zakupach lub drobnych pracach domowych. Mariusz",
        'author': user_profile.pk
    }
    c = Client()
    c.login(username=user_profile.user.username, password='abc123')
    response = c.post("/notices/add/", new_notice)
    assert response.status_code == 302
    assert Notice.objects.count() == notices_before + 1


# form message
@pytest.mark.django_db
def test_add_message(superuser, user_profile):
    messages_before = Message.objects.count()
    new_message = {
        'topic': "Usunięcie wraku",
        'content': "Proszę o usunięcie wraku samochodu z osiedla! Wyciekają z niego płyny eksploatacyjne",
        'recipient': user_profile.pk,
    }
    c = Client()
    c.login(username=superuser.user.username, password='abc123')
    response = c.post("/messages/add/", new_message)
    assert response.status_code == 302
    assert Message.objects.count() == messages_before + 1


# form poll
@pytest.mark.django_db
def test_add_poll(superuser):
    polls_before = Poll.objects.count()
    new_poll = {
        'name': "Uchwała nr 01/2021",
        'description': "Głosowanie nad uchwałą w sprawie przeniesienia wiaty śmietnikowej.",
        'question': "Czy jest Pan/Pani za przyjęciem uchwały nr 01/2021?"
    }
    c = Client()
    c.login(username=superuser.user.username, password='abc123')
    response = c.post("/polls/add/", new_poll)
    assert response.status_code == 302
    assert Poll.objects.count() == polls_before + 1


# form vote
@pytest.mark.django_db
def test_add_vote(user_profile, poll):
    votes_before = Vote.objects.count()
    new_vote = {
        # 'poll': poll.pk,
        'vote': 'Za'
    }
    c = Client()
    c.login(username=user_profile.user.username, password='abc123')
    response = c.post(f"/polls/{poll.pk}/", new_vote)
    assert response.status_code == 302
    assert Vote.objects.count() == votes_before + 1


# delete message success
@pytest.mark.django_db
def test_delete_message(superuser, message):
    messages_before = Message.objects.count()
    delete = {
        'submit': 'Tak'
    }
    c = Client()
    c.login(username=superuser.user.username, password='abc123')
    response = c.post(f"/messages/delete/{message.pk}/", delete)
    assert response.status_code == 302
    assert Message.objects.count() == messages_before - 1


# delete message fail
@pytest.mark.django_db
def test_delete_message_fail(user_profile, message):
    messages_before = Message.objects.count()
    delete = {
        'submit': 'Tak'
    }
    c = Client()
    c.login(username=user_profile.user.username, password='abc123')
    response = c.post(f"/messages/delete/{message.pk}/", delete)
    assert response.status_code == 403
    assert Message.objects.count() == messages_before


# delete notice success
@pytest.mark.django_db
def test_delete_notice(user_profile, notice):
    notices_before = Notice.objects.count()
    delete = {
        'submit': 'Tak'
    }
    c = Client()
    c.login(username=user_profile.user.username, password='abc123')
    response = c.post(f"/notices/delete/{notice.pk}/", delete)
    assert response.status_code == 302
    assert Notice.objects.count() == notices_before - 1


# delete notice fail
@pytest.mark.django_db
def test_delete_notice_fail(user_profile_2, notice):
    notices_before = Notice.objects.count()
    delete = {
        'submit': 'Tak'
    }
    c = Client()
    c.login(username=user_profile_2.user.username, password='abc123')
    response = c.post(f"/notices/delete/{notice.pk}/", delete)
    assert response.status_code == 302
    assert Notice.objects.count() == notices_before


# delete poll success
@pytest.mark.django_db
def test_delete_poll(superuser, poll):
    polls_before = Poll.objects.count()
    delete = {
        'submit': 'Tak'
    }
    c = Client()
    c.login(username=superuser.user.username, password='abc123')
    response = c.post(f"/polls/delete/{poll.pk}/", delete)
    assert response.status_code == 302
    assert Poll.objects.count() == polls_before - 1


# delete poll fail
@pytest.mark.django_db
def test_delete_poll_fail(user_profile, poll):
    polls_before = Poll.objects.count()
    delete = {
        'submit': 'Tak'
    }
    c = Client()
    c.login(username=user_profile.user.username, password='abc123')
    response = c.post(f"/polls/delete/{poll.pk}/", delete)
    assert response.status_code == 403
    assert Poll.objects.count() == polls_before
