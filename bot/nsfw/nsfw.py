"""Analyze the message."""
from googleapiclient import discovery
from decouple import config  # type: ignore
import json
API_KEY = config("API_KEY")


class AnalyzeMessage():
    """Analyze a message"""

    def __init__(self):
        """Initialize the message"""
        pass

    def analyze_text(self, message):
        """Analyze text and return maximum values.

        Args:
            message (str):text to analyze

        Returns:
            [int]: integer
        """
        # Generates API client object dynamically based on service name and version.
        category_list = ["THREAT", "TOXICITY",
                         "INSULT", "SEXUALLY_EXPLICIT", "FLIRTATION"]
        service = discovery.build(
            'commentanalyzer', 'v1alpha1', developerKey=API_KEY)
        analyze_request = {
            'comment': {'text': message},
            'requestedAttributes': {'TOXICITY': {}, "THREAT": {},
                                    "INSULT": {}, "SEXUALLY_EXPLICIT": {},
                                    "FLIRTATION": {}}
        }
        try:
            response = service.comments().analyze(body=analyze_request).execute()
            value = -1
            for category in category_list:
                value = max(value,
                            response["attributeScores"][category]["spanScores"][0]["score"]["value"])
        except Exception:
            return -1
        return value
