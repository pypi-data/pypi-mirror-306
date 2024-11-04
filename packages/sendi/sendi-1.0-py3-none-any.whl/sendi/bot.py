import asyncio
import contextlib
import os
import ssl
from pathlib import Path

import certifi
import slixmpp
from slixmpp import ClientXMPP
from slixmpp.exceptions import IqTimeout
from slixmpp.features.feature_mechanisms import Failure
from slixmpp.jid import JID
from slixmpp.plugins.xep_0363.http_upload import FileTooBig, HTTPError, UploadServiceNotFound
from slixmpp.stanza import Message, StreamError

from sendi.common import SecurityLevel, sendi_logger

# based on :
# - https://codeberg.org/nicoco/slixmpp/src/branch/pyproject/examples/http_upload.py : MIT
# - https://github.com/Syndace/slixmpp-omemo/blob/main/examples/echo_client.py : AGPL-V3
# - https://github.com/caronc/apprise/tree/v0.9.9/apprise/plugins/NotifyXMPP : MIT


class XMPPSendMsgBot(ClientXMPP):
    def __init__(
        self,
        jid: str,
        password: str,
        host: str = "localhost",
        port: int = 5222,
        security_level: SecurityLevel = SecurityLevel.SIMPLE,
        message_body: str | None = None,
        file_path: Path | None = None,
        targets: list[str] | None = None,
        lang: str | None = None,
        omemo_cache_file_path: Path | None = None,
        clear_omemo_cache: bool = False,
    ) -> None:
        """
        Initialize our SliXmppAdapter object
        """
        self.success = False
        self.host = host
        self.port = port
        self.security_level = security_level
        self.secure = security_level in [SecurityLevel.SIMPLE, SecurityLevel.ENCRYPTED]
        self.verify_certificates = self.secure
        self._jid = jid
        self._password = password or ""
        self.file_path = file_path
        self.body = message_body
        self.targets: list[JID] = [JID(target) for target in targets] if targets else []
        self.disconnect_wait_time = 200
        self.omemo_cache_file_path = omemo_cache_file_path
        if not self.omemo_cache_file_path:
            default_cache_path = Path(
                os.environ.get("XDG_CACHE_HOME") or Path.home().joinpath(".cache")
            ).joinpath("sendi")
            # INFO: we store cache per bare_jid on not per full_jid.
            # Multiple same user connection with same bare_jid will use the same cache.
            # This also prevent issue with "/resource" url considered as subpath in the cache file generation
            self.omemo_cache_file_path = default_cache_path.joinpath(f"{JID(jid).bare}.json")
        parent_cache_dir = self.omemo_cache_file_path.parent
        parent_cache_dir.mkdir(exist_ok=True)
        if clear_omemo_cache:
            self.omemo_cache_file_path.unlink(missing_ok=True)

        self.xep = [
            # xep_0030: Service Discovery
            30,
            # Service Discovery Extensions
            128,
            # xep_0199: XMPP Ping
            199,
            # Stream managment
            198,
            # http upload
            363,
            # OMEMO Media sharing
            454,
            # xhtml-im: needed for http upload
            71,
            # Out of Band Data: needed for http upload
            66,
            # Explicit Message Encryption
            380,
            # Pubsub
            60,
        ]
        self.disconnected_event = asyncio.Event()

        slixmpp.ClientXMPP.__init__(self, self._jid, self._password, lang=lang)
        for xep in self.xep:
            # Load xep entries
            self.register_plugin(f"xep_{xep:04d}")

        if self.security_level == SecurityLevel.ENCRYPTED:
            # Omemo
            from slixmpp.plugins import register_plugin

            from sendi.omemo import XEP_0384Impl

            XEP_0384Impl.STORAGE_PATH = self.omemo_cache_file_path
            register_plugin(XEP_0384Impl)
            self.register_plugin(
                "xep_0384",  # OMEMO Encryption
                module=XEP_0384Impl,
            )
            self.omemo_initialized_event = asyncio.Event()

        if self.secure:
            # Don't even try to use the outdated ssl.PROTOCOL_SSLx
            self.ssl_version = ssl.PROTOCOL_TLSv1

            # If the python version supports it, use highest TLS version
            # automatically
            if hasattr(ssl, "PROTOCOL_TLS"):
                # Use the best version of TLS available to us
                self.ssl_version = ssl.PROTOCOL_TLS
            self.ca_certs = None
            if self.verify_certificates:
                # Set the ca_certs variable for certificate verification
                self.ca_certs = self.get_ca_certificates_locations()
                if self.ca_certs is None:
                    sendi_logger.warn(
                        "XMPP Secure comunication can not be verified; "
                        "no local CA certificate file"
                    )

        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("connection_failed", self.connection_failed)
        self.add_event_handler("failed_all_auth", self.failed_auth)
        self.add_event_handler("stream_error", self.stream_error)
        self.add_event_handler("disconnected", self.on_disconnect)
        self.add_event_handler("omemo_initialized", self.omemo_initialized)

    async def omemo_initialized(self, event: dict) -> None: #noqa: ARG002
        print("omemo initialized")
        self.omemo_initialized_event.set()


    @staticmethod
    def get_ca_certificates_locations() -> list[Path]:
        """
        Return possible locations to root certificate authority (CA) bundles.

        Taken from https://golang.org/src/crypto/x509/root_linux.go
        TODO: Maybe refactor to a general utility function?
        """
        candidates = [
            # Debian/Ubuntu/Gentoo etc.
            "/etc/ssl/certs/ca-certificates.crt",
            # Fedora/RHEL 6
            "/etc/pki/tls/certs/ca-bundle.crt",
            # OpenSUSE
            "/etc/ssl/ca-bundle.pem",
            # OpenELEC
            "/etc/pki/tls/cacert.pem",
            # CentOS/RHEL 7
            "/etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem",
            # macOS Homebrew; brew install ca-certificates
            "/usr/local/etc/ca-certificates/cert.pem",
        ]
        # Certifi provides Mozilla's carefully curated collection of Root
        # Certificates for validating the trustworthiness of SSL certificates
        # while verifying the identity of TLS hosts. It has been extracted from
        # the Requests project.
        with contextlib.suppress(ImportError):
            candidates.append(certifi.where())

        path_certificates = []
        for candidate in candidates:
            path = Path(candidate)
            if path.is_file():
                path_certificates.append(path)
        return path_certificates

    async def connection_failed(self, event: str) -> None:
        sendi_logger.error(f"connection failed: {event}")
        await self.disconnect()

    async def failed_auth(self, event: Failure) -> None:
        """After all auth test. Slixmpp test multiple auth before finding a working one"""
        sendi_logger.error(f"bad auth: {event['text']}")

    async def stream_error(self, event: StreamError) -> None:
        """Stream error case, can occur with policy-violation error from ejabberd-fail2ban module"""
        sendi_logger.error(f"stream error: {event['text']}")

    async def upload(self, filename: Path) -> str | None:
        try:
            match self.security_level:
                case SecurityLevel.ENCRYPTED:
                    upload_file = self["xep_0454"].upload_file
                case _:
                    upload_file = self["xep_0363"].upload_file
            sendi_logger.debug("upload file")
            url = await upload_file(
                filename,
                domain=self.host,
            )
            sendi_logger.debug("file uploaded")
        except UploadServiceNotFound as exc:
            sendi_logger.error(f"Err: UploadServiceNotFound : {exc}")
            return None
        except (FileTooBig, HTTPError) as exc:
            sendi_logger.error(f"Err: {exc}")
            return None
        except IqTimeout:
            sendi_logger.error("Err: Could not send file in time")
            return None
        except Exception as exc:
            sendi_logger.error(f"Err: {exc}")
            return None
        return url

    def create_http_upload_link(self, url: str, target: JID) -> Message:
        message_html = f'<a href="{url}">{url}</a>'
        message = self.make_message(mto=target, mbody=url, mhtml=message_html)
        message["oob"]["url"] = url
        return message

    async def encrypt_message(self, message: Message, target: JID) -> list[Message]:
        try:
            sendi_logger.info(f"encrypt one message for {target}")
            encrypted_messages_data, encryption_errors = await self["xep_0384"].encrypt_message(
                message, target
            )
        except Exception as exc:
            sendi_logger.exception(exc)
            return []
        if len(encryption_errors) > 0:
            sendi_logger.warn(
                f"There were non-critical errors during encryption: {encryption_errors}"
            )
        encrypted_messages = []
        for namespace, msg in encrypted_messages_data.items():
            msg["eme"]["namespace"] = namespace
            msg["eme"]["name"] = self["xep_0380"].mechanisms[namespace]
            encrypted_messages.append(msg)
        return encrypted_messages

    async def refresh_omemo_configuration(self, targets: list[JID]) -> None:
        session_manager = await self["xep_0384"].get_session_manager()
        for target in targets:
            # Device lists have to be manually refreshed since this bot comes online and sends messages before
            # potential pubsub/PEP notifications with device list updates had time to arrive.
            try:
                await session_manager.refresh_device_lists(str(target))
            except Exception as e:
                # An error here is non-critical
                sendi_logger.warning(f"manual device list update failed for {target}", exc_info=e)
                pass

    async def session_start(self, event: dict) -> None:  # noqa: ARG002, C901
        sendi_logger.debug("session start")
        self.send_presence()
        sendi_logger.debug("presence sended")
        self.get_roster()
        sendi_logger.debug("roster obtained")

        targets = list(self.targets)
        if not targets:
            # We always default to notifying ourselves
            targets.append(JID(self.jid))

        if self.security_level == SecurityLevel.ENCRYPTED:
            await self.refresh_omemo_configuration(targets)
            await self.omemo_initialized_event.wait()

        # HTTP _UPLOAD
        sendi_logger.debug("upload file")
        url = None
        if self.file_path:
            url = await self.upload(filename=self.file_path)
            if not url:
                sendi_logger.error("no url, disconnect")
                self.disconnect()
                return None
        sendi_logger.debug("uploaded file")
        sendi_logger.debug("prepare message")
        # MESSAGES
        messages_to_send: list[Message] = []
        while len(targets) > 0:
            # Get next target (via JID)
            target = targets.pop(0)
            # HTTP UPLOAD MESSAGE
            unencrypted_messages = []
            if url:
                # http upload message
                unencrypted_messages.append(self.create_http_upload_link(url, target))
            if self.body:
                # simple text message
                unencrypted_messages.append(
                    self.make_message(mto=target, mbody=self.body, mtype="chat")
                )
            if self.security_level == SecurityLevel.ENCRYPTED:
                encrypted_messages = []
                for message in unencrypted_messages:
                    enc_messages = await self.encrypt_message(message, target)
                    if not enc_messages:
                        sendi_logger.error("❌ Can't encrypt correctly message, skip sending")
                        self.disconnect()
                        return None
                    encrypted_messages.extend(enc_messages)
                sendi_logger.info(
                    f"prepared {len(encrypted_messages)} 🔐 encrypted messages for {target}"
                )
                messages_to_send.extend(encrypted_messages)
            else:
                sendi_logger.info(
                    f"prepared {len(unencrypted_messages)} ✉ unencrypted messages for {target}"
                )
                messages_to_send.extend(unencrypted_messages)
        sendi_logger.info(f"📨 sending {len(messages_to_send)} messages")
        for message in messages_to_send:
            sendi_logger.info("send one message")
            await asyncio.sleep(5)
            message.send()
        sendi_logger.debug("disconnect")
        self.disconnect(wait=self.disconnect_wait_time)
        self.success = True

    def on_disconnect(self, reason: str) -> None:  # noqa: ARG002
        sendi_logger.info("Disconnecting")
        self.disconnected_event.set()
