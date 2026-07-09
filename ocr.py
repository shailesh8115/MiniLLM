from chatbot import bot

try:
    import easyocr
except Exception:
    easyocr = None


class OCR:

    def __init__(self):
        self.reader = None

        if easyocr is not None:
            try:
                self.reader = easyocr.Reader(
                    ["en"],
                    gpu=False
                )
            except Exception as e:
                print("EasyOCR initialization failed:", e)
                self.reader = None

    def extract_text(self, image_path):

        if self.reader is None:
            return "❌ EasyOCR is not available on this deployment."

        result = self.reader.readtext(
            image_path,
            detail=0
        )

        return "\n".join(result)

    def ask(self, image_path, question=""):

        text = self.extract_text(image_path)

        if text.startswith("❌"):
            return text

        if not question:
            return text

        return bot.chat(
            f"Image OCR Text:\n\n{text}\n\nQuestion:\n{question}"
        )


ocr = OCR()