from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from pathlib import Path


class Site(BaseModel):
    name: str
    url: str


class SitemapGazerConfig(BaseModel):
    sites: List[Site] = Field(
        default_factory=list, description="List of sites to monitor"
    )
    genReadme: bool = Field(
        default=True, description="Whether to generate a README report"
    )
    output_dir: Path = Field(
        default=Path("./data"),
        description="The directory to store the output files",
    )


class NewsStory(BaseModel):
    title: str
    publish_date: datetime
    publication_name: str
    publication_language: str
    access: Optional[str] = None
    genres: List[str] = Field(default_factory=list)
    keywords: List[str] = Field(default_factory=list)
    stock_tickers: List[str] = Field(default_factory=list)


class Page(BaseModel):
    url: str
    priority: Optional[float] = None
    last_modified: Optional[datetime] = None
    change_frequency: Optional[str] = None
    news_story: Optional[NewsStory] = None


class Sitemap(BaseModel):
    url: str
    type: str
    sitemaps: List["Sitemap"] = Field(default_factory=list)
    pages: List[Page] = Field(default_factory=list)


class Diff(BaseModel):
    pages: List[Page] = Field(default_factory=list)


Sitemap.model_rebuild()  # This is needed for the self-referential type hint to work
