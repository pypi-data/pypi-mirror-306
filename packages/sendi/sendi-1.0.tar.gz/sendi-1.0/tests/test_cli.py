import asyncio
import os
import tomllib
from pathlib import Path

import pytest
from typer.testing import CliRunner

from sendi.bot import XMPPSendMsgBot
from sendi.cli import Config, app
from sendi.common import SecurityLevel
from tests.receiver import XMPPReceiveMsgBot

runner = CliRunner()


@pytest.fixture
def config_file() -> str:
    return os.environ.get("TEST_CONFIG_FILE", default="test.toml")


@pytest.fixture
def config_data(config_file: str) -> dict:
    with open(config_file, "rb") as file:
        return tomllib.load(file)


@pytest.fixture
def receiver1_config(config_data: dict) -> dict:
    receiver_config = config_data["receiver1"]
    clean_message(receiver_config["jid"], receiver_config["password"])
    return receiver_config


@pytest.fixture
def receiver2_config(config_data: dict) -> dict:
    receiver_config = config_data["receiver2"]
    clean_message(receiver_config["jid"], receiver_config["password"])
    return receiver_config


@pytest.fixture
def sender_unencrypted_config(config_data: dict) -> Config:
    return Config.parse_obj(config_data["sender"])


@pytest.fixture
def sender_encrypted_config(config_data: dict) -> Config:
    return Config.parse_obj(config_data["sender-encrypted"])


def test_app() -> None:
    result = runner.invoke(
        app,
        [],
    )
    assert result.exit_code == 2  # noqa: PLR2004
    assert "Usage" in result.stdout


def clean_message(jid: str, password: str, duration: int = 1) -> None:
    with asyncio.Runner() as asyncrunner:
        xmpp_bot = XMPPReceiveMsgBot(
            jid=jid,
            password=password,
            number_message_to_wait=100,
            timeout=duration,
            security_level=SecurityLevel.SIMPLE,
            logger_name="sendi_cleanup",
        )
        xmpp_bot.connect(force_starttls=True)
        asyncrunner.get_loop().run_until_complete(xmpp_bot.disconnected)


@pytest.mark.parametrize(
    "sender_config_fixture", ["sender_unencrypted_config", "sender_encrypted_config"]
)
def test_sendi(
    receiver1_config: dict,
    receiver2_config: dict,
    sender_config_fixture: str,
    request: pytest.FixtureRequest,
) -> None:
    sender_config: Config = request.getfixturevalue(sender_config_fixture)
    message = "Test"
    bot_timeout = 600
    file_path = Path("tests/test_image.jpg")
    assert file_path.is_file()
    targets = [receiver2_config["jid"], receiver1_config["jid"]]
    with asyncio.Runner() as asyncrunner:
        sender_bot = XMPPSendMsgBot(
            host=sender_config.host,
            jid=sender_config.jid,
            message_body=message,
            password=sender_config.password,
            targets=targets,
            port=sender_config.port,
            security_level=sender_config.security_level,
            lang=sender_config.lang,
            file_path=file_path if file_path else None,
        )
        receiver1_bot = XMPPReceiveMsgBot(
            jid=receiver1_config["jid"],
            password=receiver1_config["password"],
            number_message_to_wait=2,
            timeout=bot_timeout,
            security_level=sender_config.security_level,
            logger_name="sendi_receiver_1",
        )
        receiver2_bot = XMPPReceiveMsgBot(
            jid=receiver2_config["jid"],
            password=receiver2_config["password"],
            number_message_to_wait=2,
            timeout=bot_timeout,
            security_level=sender_config.security_level,
            logger_name="sendi_receiver_2",
        )

        async def wait_for_all_boot() -> None:
            receiver1_bot.connect(force_starttls=True)
            receiver2_bot.connect(force_starttls=True)
            await asyncio.gather(
                receiver1_bot.connected_event.wait(),
                receiver2_bot.connected_event.wait(),
            )
            sender_bot.connect(force_starttls=True)
            await asyncio.gather(
                receiver1_bot.disconnected_event.wait(),
                receiver2_bot.disconnected_event.wait(),
                sender_bot.disconnected_event.wait(),
            )

        asyncrunner.get_loop().run_until_complete(wait_for_all_boot())

    received_message_number = 2
    assert len(receiver2_bot.received_messages) == len(
        receiver1_bot.received_messages
    ), "Receiver2-Receiver1: Differents numbers of received messages."
    assert (
        len(receiver1_bot.received_messages) == received_message_number
    ), f"Invalid number of received message, should be {received_message_number}"

    # Check correct encryption of received message
    if sender_config.security_level == SecurityLevel.ENCRYPTED:
        assert len(receiver1_bot.encrypted_messages) == received_message_number
        assert len(receiver2_bot.encrypted_messages) == received_message_number
        assert len(receiver1_bot.unencrypted_messages) == received_message_number
        assert len(receiver2_bot.unencrypted_messages) == received_message_number
    if sender_config.security_level == SecurityLevel.SIMPLE:
        assert len(receiver1_bot.unencrypted_messages) == received_message_number
        assert len(receiver2_bot.unencrypted_messages) == received_message_number
        assert len(receiver1_bot.encrypted_messages) == 0
        assert len(receiver2_bot.encrypted_messages) == 0

    # Check content
    if "Test" in str(receiver1_bot.unencrypted_messages[0]):
        simple_message = receiver1_bot.unencrypted_messages[0]
        file_message = receiver1_bot.unencrypted_messages[1]
    else:
        simple_message = receiver1_bot.unencrypted_messages[1]
        file_message = receiver1_bot.unencrypted_messages[0]
    assert "Test" in str(simple_message)
    if sender_config.security_level == SecurityLevel.ENCRYPTED:
        assert "aesgcm" in str(file_message) # xep 0454
    if sender_config.security_level == SecurityLevel.SIMPLE:
        assert "test_image.jpg" in str(file_message)
