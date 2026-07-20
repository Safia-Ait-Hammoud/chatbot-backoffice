from tempfile import NamedTemporaryFile
import pymupdf4llm


class Extractor:

    def extract(self, file_bytes: bytes) -> str:

        with NamedTemporaryFile(
            suffix=".pdf",
            delete=True
        ) as tmp:

            tmp.write(file_bytes)
            tmp.flush()

            markdown = pymupdf4llm.to_markdown(
                tmp.name
            )

        return markdown.strip()