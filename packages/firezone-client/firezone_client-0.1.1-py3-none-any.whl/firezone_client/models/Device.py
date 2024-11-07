from datetime import datetime
from typing import List

from firezone_client.models import User

class Device:

    # required fields
    user_id: str | User
    public_key: str

    # optional fields
    allowed_ips: list
    description: str
    dns: list
    endpoint: str
    ipv4: str
    ipv6: str
    mtu: int
    name: str
    persistent_keepalive: int
    preshared_key: str
    use_default_allowed_ips: bool
    use_default_dns: bool
    use_default_endpoint: bool
    use_default_mtu: bool
    use_default_persistent_keepalive: bool

    # read-only fields
    id: str
    server_public_key: str
    inserted_at: datetime
    updated_at: datetime
    remote_ip: str | None
    latest_handshake: datetime | None
    rx_bytes: int | None
    tx_bytes: int | None

    # minimal required fields for creation or update
    required_fields = [ "user_id", "public_key" ]

    # optional fields for creation or update
    optional_fields = [ "allowed_ips", "description", "dns", "endpoint",
                        "ipv4", "ipv6", "mtu", "name", "persistent_keepalive",
                        "preshared_key", "use_default_allowed_ips", "use_default_dns",
                        "use_default_endpoint", "use_default_mtu",
                        "use_default_persistent_keepalive", "user_id" ]

    def __init__(self, *args, **kwargs) -> None:
        """
        Initializes a new instance of the Device class from dict.

        :param args: Positional arguments to pass to the constructor.
        :type args: tuple

        :param kwargs: Keyword arguments to pass to the constructor.
        :type kwargs: dict
        """
        self.__dict__.update(kwargs)

    @staticmethod
    def list(client) -> List['Device']:
        """
        Retrieves a list of all device using the provided client.

        :param client: The client to use for the request.
        :type client: FZClient

        :raises Exception: If the server returns an error.

        :return: A list of all devices.
        :rtype: List[Device]
        """
        return [
            Device(**device_json)
            for device_json in client.__get__("/devices")["data"]
        ]

    @staticmethod
    def get(client, *args, **kwargs) -> 'Device':
        """
        Retrieves a device with the specified ID using the provided client.

        :param client: The client to use for the request.
        :type client: FZClient

        :param id: The ID of the device to retrieve.
        :type id: str

        :raises Exception: If the ID is missing or if the server returns an error.

        :return: The device with the specified ID.
        :rtype: Device
        """
        device_id = kwargs.get("id")

        if device_id is None:
            raise Exception("id is required")

        server_reply = client.__get__(f"/devices/{device_id}")

        if server_reply.get("errors"):
            raise Exception(server_reply.get("errors"))

        return Device(**server_reply.get("data"))

    def create(self, client) -> 'Device':
        """
        Creates a new device using the provided data with client.

        :param client: The client to use for the request.
        :type client: FZClient

        :raises Exception: If any of the required fields are missing or if the server returns an error.

        :return: The newly created device.
        :rtype: Device
        """
        data = {"device": {}}

        for field in self.required_fields:
            if getattr(self, field) is None:
                raise Exception(f"{field} is required")
            data["device"][field] = getattr(self, field)

        for field in self.optional_fields:
            try:
                if getattr(self, field) is not None:
                    data["device"][field] = getattr(self, field)
            except AttributeError:
                pass

        # patch user to user_id in payload
        if isinstance(self.user_id, User):
            data["device"]["user_id"] = self.user_id.id

        server_reply = client.__post__("/devices", data)
        if server_reply.get("errors"):
            raise Exception(server_reply.get("errors"))

        return Device(**server_reply.get("data"))

    def update(self, client) -> 'Device':
        """
        Updates the current device with new data using the provided client.

        :param client: The client to use for the request.
        :type client: FZClient

        :raises Exception: If any of the required fields are missing or if the server returns an error.

        :return: The updated device.
        :rtype: Device
        """
        raise NotImplementedError("Update is not implemented yet")
        data = {"device": {}}

        old_device_version = Device.get(client, id=self.id)

        for field in self.optional_fields + self.required_fields:
            if getattr(self, field) != getattr(old_device_version, field):
                data["device"][field] = getattr(self, field)

        if isinstance(self.user_id, User):
            data["device"]["user_id"] = self.user_id.id

        server_reply = client.__patch__(f"/devices/{self.id}", data)
        if server_reply.get("errors"):
            raise Exception(server_reply.get("errors"))

        return Device(**server_reply.get("data"))

    def delete(self, client) -> None:
        """
        Deletes the current device using the provided client.

        :param client: The client to use for the request.
        :type client: FZClient
        """
        return client.__delete__(f"/devices/{self.id}")
