import asyncio
import logging
import tempfile
from pathlib import Path
from typing import Any

import oldmemo
import twomemo
from slixmpp import ClientXMPP
from slixmpp.stanza import Message

from sendi.common import SecurityLevel


class XMPPReceiveMsgBot(ClientXMPP):
    def __init__(
        self,
        jid: str,
        password: str,
        number_message_to_wait: int,
        timeout: int,
        security_level: SecurityLevel,
        logger_name: str = "sendi-receiver-unknown",
    ) -> None:
        ClientXMPP.__init__(self, jid, password)
        self.timeout = timeout
        self.received_messages: list[Any] = []
        self.unencrypted_messages: list[Any] = []
        self.encrypted_messages: list[Any] = []
        self.number_message_to_wait = number_message_to_wait
        self.connected_event = asyncio.Event()
        self.disconnected_event = asyncio.Event()
        self.logger = logging.getLogger(logger_name)

        self.security_level = security_level

        self.register_plugin("xep_0060")
        self.register_plugin("xep_0199")  # XMPP Ping
        self.register_plugin("xep_0198")  # Stream management
        self.register_plugin("xep_0380")  # Explicit Message Encryption
        from slixmpp.plugins import register_plugin

        from sendi.omemo import XEP_0384Impl

        self.omemo_configuration_path = Path(tempfile.mkdtemp()).joinpath("storage_path.json")
        self.logger.info(f"temp_storage_path for {jid} is {self.omemo_configuration_path}")
        if self.security_level == SecurityLevel.ENCRYPTED:
            XEP_0384Impl.STORAGE_PATH = self.omemo_configuration_path
            register_plugin(XEP_0384Impl)
            self.register_plugin(
                "xep_0384",  # OMEMO Encryption
                module=XEP_0384Impl,
            )
            self.add_event_handler("omemo_initialized", self.omemo_initalized)
            self.omemo_initialized_event = asyncio.Event()

        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.message)
        self.add_event_handler("connection_failed", self.connection_failed)
        self.add_event_handler("disconnected", self.on_disconnect)

    async def session_start(self, event: dict) -> None:  # noqa: ARG002
        self.send_presence()
        self.get_roster()

        loop_nb = 0
        self.logger.info(f"{self.boundjid.bare} is ready")
        if self.security_level == SecurityLevel.ENCRYPTED:
            await self.omemo_initialized_event.wait()
        self.connected_event.set()
        while len(self.received_messages) < self.number_message_to_wait:
            if loop_nb > self.timeout:
                self.logger.info(
                    f"{self.boundjid.bare} of {self.timeout}s exceeded, without getting all messages"
                )
                break
            await asyncio.sleep(1)
            loop_nb += 1

        # Clean up temporary OMEMO data before disconnecting
        if self.security_level == SecurityLevel.ENCRYPTED:
            session_manager = await self["xep_0384"].get_session_manager()
            try:
                await session_manager.purge_backend(twomemo.twomemo.NAMESPACE)
            except Exception as e:
                self.logger.warning("Twomemo cleanup failed", exc_info=e)
            try:
                await session_manager.purge_backend(oldmemo.oldmemo.NAMESPACE)
            except Exception as e:
                self.logger.warning("Oldmemo cleanup failed", exc_info=e)

        self.disconnect()
    async def connection_failed(self, event: str) -> None:
        print(f"connection failed: {event}")
        self.disconnect()


    async def omemo_initalized(self, event: Any) -> None:  #noqa: ARG002,ANN401
        self.omemo_initialized_event.set()


    async def message(self, msg: Message) -> None:
        if self.security_level == SecurityLevel.ENCRYPTED:
            await self.message_encrypted(msg)
        else:
            self.logger.info(f"{self.boundjid.bare}: received 1 ✉  unencrypted message")
            await self.message_unencrypted(msg)
        self.received_messages.append(msg)

    async def message_unencrypted(self, msg: Message) -> None:
        self.unencrypted_messages.append(msg)

    async def message_encrypted(self, msg: Message) -> None:
        namespace = self["xep_0384"].is_encrypted(msg)
        if namespace is None:
            self.logger.warning(
                f"{self.boundjid.bare}: received 1 ✉  unencrypted message but context allow OMEMO"
            )
            await self.message_unencrypted(msg)
        else:
            try:
                message, device_information = await self["xep_0384"].decrypt_message(msg)
                self.logger.info(f"{self.boundjid.bare}: received 1 🔐 encrypted message")
                self.unencrypted_messages.append(message)
            except Exception:
                self.logger.exception(
                    f"{self.boundjid.bare}: ❌ failed to decrypt message received"
                )
            finally:
                self.encrypted_messages.append(msg)

    def on_disconnect(self, reason: str) -> None:  # noqa: ARG002
        self.logger.info(f"{self.boundjid.bare}: remove {self.omemo_configuration_path}")
        self.omemo_configuration_path.unlink(missing_ok=True)
        self.disconnected_event.set()
