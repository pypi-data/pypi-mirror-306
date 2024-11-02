import asyncio
from typing import Optional

import modal


async def playwright_web_scrape(url: str, timeout: int = 60 * 5) -> Optional[str]:
    playwright_web_scraper = modal.Function.lookup(
        "web-scraper", "playwright_web_scrape"
    )

    try:
        result = await asyncio.wait_for(
            playwright_web_scraper.remote.aio(url), timeout=timeout
        )
        return result
    except asyncio.TimeoutError as e:
        print("Timeout web scraping hit")
        return None
