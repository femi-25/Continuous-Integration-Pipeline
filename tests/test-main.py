import pytest
from unittest.mock import patch, MagicMock
from app.main import main  # Adjust this import based on your actual module name

def test_main():
    with patch('app.main.scrape', MagicMock()) as mock_scrape:
        mock_scrape.return_value = None  # Or set to appropriate return value if any
        main()

    # Verify that the scrape function was called
    mock_scrape.assert_called_once()
