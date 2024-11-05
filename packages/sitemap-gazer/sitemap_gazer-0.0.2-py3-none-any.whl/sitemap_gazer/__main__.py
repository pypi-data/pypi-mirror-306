from datetime import datetime
import click
import tempfile
import shutil
from pathlib import Path
from sitemap_gazer.core.crawl import crawl
from sitemap_gazer.core.diff import diff
from sitemap_gazer.core.init import create_config_file, load_config_file
from sitemap_gazer.batch.readme import readme
from sitemap_gazer.utils import get_timestamped_dirs


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is not None:
        # this should never happen
        return

    try:
        config = load_config_file(Path.cwd() / "sitemap-gazer.json")
        data_dir = Path.cwd() / "data"
        data_dir.mkdir(parents=True, exist_ok=True)
    except FileNotFoundError:
        click.echo(
            "Config file not found. Please run 'sitemap-gazer init <URL>' to create a new configuration."
        )
        return

    # Create timestamp for this crawl
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    have_changes = False

    for site in config.sites:
        site_dir = Path(config.output_dir) / site.name
        site_dir.mkdir(parents=True, exist_ok=True)

        # Get latest crawl for this site
        latest_site_crawl = None
        site_dirs = get_timestamped_dirs(site_dir, limit=1)
        if len(site_dirs) > 0:
            latest_site_crawl = site_dirs[0]
        else:
            click.echo(
                f"No previous crawl found for {site.name}. Starting initial crawl."
            )

        # Create temporary directory for crawl
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir)

            click.echo(f"Crawling {site.url} to temporary directory")
            crawl(site.url, temp_dir_path)

            # Calculate diff if we have a previous crawl
            if latest_site_crawl:
                click.echo(f"Calculating diff for {site.name}")
                diff_pages = diff(latest_site_crawl, temp_dir_path)
                click.echo(
                    f"Found {len(diff_pages)} new pages, {[p.url for p in diff_pages]}"
                )
                if len(diff_pages) > 0:
                    have_changes = True
                    # Move from temp to final location if changes found
                    final_dir = site_dir / timestamp
                    shutil.copytree(temp_dir_path, final_dir)
            else:
                have_changes = True
                # Move from temp to final location for initial crawl
                final_dir = site_dir / timestamp
                shutil.copytree(temp_dir_path, final_dir)

    if not have_changes:
        click.echo("No changes detected in any site.")
        return

    if config.genReadme:
        # update README.md
        click.echo("Updating README.md")
        readme(config)


@cli.command()
def init():
    pwd = Path.cwd()
    config_file_path = create_config_file(pwd)
    config = load_config_file(config_file_path)
    click.echo(config)
    click.echo(f"Created {config_file_path}")
    click.echo(f"add site to {config_file_path} to begin")


@cli.command(name="readme")
def update_readme():
    pwd = Path.cwd()
    config = load_config_file(pwd / "sitemap-gazer.json")
    click.echo("Updating README.md")
    readme(config)


if __name__ == "__main__":
    cli()
