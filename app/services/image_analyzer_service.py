from app.services.ai_service import AIService


ANALYZER_PROMPT = """
You are an image text extraction assistant.

Task:
Extract only the English text visible inside the image.

Strict rules:

1. Analyze the image carefully.
2. If the image contains words, sentences, letters, or numbers — write them exactly as they appear.
3. Do not add anything from yourself.
4. Do not correct the text.
5. If the text is unclear, write only the clearly visible part.
6. If there is no text in the image, write only:

TEXT:
No text found

ELEMENTS:
None

Response format:

TEXT:
(exact text visible in the image)

ELEMENTS:
— each word or separate part on its own line

Important:
— Do not translate
— Do not explain
— Do not teach
— Only extract the text visible in the image
"""


class ImageAnalyzerService:
    def __init__(self):
        self.ai_service = AIService()

    async def analyze_image(
        self,
        image_bytes: bytes,
        mime_type: str,
    ) -> str:
        return await self.ai_service.generate_vision_reply(
            image_bytes=image_bytes,
            mime_type=mime_type,
            prompt=ANALYZER_PROMPT,
        )
