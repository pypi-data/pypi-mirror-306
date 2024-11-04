import asyncio
import concurrent.futures
from pathlib import Path

from sendi.bot import XMPPSendMsgBot
from sendi.common import ConnectionType, SecurityLevel, sendi_logger


def sendi(
    host: str,
    jid: str,
    password: str,
    targets: list[str],
    port: int = 5222,
    connection_type: ConnectionType = ConnectionType.STANDARD,
    security_level: SecurityLevel = SecurityLevel.SIMPLE,
    in_thread: bool = False,
    message: str | None = None,
    file_path: Path | None = None,
    lang: str | None = None,
    omemo_cache_file_path: Path | None = None,
    clear_omemo_cache: bool = False,
) -> bool:
    bot_kwargs = {
        "host": host,
        "port": port,
        "security_level": security_level,
        "jid": jid,
        "password": password,
        "message_body": message,
        "file_path": file_path,
        "targets": targets,
        "lang": lang,
        "omemo_cache_file_path": omemo_cache_file_path,
        "clear_omemo_cache": clear_omemo_cache,
    }
    if in_thread:
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(run_loop, bot_kwargs, connection_type)
            sendi_logger.info("🚀 Runned in thread !")
            return future.result()
    else:
        sendi_logger.info("⟳ Runned outside of thread !")
        return run_loop(bot_kwargs, connection_type=connection_type)


def run_loop(bot_kwargs: dict, connection_type: ConnectionType) -> bool:
    with asyncio.Runner() as runner:
        xmpp_bot = XMPPSendMsgBot(**bot_kwargs)
        match connection_type:
            # TLS case
            case ConnectionType.TLS:
                sendi_logger.info("connect with TLS")
                xmpp_bot.connect(use_ssl=True)
            # starttls case
            case ConnectionType.STANDARD:
                sendi_logger.info("connect with STARTTLS")
                xmpp_bot.connect(force_starttls=True)
        sendi_logger.debug("running event loop")
        runner.get_loop().run_until_complete(xmpp_bot.disconnected_event.wait())
    return xmpp_bot.success
