import re
from decimal import Decimal

from playwright.sync_api import sync_playwright

from src.application.ports.listing_scraper import ListingScraper
from src.domain.entities.listing import Listing


class OlxScraper(ListingScraper):
    def fetch(self, url: str) -> list[Listing]:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto(url, wait_until="networkidle", timeout=60000)

            links = page.locator('a[href*="/d/oferta/"], a[href*="/oferta/"]').evaluate_all(
                """
                elements => elements.map(a => ({
                    href: a.href,
                    title: (a.innerText || '').trim()
                }))
                """
            )

            browser.close()

        listings: list[Listing] = []

        for item in links:
            href = item.get("href")
            title = item.get("title", "").strip()

            if not href:
                continue

            if not title or len(title) < 8:
                continue

            external_id = self._extract_external_id(href)
            if external_id is None:
                continue

            if not self._looks_like_apartment(title):
                continue

            listings.append(
                Listing(
                    id=None,
                    external_id=external_id,
                    title=title,
                    url=href,
                    price=None,
                    location=None,
                )
            )

        unique_by_external_id: dict[str, Listing] = {}
        for listing in listings:
            unique_by_external_id[listing.external_id] = listing

        return list(unique_by_external_id.values())

    @staticmethod
    def _extract_external_id(url: str) -> str | None:
        match = re.search(r"-ID([A-Za-z0-9]+)\.html", url)
        if match:
            return match.group(1)

        match = re.search(r"ID([A-Za-z0-9]+)\.html", url)
        if match:
            return match.group(1)

        return None

    @staticmethod
    def _looks_like_apartment(title: str) -> bool:
        lowered = title.lower()
        apartment_keywords = [
            "apartament",
            "garsoniera",
            "garsonieră",
            "studio",
            "2 camere",
            "3 camere",
            "1 camera",
            "1 cameră",
            "4 camere",
        ]
        return any(keyword in lowered for keyword in apartment_keywords)