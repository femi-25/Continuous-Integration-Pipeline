import asyncio
from playwright.async_api import async_playwright
from pymongo import MongoClient
import sys
import os

# MongoDB connection
client = MongoClient(os.getenv('MONGO_URI'))
db = client['scraping_db']
collection = db['scraped_data']

async def scrape(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)
        
        # Extract data
        elements = await page.query_selector_all('p')
        data = []
        for element in elements:
            text = await element.inner_text()
            data.append({'text': text})
        
        # Store data in MongoDB
        collection.insert_many(data)
        await browser.close()

if __name__ == "__main__":
    url = sys.argv[1]
    asyncio.run(scrape(url))
