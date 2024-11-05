import json
from pathlib import Path

from sitemap_gazer.models import SitemapGazerConfig, Diff, Page
from sitemap_gazer.utils import get_timestamped_dirs


def readme(config: SitemapGazerConfig):
    readme_path = Path.cwd() / "README.md"

    template = """# Sitemap Gazer Report

{site_links}

{site_details}

Note: Crawls without changes or initial crawls may not be shown in detail.
"""

    site_template = """## {site_name}
"""

    crawl_template = """### {timestamp}

{pages}

Raw data: [sitemap.json](./data/{site_name}/{timestamp}/sitemap.json) and [diff.json](./data/{site_name}/{timestamp}/diff.json)
"""

    def generate_site_links():
        return "\n\n".join(
            f"[{site.name}](#{site.name.replace('.', '').lower()})"  # markdown link
            for site in config.sites
        )

    def generate_site_details():
        details = []
        for site in config.sites:
            details.append(site_template.format(site_name=site.name))

            site_crawls = get_timestamped_dirs(
                Path(config.output_dir) / site.name, limit=3
            )

            for crawl in site_crawls:
                timestamp = crawl.name
                diff_path = crawl / "diff.json"

                if diff_path.exists():
                    with diff_path.open() as diff_file:
                        diff_data = Diff.model_validate_json(diff_file.read())

                    if diff_data.pages:
                        pages = "\n".join(f"- {page.url}" for page in diff_data.pages)
                        details.append(
                            crawl_template.format(
                                timestamp=timestamp, pages=pages, site_name=site.name
                            )
                        )
        return "\n".join(details)

    with readme_path.open("w") as f:
        f.write(
            template.format(
                site_links=generate_site_links(), site_details=generate_site_details()
            )
        )
