import uuid

from langchain_text_splitters import MarkdownHeaderTextSplitter


class ChunkingService:

    async def parent_child_chunk(self, document: dict, cleaned_text: str) -> dict:
        # 1. Split en chunks "parents" (sections H1/H2)
        parent_headers = [("#", "H1"), ("##", "H2")]
        parent_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=parent_headers)
        parent_docs = parent_splitter.split_text(cleaned_text)

        # 2. Split de chaque parent en chunks "enfants" (sous-sections H3)
        child_headers = [("###", "H3")]
        child_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=child_headers)

        parents = []

        for parent_doc in parent_docs:
            parent_id = str(uuid.uuid4())

            child_docs = child_splitter.split_text(parent_doc.page_content)
            has_h3_sections = any("H3" in child_doc.metadata for child_doc in child_docs)

            if not has_h3_sections:
                # Pas de vraie sous-section H3 donc  le parent = enfant
                children = [{
                    "content": parent_doc.page_content,
                    "metadata": {
                        **parent_doc.metadata,
                        "parent_id": parent_id,
                    },
                }]
            else:
                children = [
                    {
                        "content": child_doc.page_content,
                        "metadata": {
                            **parent_doc.metadata,
                            **child_doc.metadata,
                            "parent_id": parent_id,
                        },
                    }
                    for child_doc in child_docs
                ]

            parents.append({
                "parent_id": parent_id,
                "content": parent_doc.page_content,
                "metadata": parent_doc.metadata,
                "children": children,
            })

        return {
            "document_id": document["id"],
            "project_id": document["project_id"],
            "parents": parents,
        }