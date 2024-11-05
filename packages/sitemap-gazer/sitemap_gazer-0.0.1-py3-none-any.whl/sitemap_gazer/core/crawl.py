import json
from datetime import datetime
from typing import Dict, Any
from pathlib import Path
from pydantic import HttpUrl
from usp.tree import sitemap_tree_for_homepage
from usp.objects.sitemap import AbstractSitemap, PagesXMLSitemap, PagesTextSitemap
from urllib.parse import urlparse
from decimal import Decimal

from sitemap_gazer.models import SitemapGazerConfig, Sitemap, Page, NewsStory


def sitemap_to_dict(sitemap: AbstractSitemap) -> Sitemap:
    result = Sitemap(url=sitemap.url, type=sitemap.__class__.__name__)

    if isinstance(sitemap, (PagesXMLSitemap, PagesTextSitemap)):
        for page in sitemap.pages:
            page_dict = Page(
                url=page.url,
                priority=(
                    float(page.priority)
                    if isinstance(page.priority, Decimal)
                    else page.priority
                ),
                last_modified=(
                    page.last_modified.isoformat() if page.last_modified else None
                ),
                change_frequency=(
                    page.change_frequency.value if page.change_frequency else None
                ),
            )
            if page.news_story:
                page_dict.news_story = NewsStory(
                    title=page.news_story.title,
                    publish_date=page.news_story.publish_date,
                    publication_name=page.news_story.publication_name,
                    publication_language=page.news_story.publication_language,
                    access=page.news_story.access,
                    genres=page.news_story.genres,
                    keywords=page.news_story.keywords,
                    stock_tickers=page.news_story.stock_tickers,
                )
            result.pages.append(page_dict)
    elif hasattr(sitemap, "sub_sitemaps"):
        for sub_sitemap in sitemap.sub_sitemaps:
            result.sitemaps.append(sitemap_to_dict(sub_sitemap))

    return result


def crawl(
    url: HttpUrl,
    output_dir: Path,
) -> Path:
    tree: AbstractSitemap = sitemap_tree_for_homepage(url)
    tree_sitemap: Sitemap = sitemap_to_dict(tree)

    # Save sitemap as JSON
    sitemap_filepath = output_dir / "sitemap.json"
    with sitemap_filepath.open("w") as f:
        json.dump(tree_sitemap.model_dump(), f, indent=2, default=str)

    return sitemap_filepath
