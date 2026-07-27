import uuid

from langchain_text_splitters import MarkdownHeaderTextSplitter


class ChunkingService:

    async def parent_child_chunk(self, cleaned_text: str) -> dict:
        # 1. Un seul split pour H1 + H2 en même temps (au lieu de 2 parses du texte)
        headers = [("#", "H1"), ("##", "H2")]
        splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers)
        docs = splitter.split_text(cleaned_text)

        # Le H1 est propagé dans les metadata de tous les docs
        h1_title = docs[0].metadata.get("H1", "")

        parent_docs = [d for d in docs if "H2" in d.metadata]
        # 2. Split de chaque parent en enfants (sous-sections H3) — inchangé
        child_headers = [("###", "H3")]
        child_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=child_headers)

        parents = []

        for parent_index, parent_doc in enumerate(parent_docs):
            parent_id = str(uuid.uuid4())
            h2_title = parent_doc.metadata.get("H2", "")
            #contneu brute utiliser pour la creation du child 
            body= parent_doc.page_content
            #contenu avec H2  va etre stocker sur le child si pas de H3
            content = h2_title + "\n" + body
            #contenu avec H1 et H2   va etre stocker sur le parent
            parent_content = h1_title + "\n" + content

            child_docs = child_splitter.split_text(body)
            
            has_h3_sections = any("H3" in c.metadata for c in child_docs)
            

            if not has_h3_sections:
                children = [{
                    "child_id": str(uuid.uuid4()),
                    "content": content,
                    "metadata": {
                        **parent_doc.metadata,
                        "parent_id": parent_id,
                        "parent_index": parent_index,
                        "chunk_index": 0,
                    },
                }]
            else:
                children = [
                    {
                        "child_id": str(uuid.uuid4()),
                        "content":  h2_title + "\n" + child_doc.metadata.get("H3", "") + "\n" +child_doc.page_content,
                        "metadata": {
                            **parent_doc.metadata,
                            **child_doc.metadata,
                            "parent_id": parent_id,
                            "parent_index": parent_index,
                            "chunk_index": chunk_index,
                        },
                    }
                    for chunk_index, child_doc in enumerate(child_docs)
                ]

            parents.append({
                "parent_id": parent_id,
                "parent_index": parent_index,
                "content": parent_content,
                "metadata": parent_doc.metadata,
                "children": children,
            })

        return {
            "parents": parents,
        }

    #async def sematicchunking(self , cleaned_text: str) -> list[dict]:
      