from typing import List
from datetime import datetime


class User:
    disabled_at: datetime | None
    email: str
    id: str
    inserted_at: datetime
    last_signed_in_at: datetime | None
    last_signed_in_method: datetime | None
    role: str = "unprivileged"
    updated_at: datetime

    password: str | None = None
    password_confirmation: str | None = None

    def __init__(self, *args, **kwargs) -> None:
        """
        Initializes a new instance of the User class from dict.

        :param args: Positional arguments to pass to the constructor.
        :type args: tuple

        :param kwargs: Keyword arguments to pass to the constructor.
        :type kwargs: dict
        """
        self.__dict__.update(kwargs)

    @staticmethod
    def list(client) -> List['User']:
        """
        Receives a list of all users.

        :param client: The client to use for the request.
        :type client: FZClient

        :raises Exception: If the server returns an error.

        :return: A list of all users.
        :rtype: List[User]
        """
        return [
            User(**user_json)
            for user_json in client.__get__("/users")["data"]
        ]

    @staticmethod
    def get(client, *args, **kwargs) -> 'User':
        """
        Retrieves a user with the specified ID using the provided client.

        :param client: The client to use for the request.
        :type client: FZClient

        :param id: The ID of the user to retrieve.
        :type id: str

        :raises Exception: If the ID is missing or if the server returns an error.

        :return: The user with the specified ID.
        :rtype: User
        """
        user_id = kwargs.get("id")

        if not user_id:
            raise Exception("id key is required")

        server_reply = client.__get__(f"/users/{user_id}")
        data = server_reply.get("data")

        if not data:
            raise Exception(server_reply)

        return User(**data)

    def create(self, client) -> 'User':
        """
        Creates a new user.

        :param client: The client to use for the request.
        :type client: FZClient

        :raises Exception: If the server returns an error.

        :return: The newly created user.
        :rtype: User
        """
        data = {
            "user": {
                "email": self.email,
                "role": self.role
            }
        }
        if self.password:
            data["user"]["password"] = self.password
            data["user"]["password_confirmation"] = self.password

        server_reply = client.__post__("/users", data)
        server_data = server_reply.get("data")

        if not server_data:
            raise Exception(server_reply)

        return User(**server_data)

    def update(self, client) -> 'User':
        """
        Update current user with new data and return the updated user.

        :param client: The client to use for the request.
        :type client: FZClient

        :raises Exception: If the server returns an error.

        :return: The updated user.
        :rtype: User
        """
        old_user_version = User.get(client, id=self.id)
        # get diff between old and new user and add it to the dict
        data = {"user": {}}
        # allowed attributes
        allowed_attributes = ["email", "role", "password", "password_confirmation"]
        for attribute in allowed_attributes:
            if getattr(self, attribute) != getattr(old_user_version, attribute):
                data["user"][attribute] = getattr(self, attribute)

        server_reply = client.__patch__(f"/users/{self.id}", data)
        server_data = server_reply.get("data")

        if not server_data:
            raise Exception(server_reply)

        return User(**server_data)

    def delete(self, client):
        """
        Delete current user.

        :param client: The client to use for the request.
        :type client: FZClient
        """
        return client.__delete__(f"/users/{self.id}")
