import json
import os
from typing import List
import sys
import traceback
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Annotated
from urllib.parse import urlparse

from operator import itemgetter
import human_readable
import pytimeparse
import typer
import websockets
from dateutil import parser
from loguru import logger
from tabulate import tabulate
from typer_config.decorators import use_toml_config

from trainwave_cli.api import Api, Secret
from trainwave_cli.config.config import config
from trainwave_cli.utils import async_command, ensure_api_key

app = typer.Typer()


@app.command()
@async_command
@use_toml_config(default_value="trainwave.toml")
@ensure_api_key
async def list(
    organization: Annotated[str, typer.Option(help="The organization ID or RID")],
) -> None:
    api_client = Api(config.api_key, config.endpoint)
    secrets = await api_client.list_secrets(organization)

    project_scoped = [secret for secret in secrets if secret.project]
    org_scoped = [secret for secret in secrets if not secret.project]
    unique: dict[str, tuple[bool, Secret]] = {}

    for org_secret in org_scoped:
        unique[org_secret.name] = (False, org_secret)

    for project_secret in project_scoped:
        if project_secret.name in unique:
            unique[project_secret.name] = (True, project_secret)
        else:
            unique[project_secret.name] = (False, project_secret)

    sorted_secrets = dict(sorted(unique.items(), key=itemgetter(0)))

    headers = ["ID", "NAME", "SCOPE", "DIGEST", "CREATED"]
    table = [
        [
            secret.rid,
            secret.name if not overridden else f"{secret.name} (*)",
            "PROJECT" if secret.project else "ORG",
            secret.digest[:16],
            human_readable.date_time(
                datetime.now(timezone.utc) - parser.parse(secret.created_at)
            ),
        ]
        for (overridden, secret) in sorted_secrets.values()
    ]
    typer.echo(tabulate(table, headers=headers, tablefmt="simple"))


@app.command()
@async_command
@use_toml_config(default_value="trainwave.toml")
@ensure_api_key
async def set(
    organization: Annotated[str, typer.Option(help="The organization ID or RID")],
    secrets: List[str],
    project: Annotated[str | None, typer.Option(help="Project ID or RID")] = None,
) -> None:
    secret_dict: dict[str, str] = {}
    for secret in secrets:
        splitted = secret.split("=")

        # Validate format
        if len(splitted) != 2:
            typer.echo(
                f"Error: Invalid format '{secret}'. Expected format is KEY=VALUE.",
                err=True,
            )
            raise typer.Exit(code=1)

        secret_name, secret_value = splitted
        secret_dict[secret_name] = secret_value

    # Now call API and insert
    api_client = Api(config.api_key, config.endpoint)
    await api_client.set_secrets(organization, secret_dict, project)


@app.command()
@async_command
@use_toml_config(default_value="trainwave.toml")
@ensure_api_key
async def unset(
    organization: Annotated[str, typer.Option(help="The organization ID or RID")],
    secrets: List[str],
) -> None:
    api_client = Api(config.api_key, config.endpoint)
    await api_client.unset_secrets(organization, secrets)
