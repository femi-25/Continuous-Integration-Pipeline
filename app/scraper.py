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
        
        print(f"Scraping URL: {url}")
        elements = await page.query_selector_all('p')
        print(f"Number of <p> elements found: {len(elements)}")

        if not elements:
            print("No <p> tags found on the page.")
            await browser.close()
            return

        # Extract data
        data = []
        for element in elements:
            text = await element.inner_text()
            print(f"Extracted text inside scrape function: {text}")  # Debug statement
            data.append({'text': text})
        
        print(f"Data to be inserted inside scrape function: {data}")  # Debug statement
        
        # Store data in MongoDB
        if data:
            collection.insert_many(data)
            print("Data inserted into MongoDB")
        else:
            print("No data to insert")
        
        await browser.close()

if __name__ == "__main__":
    url = sys.argv[1]
    asyncio.run(scrape(url))
