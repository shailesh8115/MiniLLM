import easyocr

from chatbot import bot


class OCR:

    def __init__(self):
        self.reader = easyocr.Reader(["en"], gpu=False)

    def extract_text(self, image_path):

        result = self.reader.readtext(
            image_path,
            detail=0
        )

        return "\n".join(result)

    def ask(
        self,
        image_path,
        question=""
    ):

        text = self.extract_text(image_path)

        if not question:

            return text

        prompt = f"""
Image OCR Text

{text}

Question

{question}
"""

        return bot.chat(prompt)


ocr = OCR()