import pytest


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(username='TestUser', password='1234567')


@pytest.fixture
def user_2(django_user_model):
    return django_user_model.objects.create_user(username='TestUser2', password='1234567')


@pytest.fixture
def another_user(django_user_model):
    return django_user_model.objects.create_user(username='TestUserAnother', password='1234567')
