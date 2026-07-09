from chatbot import bot

try:
    import easyocr
except ImportError:
    easyocr = None

class OCR:

    ...

    def extract_text(self, image_path):

        result = self.reader.readtext(
            image_path,
            detail=0
        )

        return "\n".join(result)

    # Alias
    def extract(self, image_path):
        return self.extract_text(image_path)
    # -----------------------
    # Ask AI
    # -----------------------

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