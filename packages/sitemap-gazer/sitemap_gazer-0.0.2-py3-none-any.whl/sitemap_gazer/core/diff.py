from pathlib import Path
from typing import List
from sitemap_gazer.models import Page, Sitemap, Diff


def diff(previous_data_dir: Path, current_data_dir: Path) -> List[Page]:
    # Load previous sitemap
    previous_sitemap_path = previous_data_dir / "sitemap.json"
    with open(previous_sitemap_path, "r") as f:
        previous_sitemap = Sitemap.model_validate_json(f.read())

    # Load current sitemap
    current_sitemap_path = current_data_dir / "sitemap.json"
    with open(current_sitemap_path, "r") as f:
        current_sitemap = Sitemap.model_validate_json(f.read())

    # Extract URLs from previous sitemap
    previous_urls = set()

    def extract_urls(sitemap: Sitemap):
        for page in sitemap.pages:
            previous_urls.add(page.url)
        for sub_sitemap in sitemap.sitemaps:
            extract_urls(sub_sitemap)

    extract_urls(previous_sitemap)

    # Find new URLs in current sitemap
    new_pages = []

    def find_new_urls(sitemap: Sitemap):
        for page in sitemap.pages:
            if page.url not in previous_urls:
                new_pages.append(page)
        for sub_sitemap in sitemap.sitemaps:
            find_new_urls(sub_sitemap)

    find_new_urls(current_sitemap)

    # Remove duplicate URLs
    unique_new_pages = []
    seen_urls = set()
    for page in new_pages:
        if page.url not in seen_urls:
            unique_new_pages.append(page)
            seen_urls.add(page.url)

    # Save diff to diff.json in current data directory
    diff_path = current_data_dir / "diff.json"
    with open(diff_path, "w") as f:
        f.write(Diff(pages=unique_new_pages).model_dump_json(indent=2))

    return unique_new_pages
