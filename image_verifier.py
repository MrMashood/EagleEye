import google.generativeai as genai
from PIL import Image
import os

class ImageVerifier:
    """Verifies if product images match their descriptions using Google Gemini API."""
    
    def __init__(self, api_key: str):
        """
        Initialize the verifier with Google API key.
        
        Args:
            api_key: Google API key
        """
        self.api_key = api_key
        # Configure the library directly
        genai.configure(api_key=self.api_key)
        # Using the validated model
        self.model = genai.GenerativeModel('gemini-flash-latest')
    
    def verify_image(self, image: Image.Image, category: str, title: str) -> dict:
        """
        Verify if an image matches the given category and title.
        
        Args:
            image: PIL Image object to verify
            category: Product category (e.g., "Gaming Console", "Audio")
            title: Product title/description
            
        Returns:
            Dictionary with verification results:
            - confidence: Confidence score (0-100)
            - verdict: "Match", "Uncertain", or "Mismatch"
            - reasoning: Detailed explanation from the model
            - success: Boolean indicating if API call succeeded
            - error: Error message if success is False
        """
        try:
            # Construct prompt
            prompt = f"""You are a fraud detection system for an e-commerce platform. Analyze if the provided image matches the stated product category and title.

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

Be strict in your evaluation to protect buyers from fraud."""

            # Generate content with image and prompt
            response = self.model.generate_content([prompt, image])
            
            # Get text response
            model_response = response.text
            
            # Extract confidence, verdict, and reasoning
            confidence = self._extract_confidence(model_response)
            verdict = self._extract_verdict(model_response)
            reasoning = self._extract_reasoning(model_response)
            
            return {
                "success": True,
                "confidence": confidence,
                "verdict": verdict,
                "reasoning": reasoning,
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
        """Extract confidence score from model response."""
        try:
            for line in response.split('\n'):
                if line.strip().startswith('CONFIDENCE:'):
                    # Extract number from the line
                    confidence_str = line.split('CONFIDENCE:')[1].strip()
                    # Remove any non-digit characters except for the number itself
                    confidence = int(''.join(filter(str.isdigit, confidence_str)))
                    return max(0, min(100, confidence))  # Clamp between 0-100
        except:
            pass
        return 50  # Default if extraction fails
    
    def _extract_verdict(self, response: str) -> str:
        """Extract verdict from model response."""
        try:
            for line in response.split('\n'):
                if line.strip().startswith('VERDICT:'):
                    verdict = line.split('VERDICT:')[1].strip()
                    # Normalize verdict
                    verdict_lower = verdict.lower()
                    if 'match' in verdict_lower and 'mismatch' not in verdict_lower:
                        return "Match"
                    elif 'mismatch' in verdict_lower:
                        return "Mismatch"
                    elif 'uncertain' in verdict_lower:
                        return "Uncertain"
                    return verdict
        except:
            pass
        return "Unknown"
    
    def _extract_reasoning(self, response: str) -> str:
        """Extract reasoning from model response."""
        try:
            if 'REASONING:' in response:
                reasoning = response.split('REASONING:')[1].strip()
                return reasoning
            return response
        except:
            return response
