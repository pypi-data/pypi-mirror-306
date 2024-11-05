import json
from pathlib import Path

from sitemap_gazer.models import SitemapGazerConfig
from sitemap_gazer.utils import get_timestamped_dirs


def readme(config: SitemapGazerConfig):
    """
    DEPRECATED: This function is deprecated and will be removed in a future version.
    """
    readme_path = Path.cwd() / "README.md"

    # Get the latest 5 crawls
    crawls = get_timestamped_dirs(config.output_dir, limit=5)

    with readme_path.open("w") as f:
        f.write(f"# Sitemap Gazer Report - {config.url}\n\n")

        for crawl in crawls:
            timestamp = crawl.name
            diff_path = crawl / "diff.json"

            if diff_path.exists():
                with diff_path.open() as diff_file:
                    diff_data = json.load(diff_file)

                f.write(f"## {timestamp}\n\n")

                if diff_data["pages"]:
                    for page in diff_data["pages"]:
                        f.write(f"- {page['url']}\n")
                else:
                    f.write("No changes detected.\n")

                f.write(
                    f"\nRaw data: [sitemap.json](./{timestamp}/sitemap.json) and [diff.json](./{timestamp}/diff.json)\n\n"
                )
            else:
                f.write(f"## {timestamp}\n\n")
                f.write("Initial crawl.\n\n")
                f.write(f"Raw data: [sitemap.json](./{timestamp}/sitemap.json)\n\n")
