import logging
import os
import tomllib
from pathlib import Path
from typing import Optional

import typer
from pydantic import ValidationError
from pydantic.main import BaseModel

from sendi.common import sendi_logger
from sendi.lib import ConnectionType, SecurityLevel, sendi

app = typer.Typer()

DEFAULT_CONFIG_PATH = Path(
    os.environ.get("XDG_CONFIG_HOME") or Path.home().joinpath(".config")
).joinpath("sendi", "config.toml")


class Config(BaseModel):
    host: str
    port: int = 5222
    password: str
    jid: str
    security_level: SecurityLevel = SecurityLevel.SIMPLE
    connection_type: ConnectionType = ConnectionType.STANDARD
    in_thread: bool = False
    lang: str | None = None
    loglevel: int = logging.ERROR
    omemo_cache_file_path: Path | None = None
    clear_omemo_cache: bool = False


@app.command()
def send(
    config_name: str,
    targets: list[str],
    message: Optional[str] = None,
    file_path: Optional[Path] = None,
    config_file: Path = DEFAULT_CONFIG_PATH,
) -> None:
    """
    Send message and/or file to all the target jid.
    """

    try:
        with open(config_file, "rb") as file:
            config_data = tomllib.load(file)
    except FileNotFoundError as exc:
        sendi_logger.error(f"❌ Error: Config file {config_file} not provided")
        raise typer.Exit(2) from exc
    except tomllib.TOMLDecodeError as exc:
        sendi_logger.error(f"❌ Error: Config file {config_file} is not a valid toml file")
        raise typer.Exit(2) from exc

    try:
        config = Config.parse_obj(config_data[config_name])
    except ValidationError as exc:
        sendi_logger.error(exc)
        raise typer.Exit(2) from exc

    logging.basicConfig(level=config.loglevel, format="%(levelname)-8s %(message)s")
    result = sendi(
        host=config.host,
        jid=config.jid,
        message=message,
        password=config.password,
        targets=targets,
        port=config.port,
        security_level=config.security_level,
        in_thread=config.in_thread,
        lang=config.lang,
        file_path=file_path if file_path else None,
        omemo_cache_file_path=config.omemo_cache_file_path,
        clear_omemo_cache=config.clear_omemo_cache,
    )
    if result:
        sendi_logger.info("💬 message properly send")
    else:
        sendi_logger.error("🚩 failed to send message")
        raise typer.Exit(1)
