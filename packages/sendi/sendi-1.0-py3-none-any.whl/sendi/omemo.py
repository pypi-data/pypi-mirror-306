# based on https://github.com/Syndace/slixmpp-omemo/blob/main/examples/echo_client.py

import json
import logging
from pathlib import Path
from typing import Any

from omemo.storage import Just, Maybe, Nothing, Storage
from omemo.types import DeviceInformation, JSONType
from slixmpp_omemo import XEP_0384, TrustLevel

log = logging.getLogger(__name__)


class StorageImpl(Storage):
    """
    Example storage implementation that stores all data in a single JSON file.
    """

    def __init__(self, path: Path) -> None:
        super().__init__()
        self.path = path

        self.__data: dict[str, JSONType] = {}
        try:
            with open(self.path, encoding="utf8") as f:
                self.__data = json.load(f)
        except Exception:  # noqa: S110
            pass

    async def _load(self, key: str) -> Maybe[JSONType]:
        if key in self.__data:
            return Just(self.__data[key])

        return Nothing()

    async def _store(self, key: str, value: JSONType) -> None:
        self.__data[key] = value
        with open(self.path, "w", encoding="utf8") as f:  # noqa: ASYNC230
            json.dump(self.__data, f)

    async def _delete(self, key: str) -> None:
        self.__data.pop(key, None)
        with open(self.path, "w", encoding="utf8") as f:  # noqa: ASYNC230
            json.dump(self.__data, f)


class XEP_0384Impl(XEP_0384):  # pylint: disable=invalid-name
    """
    Example implementation of the OMEMO plugin for Slixmpp.
    """

    STORAGE_PATH: Path

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # noqa: ANN401
        super().__init__(*args, **kwargs)

        if not isinstance(self.STORAGE_PATH, Path):
            raise TypeError()
        self.storage_path: Path = self.STORAGE_PATH
        # Just the type definition here
        self.__storage: Storage

    def plugin_init(self) -> None:
        self.__storage = StorageImpl(self.storage_path)
        super().plugin_init()

    @property
    def storage(self) -> Storage:
        return self.__storage

    @property
    def _btbv_enabled(self) -> bool:
        return True

    async def _devices_blindly_trusted(
        self, blindly_trusted: frozenset[DeviceInformation], identifier: str | None
    ) -> None:
        log.info(f"[{identifier}] Devices trusted blindly: {blindly_trusted}")

    async def _prompt_manual_trust(
        self, manually_trusted: frozenset[DeviceInformation], identifier: str | None
    ) -> None:
        # Since BTBV is enabled and we don't do any manual trust adjustments in the example, this method
        # should never be called. All devices should be automatically trusted blindly by BTBV.

        # To show how a full implementation could look like, the following code will prompt for a trust
        # decision using `input`:
        session_mananger = await self.get_session_manager()

        for device in manually_trusted:
            while True:
                answer = input(f"[{identifier}] Trust the following device? (yes/no) {device}")
                if answer in {"yes", "no"}:
                    await session_mananger.set_trust(
                        device.bare_jid,
                        device.identity_key,
                        TrustLevel.TRUSTED.value
                        if answer == "yes"
                        else TrustLevel.DISTRUSTED.value,
                    )
                    break
                print("Please answer yes or no.")
