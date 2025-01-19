import pytest
import asyncio
from unittest.mock import patch, AsyncMock, MagicMock
from app.scraper import scrape  # Adjust this import based on your actual module name

@pytest.fixture
def mock_playwright():
    async_playwright_mock = AsyncMock()
    browser_mock = AsyncMock()
    page_mock = AsyncMock()
    
    async_playwright_mock.return_value.chromium.launch.return_value = browser_mock
    browser_mock.new_page.return_value = page_mock
    
    page_mock.query_selector_all.return_value = [AsyncMock(inner_text=AsyncMock(return_value='Sample text 1')),
                                                 AsyncMock(inner_text=AsyncMock(return_value='Sample text 2'))]

    with patch('app.scraper.async_playwright', async_playwright_mock):
        yield async_playwright_mock

@pytest.fixture
def mock_mongo():
    mongo_mock = MagicMock()
    collection_mock = MagicMock()
    
    mongo_mock.return_value.__getitem__.return_value = collection_mock
    with patch('app.scraper.MongoClient', return_value=mongo_mock):
        yield collection_mock

@pytest.mark.asyncio
async def test_scrape(mock_playwright, mock_mongo):
    url = 'http://google.com'
    await scrape(url)

    # Check that the browser and page were launched and navigated
    mock_playwright.return_value.chromium.launch.assert_called_once_with(headless=True)
    browser = mock_playwright.return_value.chromium.launch.return_value
    browser.new_page.assert_called_once()
    page = browser.new_page.return_value
    page.goto.assert_called_once_with(url)

    # Check that data was extracted and inserted into MongoDB
    page.query_selector_all.assert_called_once_with('p')
    mock_mongo.insert_many.assert_called_once_with([{'text': 'Sample text 1'}, {'text': 'Sample text 2'}])
