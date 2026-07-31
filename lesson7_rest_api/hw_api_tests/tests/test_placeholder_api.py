import pytest
import requests

BASE_URL = "https://jsonplaceholder.typicode.com"

def test_get_all_posts():
    response = requests.get(f"{BASE_URL}/posts")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 100

def test_get_single_post():
    post_id=1
    response = requests.get(f"{BASE_URL}/posts/{post_id}")
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == post_id
    assert 'userId' in data
    assert 'title' in data
    assert 'body' in data

@pytest.mark.parametrize("post_id", [1, 2])
def test_get_multiple_posts(post_id):
    response = requests.get(f"{BASE_URL}/posts/{post_id}")
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == post_id

@pytest.mark.parametrize("title,body", [
    ("Test Post 1", "This is test body 1"),
    ("Test Post 2", "This is test body 2"),
    ])
def test_create_post(title, body):
    new_post = {
        "title": title,
        "body": body,
        "userId": 1
    }
    response = requests.post(url=f"{BASE_URL}/posts", json=new_post)
    assert response.status_code == 201
    data = response.json()
    assert data['title'] == title
    assert data['body'] == body
    assert data['userId'] == 1
    assert 'id' in data

def test_update_post():
    post_id = 1
    updated_data = {
        "id": post_id,
        "userId": 1,
        "title": "Updated Title",
        "body": "Updated Body"
    }
    response = requests.put(f"{BASE_URL}/posts/{post_id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data['title'] == 'Updated Title'
    assert data['body'] == 'Updated Body'

def test_delete_post():
    post_id = 1
    response = requests.delete(f"{BASE_URL}/posts/{post_id}")
    assert response.status_code == 200
    response = requests.get(f"{BASE_URL}/posts/{post_id}")
    assert response.status_code == 200