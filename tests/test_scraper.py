import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))

import pytest
import asyncio
from scraper import scrape  # Ensure the correct module name

@pytest.mark.asyncio
async def test_scrape_with_real_website():
    url = 'http://example.com'

    await scrape(url)
    # There are no assertions here, as we're only demonstrating that the scrape function can run.
    # You would typically check the data inserted into the database or some other side effect.
