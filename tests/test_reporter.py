"""Unit tests for the SaharaNet Reporter Agent extraction logic.

This module mocks the InMemoryRunner and Gemini API responses to test the extraction and
validation of CitizenReportAnalysis schemas without requiring active network requests or API keys.
"""

import os
import unittest
from unittest.mock import MagicMock, patch
from pydantic import BaseModel
from agents.reporter_agent import analyze_report, CitizenReportAnalysis


class MockPart:
    """Mock for google.genai.types.Part."""
    def __init__(self, text: str):
        self.text = text


class MockContent:
    """Mock for google.genai.types.Content."""
    def __init__(self, text: str):
        self.parts = [MockPart(text)]


class MockEvent:
    """Mock for google.adk.events.Event."""
    def __init__(self, output=None, text_content=None, is_final=True):
        self.output = output
        self.content = MockContent(text_content) if text_content else None
        self._is_final = is_final

    def is_final_response(self) -> bool:
        return self._is_final


class TestReporterAgent(unittest.TestCase):
    """Test suite for SaharaNet Reporter Agent parsing and error handling."""

    def setUp(self):
        # Set a dummy API key for testing environment setup
        self.original_key = os.environ.get("GEMINI_API_KEY")
        os.environ["GEMINI_API_KEY"] = "mock_key_for_testing"

    def tearDown(self):
        # Restore original environment
        if self.original_key is not None:
            os.environ["GEMINI_API_KEY"] = self.original_key
        elif "GEMINI_API_KEY" in os.environ:
            del os.environ["GEMINI_API_KEY"]

    @patch("agents.reporter_agent.InMemoryRunner")
    def test_analyze_report_direct_output(self, mock_runner_cls):
        """Test extraction when the runner returns a Pydantic model directly in event.output."""
        # Arrange
        mock_runner = MagicMock()
        mock_runner_cls.return_value = mock_runner
        
        expected_analysis = CitizenReportAnalysis(
            location="Sector 5, Noida",
            people_count=2,
            situation_types=["medical"],
            urgency_level="high",
            summary="Two injured elderly people need medical assistance.",
            original_language="English"
        )
        
        # Mock run_debug returning a list with our mock event
        mock_event = MockEvent(output=expected_analysis)
        mock_runner.run_debug.return_value = [mock_event]

        # Act
        result = analyze_report("Some report text")

        # Assert
        self.assertEqual(result.location, "Sector 5, Noida")
        self.assertEqual(result.people_count, 2)
        self.assertEqual(result.situation_types, ["medical"])
        self.assertEqual(result.urgency_level, "high")
        self.assertEqual(result.original_language, "English")
        mock_runner.close.assert_called_once()

    @patch("agents.reporter_agent.InMemoryRunner")
    def test_analyze_report_json_fallback(self, mock_runner_cls):
        """Test extraction when event.output is None and we parse JSON from event.content."""
        # Arrange
        mock_runner = MagicMock()
        mock_runner_cls.return_value = mock_runner
        
        json_response = """
        {
            "location": "Geeta Bhawan, Sector 12",
            "people_count": 5,
            "situation_types": ["food", "shelter"],
            "urgency_level": "medium",
            "summary": "Five people stranded by high waters, lacking food and shelter.",
            "original_language": "Hindi"
        }
        """
        
        # Mock run_debug returning a list with our mock event (having output=None, but json text in content)
        mock_event = MockEvent(output=None, text_content=json_response)
        mock_runner.run_debug.return_value = [mock_event]

        # Act
        result = analyze_report("Some report text in Hindi")

        # Assert
        self.assertEqual(result.location, "Geeta Bhawan, Sector 12")
        self.assertEqual(result.people_count, 5)
        self.assertEqual(result.situation_types, ["food", "shelter"])
        self.assertEqual(result.urgency_level, "medium")
        self.assertEqual(result.original_language, "Hindi")
        mock_runner.close.assert_called_once()

    @patch("agents.reporter_agent.InMemoryRunner")
    def test_analyze_report_json_markdown_fallback(self, mock_runner_cls):
        """Test extraction when the LLM wraps JSON in markdown block format."""
        # Arrange
        mock_runner = MagicMock()
        mock_runner_cls.return_value = mock_runner
        
        json_markdown = """```json
        {
            "location": "Kailash Colony metro station",
            "people_count": 3,
            "situation_types": ["child safety", "shelter"],
            "urgency_level": "high",
            "summary": "Three lost crying children need shelter and safety help.",
            "original_language": "Hinglish"
        }
        ```"""
        
        mock_event = MockEvent(output=None, text_content=json_markdown)
        mock_runner.run_debug.return_value = [mock_event]

        # Act
        result = analyze_report("Hinglish report text")

        # Assert
        self.assertEqual(result.location, "Kailash Colony metro station")
        self.assertEqual(result.people_count, 3)
        self.assertEqual(result.situation_types, ["child safety", "shelter"])
        self.assertEqual(result.urgency_level, "high")
        self.assertEqual(result.original_language, "Hinglish")
        mock_runner.close.assert_called_once()

    def test_missing_api_key_raises_error(self):
        """Test that a ValueError is raised if the API key is not in the environment."""
        # Arrange
        if "GEMINI_API_KEY" in os.environ:
            del os.environ["GEMINI_API_KEY"]
            
        # Act & Assert
        with self.assertRaises(ValueError):
            analyze_report("Test report")


if __name__ == "__main__":
    unittest.main()
