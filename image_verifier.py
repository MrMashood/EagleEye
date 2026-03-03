from google import genai
from google.genai import types
from PIL import Image
import io

class ImageVerifier:
    """Verifies if product images match their descriptions using Google Gemini API."""

    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-2.5-flash"

    def verify_image(self, image: Image.Image, category: str, title: str) -> dict:
        try:
            prompt = f"""
            You are a fraud detection system for an e-commerce platform. Analyze if the provided image matches the stated product category and title.

            **Product Category**: {category}
            **Product Title**: {title}

            Your task:
            1. Carefully examine the image content
            2. Determine if the image actually shows a product from the stated category
            3. Check if the image aligns with the product title
            4. Identify any red flags or inconsistencies that might indicate fraud

            Provide your analysis in the following format:

            CONFIDENCE: [number from 0-100]
            VERDICT: [Match/Uncertain/Mismatch]
            REASONING: [Your detailed explanation]

            Scoring guideline:
            - 0-30: Likely mismatch/fraud (image clearly doesn't match category or title)
            - 30-70: Uncertain/ambiguous (partially matches or unclear)
            - 70-100: Likely genuine match (image matches both category and title well)

            Be strict in your evaluation to protect buyers from fraud.
            """

            # Convert PIL image to bytes for the new SDK
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format="JPEG")
            img_bytes = img_byte_arr.getvalue()

            response = self.client.models.generate_content(
                model=self.model,
                contents=[
                    types.Part.from_bytes(data=img_bytes, mime_type="image/jpeg"),
                    types.Part.from_text(text=prompt),
                ]
            )

            model_response = response.text

            return {
                "success": True,
                "confidence": self._extract_confidence(model_response),
                "verdict": self._extract_verdict(model_response),
                "reasoning": self._extract_reasoning(model_response),
                "raw_response": model_response
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "confidence": 0,
                "verdict": "Error",
                "reasoning": f"Failed to verify image: {str(e)}"
            }

    def _extract_confidence(self, response: str) -> int:
        try:
            for line in response.split('\n'):
                if line.strip().startswith('CONFIDENCE:'):
                    confidence_str = line.split('CONFIDENCE:')[1].strip()
                    confidence = int(''.join(filter(str.isdigit, confidence_str)))
                    return max(0, min(100, confidence))
        except:
            pass
        return 50

    def _extract_verdict(self, response: str) -> str:
        try:
            for line in response.split('\n'):
                if line.strip().startswith('VERDICT:'):
                    verdict = line.split('VERDICT:')[1].strip()
                    verdict_lower = verdict.lower()
                    if 'mismatch' in verdict_lower:
                        return "Mismatch"
                    elif 'match' in verdict_lower:
                        return "Match"
                    elif 'uncertain' in verdict_lower:
                        return "Uncertain"
                    return verdict
        except:
            pass
        return "Unknown"

    def _extract_reasoning(self, response: str) -> str:
        try:
            if 'REASONING:' in response:
                return response.split('REASONING:')[1].strip()
            return response
        except:
            return response