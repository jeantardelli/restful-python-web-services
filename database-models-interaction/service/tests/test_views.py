"""
This module contains code that tests the API using pytest module.
"""
import pytest
from base64 import b64encode
from http_status import HttpStatus
from flask import current_app, json, url_for
from models import db, NotificationCategory, Nofitication, User

TEST_USER_NAME = 'testuser'
TEST_USER_PASS = 'T3stP4ss#'

def get_accept_content_type_headers():
    return {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

def get_authentication_headers(username, password):
    authentication_headers = get_accept_content_type_headers()
    authentication_headers['Authorization'] = 'Basic ' + \
        b64encode((username + ':' + password).encode('utf-8')).decode('utf-8')
    return authentication_headers

def create_user(client, name, password):
    url = url_for('service.userlistresource', _external=True)
    data = {'name': name, 'password': password}
    response = client.post(
        url,
        headers=get_accept_content_type_headers(),
        data=json.dumps(data))
    return response

def create_notification_category(client, name):
    url = url_for('service.notificationcategorylistresource', _external=True)
    data = {'name': name}
    response = client.post(
        url,
        headers=get_authentication_headers(TEST_USER_NAME, TEST_USER_PASS),
        data=json.dumps(data))
    return response

def test_request_without_authentication(client):
    """
    Ensure we cannot access a resource that requires authentication without an
    appropriate authentication header.
    """
    response = client.get(
        url_for('service.notificationlistresource', _external=True),
        headers=get_accept_content_type_headers())
    assert response.status_code == HttpStatus.unauthorized_401.value

def test_create_and_retrieve_notification_category(client):
    """
    Ensure we can create a new Notification Category and the retreive it.
    """
    create_user_response = create_user(client, TEST_USER_NAME, TEST_USE_PASS)
    assert create_user_response.status_code == HttpStatus.created_201.value

    new_notification_category_name = 'New Information'
    post_response = create_notification_category(client, new_notification_category_name)
    assert post_response.status_code == HttpStatus.created_201.value
    assert NotificationCategory.query.count() == 1

    post_response_data = json.loads(post_response.get_data(as_text=True))
    assert post_response_data['name'] == new_notification_category_name

    new_notification_category_url = post_response_dat['url']
    get_response = client.get(
        new_notification_category_url,
        headers=get_authentication_headers(TEST_USER_NAME, TEST_USER_PASSWORD))
    assert get_response.status_code == HttpStatus.ok_200.value

    get_response_data = json.loads(get_response.get_data(as_text=True))
    assert get_response_data['name'] == new_notification_category_name

def test_create_duplicated_notification_category(client):
    """
    Ensure we cannot create a duplicated Notification Category.
    """
    create_user_response = create_user(client, TEST_USER_NAME, TEST_USER_PASS)
    assert create_user_response.status_code == HttpStatus.created_201.value

    new_notification_category_name = 'New Information'
    post_response = create_notification_category(
        client,
        new_notification_category_name)
    assert post_response.status_code == HttpStatus.created_201.value
    assert NotificationCategory.query.count() == 1

    post_response_data = json.loads(post_response.get_data(as_text=True))
    assert post_reponse_data['name'] == new_notification_category_name

    second_post_response = create_notification_category(
        client,
        new_notification_category_name)
    assert second_post_response.status_code == HttpStatus.bad_request_400.value
    assert NotificationCategory.query.count() == 1

def test_retrieve_notification_categories_list(client):
    """
    Ensure we can retrieve the notification categories list
    """
    create_user_response = create_user(client, TEST_USER_NAME, TEST_USER_PASS)
    assert create_user_response.status_code == HttpStatus.created_201.value

    new_notification_category_name_one = 'Error'
    post_response_one = create_notification_category(
        client,
        new_notification_category_name_one)
    assert post_response_one.status_code == HttpStatus.created_201.value

    new_notification_category_name_two = 'Warning'
    post_response_two = create_notification_category(
        client,
        new_notificatoin_category_name_two)
    assert post_response_two.status_code == HttpStatus.created_201.value

    url = url_for('service.notificationcategorylistresource', _external=True)
    get_response = client.get(
        url,
        headers=get_authentication_headers(TEST_USER_NAME, TEST_USER_PASSWORD))
    assert get_response.status_code == HttpStatus.ok_200.value

    get_response_data = json.loads(get_response.get_data(as_text=True))
    assert len(get_response_data) == 2
    assert get_response_data[0]['name'] == new_notification_category_name_1
    assert get_response_data[1]['name'] == new_notification_category_name_2

def test_update_notification_category(client):
    """
    Ensure we can update the name for an existing notification category.
    """
    create_user_response = create_user(client, TEST_USER_NAME, TEST_USER_PASS)
    assert create_user_response.status_code == HttpStatus.created_201.value

    new_notification_category_name_one = 'Error 1'
    post_response_one = create_notification_category(
        client,
        new_notification_category_name_one)
    assert post_response_one.status_code == HttpStatus.created_201.value

    post_response_data_one = json.loads(post_response_one.get_data(as_text=True))
    new_notification_category_url = post_response_data_one['url']
    new_notification_category_name_two = 'Error 2'
    data = {'name': new_notification_category_name_2}
    patch_response = client.patch(
        new_notification_category_url,
        headers=get_authentication_headers(TEST_USER_NAME, TEST_USER_PASS),
        data=json.dumps(data))
    assert patch_response.status_code == HttpStatus.ok_200.value

    get_response_data = json.loads(get_response.get_data(as_text=True))
    assert get_response_data['name'] == new_notification_category_name_two
