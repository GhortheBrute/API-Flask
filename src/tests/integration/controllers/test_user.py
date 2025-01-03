from http import HTTPStatus

from app import User, Role, db


def test_get_user_success(client):
    role = Role(name='admin')
    db.session.add(role)
    db.session.commit()

    user = User(username="jesus", password="test", role_id=role.id)
    db.session.add(user)
    db.session.commit()

    response = client.get(f'/users/{user.id}')
    assert response.status_code == HTTPStatus.OK
    assert response.json == {'id': user.id, 'username': user.username}


def test_get_user_not_found(client):
    role = Role(name='admin')
    db.session.add(role)
    db.session.commit()

    user_id = 1

    response = client.get(f'/users/{user_id}')
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_create_user(client, access_token):
    role_id = db.session.execute(db.select(Role.id).where(Role.name == 'admin')).scalar()
    payload = {'username': 'user2', 'password': 'user2', 'role_id': role_id}

    response = client.post('/users/', json=payload, headers={"Authorization": f"Bearer {access_token}"})

    assert response.status_code == HTTPStatus.CREATED
    assert response.json == {"message": "User successfully created"}


def test_list_users_success(client):
    try:
        role = Role(name='admin')
        db.session.add(role)
        db.session.commit()
        # print("Role ID:", role.id)  # Debug print

        user = User(username="jesus", password="test", role_id=role.id)
        db.session.add(user)
        db.session.commit()
        # print("User ID:", user.id)  # Debug print

        response = client.post("/auth/login", json={"username": user.username, "password": user.password})
        # print("Login response status:", response.status_code)  # Debug print
        # print("Login response JSON:", response.json)  # Debug print

        access_token = response.json['access_token']
        # breakpoint()

        response = client.get('/users/', headers={"Authorization": f"Bearer {access_token}"})
        # print("Users list response status:", response.status_code)  # Debug print
        # print("Users list response JSON:", response.json)  # Debug print

        assert response.status_code == HTTPStatus.OK
        assert response.json == {
            "users": [
                {
                    'id': user.id,
                    'username': user.username,
                    'role': {
                        'id': role.id,
                        'name': role.name,
                    },
                }
            ]
        }
    except Exception as e:
        print(f"Test failed: {str(e)}")
        raise
