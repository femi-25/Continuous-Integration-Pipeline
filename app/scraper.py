import asyncio
from playwright.async_api import async_playwright
from pymongo import MongoClient
import sys
import os

# MongoDB connection
client = MongoClient(os.getenv('MONGO_URI'))
db = client['scraping_db']
collection = db['scraped_data']

async def scrape(url, output_file="scraped_text.txt", output_dir="output"):
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
        all_text = ""  # Variable to store all text for the .txt file
        for element in elements:
            text = await element.inner_text()
            print(f"Extracted text: {text}")  # Debug statement
            data.append({'text': text})
            all_text += text + "\n"  # Append text for the file

        print(f"Data to be inserted: {data}")  # Debug statement

        # Save all text to a .txt file
        if data:
            try:
                # Ensure the output directory exists
                os.makedirs(output_dir, exist_ok=True)

                # Create the full path to the output file
                file_path = os.path.join(output_dir, output_file)

                # Write the scraped text to the file
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(all_text)

                print(f"Scraped text saved to: {file_path}")
            except Exception as e:
                print(f"Error while saving text to file: {e}")

        else:
            print("No data to insert")        

        # Save data to MongoDB
        if data:
            try:
                collection.insert_many(data)
                print("Data inserted into MongoDB")
            except Exception as e:
                print(f"Error inserting data into MongoDB")
    
        else:
            print("No data to insert")

        
        await browser.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scraper.py <URL>")
        sys.exit(1)

    url = sys.argv[1]
    asyncio.run(scrape(url))

