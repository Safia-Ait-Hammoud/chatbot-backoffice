import pymupdf
import pymupdf4llm


class Extractor:

    def extract(self, file_bytes: bytes) -> str:
        doc = pymupdf.open(stream=file_bytes, filetype="pdf")
        try:
            markdown = pymupdf4llm.to_markdown(doc)
        finally:
            doc.close()

        return markdown.strip()