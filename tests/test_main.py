import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))

import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_main():
    with patch('subprocess.call', MagicMock()) as mock_subprocess:
        response = client.post("/scrape/", json={"url": "http://example.com"})

        assert response.status_code == 200
        assert response.json() == {"message": "Scraping started!"}

        # Verify that the subprocess call was made with the correct arguments
        mock_subprocess.assert_called_once_with(['python', 'scraper.py', 'http://example.com'])
