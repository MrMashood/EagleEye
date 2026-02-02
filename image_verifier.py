import torch
from PIL import Image
from transformers import BlipProcessor, BlipForQuestionAnswering


class ImageVerifier:
    def __init__(self):
        self.device = "cpu"

        self.processor = BlipProcessor.from_pretrained(
            "Salesforce/blip-vqa-base"
        )

        self.model = BlipForQuestionAnswering.from_pretrained(
            "Salesforce/blip-vqa-base"
        ).to(self.device)

        self.model.eval()

    def verify_image(self, image: Image.Image, category: str, title: str) -> dict:
        try:
            question = (
                f"Does this image show a {title} "
                f"that belongs to the category {category}?"
            )

            inputs = self.processor(
                image,
                question,
                return_tensors="pt"
            ).to(self.device)

            with torch.no_grad():
                output = self.model.generate(
                    **inputs,
                    max_new_tokens=20
                )

            answer = self.processor.decode(
                output[0],
                skip_special_tokens=True
            ).lower()

            confidence, verdict = self._score(answer)

            return {
                "success": True,
                "confidence": confidence,
                "verdict": verdict,
                "reasoning": answer.capitalize()
            }

        except Exception as e:
            return {
                "success": False,
                "confidence": 0,
                "verdict": "Error",
                "reasoning": str(e)
            }

    def _score(self, answer: str):
        if "yes" in answer:
            return 80, "Match"
        if "no" in answer:
            return 20, "Mismatch"
        return 50, "Uncertain"
