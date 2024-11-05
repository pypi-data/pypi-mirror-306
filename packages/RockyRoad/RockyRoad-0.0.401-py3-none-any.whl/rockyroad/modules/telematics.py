from .module_imports import key
from uplink import (
    Consumer,
    post,
    patch,
    delete,
    returns,
    headers,
    Body,
    json,
    Query,
)
from uplink import get as http_get


@headers({"Ocp-Apim-Subscription-Key": key})
class Telematics(Consumer):
    """Inteface to Telematics resource for the RockyRoad API."""

    def __init__(self, Resource, *args, **kw):
        self._base_url = Resource._base_url
        super().__init__(base_url=Resource._base_url, *args, **kw)

    @returns.json
    @http_get("machines/telematics")
    def list(
        self,
        uid: Query = None,
        machine_uid: Query = None,
    ):
        """This call will return telematics information for the specified criteria."""

    @returns.json
    @json
    @post("machines/telematics")
    def insert(self, telematics: Body):
        """This call will create telematics information with the specified parameters."""

    @json
    @patch("machines/telematics/{uid}")
    def update(self, uid: str, telematics: Body):
        """This call will update the telematics information with the specified parameters."""

    @delete("machines/telematics/{uid}")
    def delete(self, uid: str):
        """This call will delete the telematics information for the specified uid."""
