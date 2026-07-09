from chatbot import bot

try:
    import easyocr
except ImportError:
    easyocr = None


class OCR:

    def __init__(self):
        if easyocr is not None:
            self.reader = easyocr.Reader(["en"], gpu=False)
        else:
            self.reader = None

    def extract_text(self, image_path):
        if self.reader is None:
            return "EasyOCR is not available."

        result = self.reader.readtext(image_path, detail=0)
        return "\n".join(result)

    def ask(self, image_path, question=""):
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