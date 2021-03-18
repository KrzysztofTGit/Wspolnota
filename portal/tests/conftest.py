import pytest
from portal.models import Profile, User, Appartment, Notice, Message, Poll


@pytest.fixture
def user():
    user = User.objects.create_user('testowy', password='tymczasowe')
    return user


@pytest.fixture
def superuser():
    user = User.objects.create_superuser(
        username="Admin",
        first_name="Admin",
        last_name="Admin",
        password="abc123",
        email="admin@gmail.com"
    )
    # p = Permission.objects.get(codename='add_message')
    # user.user_permissions.add(p)
    appartment = Appartment.objects.create(building="B", number=21)
    profile = Profile.objects.create(user=user, appartment=appartment)

    return profile


@pytest.fixture
def user_profile():
    user = User.objects.create_user(
        username="Uzytkownik",
        first_name="aaa",
        last_name="bbb",
        password="abc123",
        email="aaa@gmail.com"
    )
    app = Appartment.objects.create(building="A", number=47)
    profile = Profile.objects.create(user=user, appartment=app)

    return profile


@pytest.fixture
def user_profile_2():
    user = User.objects.create_user(
        username="Uzytkownik2",
        first_name="aaa",
        last_name="bbb",
        password="abc123",
        email="aaa2@gmail.com"
    )
    app = Appartment.objects.create(building="B", number=1)
    profile = Profile.objects.create(user=user, appartment=app)

    return profile


@pytest.fixture
def notice(user_profile):
    notice = Notice.objects.create(
        topic="Głośna muzyka z mieszkania 12",
        content="Bardzo proszę mieszkańców mieszkania nr 12 o ściszenie muzyki!",
        author=user_profile
    )
    return notice


@pytest.fixture
def message(superuser, user_profile):
    message = Message.objects.create(
        topic="Usunięcie wraku",
        content="Proszę o usunięcie wraku samochodu z osiedla! Wyciekają z niego płyny eksploatacyjne",
        author=superuser,
        recipient=user_profile
    )
    return message


@pytest.fixture
def poll():
    poll = Poll.objects.create(
        name="Uchwała nr 01/2021",
        description="Głosowanie nad uchwałą w sprawie przeniesienia wiaty śmietnikowej.",
        question="Czy jest Pan/Pani za przyjęciem uchwały nr 01/2021?"
    )
    return poll
