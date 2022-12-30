from unittest import mock
from flask import url_for
import pytest
import requests
from celery.exceptions import Retry
from project.users.models import User
from project.users.factories import UserFactory
from project.users.tasks import task_add_subscribe

def test_user_subscribe_view(client, db, monkeypatch, user_factory):
    user = user_factory.build()

    mock_task_add_subscribe_delay = mock.MagicMock(name="task_add_subscribe_delay")
    mock_task_add_subscribe_delay.return_value = mock.MagicMock(task_id='task_id')
    monkeypatch.setattr(task_add_subscribe, 'delay', mock_task_add_subscribe_delay)

    response = client.get(url_for('users.user_subscribe'))
    assert response.status_code == 200

    response = client.post(url_for('users.user_subscribe'),
                           data={'email': user.email,
                                 'username': user.username},
                           )

    assert response.status_code == 200
    assert b'sent task to Celery successfully' in response.data

    # query from the db again
    user = User.query.filter_by(username=user.username).first()
    mock_task_add_subscribe_delay.assert_called_with(
        user.id
    )

def test_post_succeed(db, monkeypatch, user):
    mock_requests_post = mock.MagicMock()
    monkeypatch.setattr(requests, 'post', mock_requests_post)

    task_add_subscribe(user.id)

    mock_requests_post.assert_called_with(
        'https://httpbin.org/delay/5',
        data={'email': user.email}
    )


def test_exception(db, monkeypatch, user):
    mock_requests_post = mock.MagicMock()
    monkeypatch.setattr(requests, 'post', mock_requests_post)

    mock_task_add_subscribe_retry = mock.MagicMock()
    monkeypatch.setattr(task_add_subscribe, 'retry', mock_task_add_subscribe_retry)

    mock_task_add_subscribe_retry.side_effect = Retry()
    mock_requests_post.side_effect = Exception()

    with pytest.raises(Retry):
        task_add_subscribe(user.id)