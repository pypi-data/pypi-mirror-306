import os
from abc import ABC, abstractmethod

import pyotp
import requests
from requests import ConnectionError, HTTPError
from retry import retry
from t_object import ThoughtfulObject

from t_vault.utils import exceptions
from t_vault.utils.bw_port import BW_PORT


class Attachment(ThoughtfulObject):
    """A class representing an attachment with a name, item ID, and URL."""

    name: str
    item_id: str
    url: str


class VaultItem(ThoughtfulObject, ABC):
    """A class representing a vault item."""

    name: str = ""
    item_id: str = ""
    totp_key: str | None = None
    attachments: list[Attachment] = []
    fields: dict[str, str | None] = {}
    url: str | None = None
    url_list: list[str] = []
    username: str | None = None
    password: str | None = None

    @abstractmethod
    def get_attachment(self, attachment_name: str, file_path: str) -> str:
        """Get an attachment by name.

        Args:
            attachment_name: The name of the attachment to retrieve.
            file_path: The path to save the attachment to.

        Returns:
            str: The path to the downloaded attachment.
        """
        raise NotImplementedError()

    @property
    def otp_now(self) -> str | None:
        """Returns the current TOTP code generated using the TOTP key associated with the instance.

        Returns:
            str: The current TOTP code, or None if no TOTP key is set.
        """
        return pyotp.TOTP(self.totp_key).now() if self.totp_key else None

    def __getitem__(self, key):
        """Get an item by key.

        Args:
            key: The key to retrieve the item.

        Returns:
            The item corresponding to the key, or the username if key is "login".
        """
        if key == "login":
            return self.username
        try:
            return self.fields[key]
        except KeyError:
            return getattr(self, key)


class BitWardenItem(VaultItem):
    """A class representing a Bitwarden vault item."""

    collection_id_list: list[str] = []
    folder_id: str | None = None
    notes: str | None = None

    def get_attachment(self, attachment_name: str, file_path: str | None = None) -> str:
        """Get an attachment by name.

        Args:
            attachment_name: The name of the attachment to retrieve.
            file_path: Path to download the attachment.

        Returns:
            str: The path to the downloaded attachment.
        """
        if file_path is None:
            file_path = os.path.join(os.getcwd(), attachment_name)
        attachment = next((attachment for attachment in self.attachments if attachment.name == attachment_name), None)
        if attachment is None:
            raise exceptions.VaultAttatchmentNotFoundError(f"Attachment '{attachment_name}' not found.")

        self._get_attachment_request(attachment, file_path)
        return file_path

    @retry((ConnectionError, HTTPError), tries=7, delay=1, backoff=1)
    def _get_attachment_request(self, attachment: Attachment, file_path: str):
        with requests.get(
            f"http://localhost:{BW_PORT}/object/attachment/{attachment.item_id}",
            params={"id": attachment.item_id, "itemid": self.item_id},
            stream=True,
        ) as r:
            r.raise_for_status()
            with open(file_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
