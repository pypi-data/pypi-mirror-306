import os
import json
from typing import Dict
from pathlib import Path

import click
from sitemap_gazer.models import SitemapGazerConfig


def create_config_file(output_dir: str) -> str:
    config = SitemapGazerConfig()

    file_path = os.path.join(output_dir, "sitemap-gazer.json")

    if os.path.exists(file_path):
        raise click.ClickException(f"Config file already exists: {file_path}")

    with open(file_path, "w") as f:
        config_dict = config.model_dump()
        config_dict["output_dir"] = str(
            config_dict["output_dir"]
        )  # Handle JSON unserializable Posix Path
        json.dump(config_dict, f, indent=2)

    return file_path


def load_config_file(file_path: str) -> SitemapGazerConfig:
    with open(file_path, "r") as f:
        return SitemapGazerConfig.model_validate_json(f.read())
