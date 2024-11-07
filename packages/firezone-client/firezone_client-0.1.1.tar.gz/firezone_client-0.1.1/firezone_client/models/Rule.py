
from datetime import datetime
from typing import List

from firezone_client.models import User

class Rule:

    # required fields
    user_id: str | User
    destination: str

    # this field need to be both set or equal to None
    port_range: str | None = None
    port_type: str | None = None

    # optional fields
    action: str  # default is drop if not specified

    # read-only fields
    id: str
    inserted_at: datetime
    updated_at: datetime

    # minimal required fields for creation or update
    required_fields = [ "user_id", "destination" ]

    # optional fields for creation or update
    optional_fields = [ "action" ]

    def __init__(self, *args, **kwargs) -> None:
        """
        Initializes a new instance of the Rule class from dict.

        :param args: Positional arguments to pass to the constructor.
        :type args: tuple

        :param kwargs: Keyword arguments to pass to the constructor.
        :type kwargs: dict
        """
        self.__dict__.update(kwargs)

    @staticmethod
    def list(client) -> List['Rule']:
        """
        List all rules.

        :param client: The client to use for the request.
        :type client: FZClient

        :return: A list of rules.
        :rtype: List[Rule]
        """
        return [
            Rule(**rule_json)
            for rule_json in client.__get__("/rules")["data"]
        ]

    @staticmethod
    def get(client, *args, **kwargs) -> 'Rule':
        rule_id = kwargs.get("id")

        if rule_id is None:
            raise ValueError("id is required")

        server_reply = client.__get__(f"/rules/{rule_id}")

        if server_reply.get("errors"):
            raise Exception(server_reply.get("errors"))

        return Rule(**server_reply.get("data"))

    def create(self, client) -> 'Rule':
        """
        Create a new rule.

        :param client: The client to use for the request.
        :type client: FZClient

        :raises Exception: If the server returns an error or invalid field.

        :return: The created rule.
        :rtype: Rule
        """
        data = {"rule": {}}

        for field in self.required_fields:
            if getattr(self, field) is None:
                raise ValueError(f"{field} is required")
            data["rule"][field] = getattr(self, field)

        if type(self.port_range) is not type(self.port_type):
            raise ValueError("port_range and port_type must be both set or equal to None")

        data["rule"]["port_range"] = self.port_range
        data["rule"]["port_type"] = self.port_type

        for field in self.optional_fields:
            if getattr(self, field) is not None:
                data["rule"][field] = getattr(self, field)

        if isinstance(self.user_id, User):
            data["rule"]["user_id"] = self.user_id.id

        server_reply = client.__post__("/rules", data)

        if server_reply.get("errors"):
            raise Exception(server_reply.get("errors"))

        return Rule(**server_reply.get("data"))

    def update(self, client) -> 'Rule':
        """
        Update the current rule.

        :param client: The client to use for the request.
        :type client: FZClient

        :raises Exception: If the server returns an error or invalid field.

        :return: The updated rule.
        :rtype: Rule
        """
        raise NotImplementedError("This method is not implemented yet")
        data = {"rule": {}}

        old_rule = Rule.get(client, id=self.id)

        for field in self.required_fields + self.optional_fields + ["port_range", "port_type"]:
            data["rule"][field] = getattr(self, field)

        if isinstance(self.user_id, User):
            data["rule"]["user_id"] = self.user_id.id

        server_reply = client.__("PUT", f"/rules/{self.id}", data)

        if server_reply.get("errors"):
            raise Exception(server_reply.get("errors"))

        return Rule(**server_reply.get("data"))

    def delete(self, client) -> None:
        """
        Delete the current rule.

        :param client: The client to use for the request.
        :type client: FZClient
        """
        return client.__delete__(f"/rules/{self.id}")
