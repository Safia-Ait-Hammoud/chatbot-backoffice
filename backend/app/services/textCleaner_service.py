import re


class TextCleaner:

  def clean(self, markdown: str) -> str:
        
        markdown = re.sub(r'~~(.*?)~~', r'\1', markdown)

  
        # 4. Remplacer les puces isolées "•" par un vrai item de liste "-"
        markdown = re.sub(r'[ \t]*•[ \t]*', '\n- ', markdown)

       
        # 6. Nettoyer les titres en gras : 
        markdown = re.sub(r'^(#+)\s+\*\*(.*?)\*\*$',r'\1 \2',markdown, flags=re.MULTILINE)

        # 8. Réduire les lignes vides multiples
        markdown = re.sub(r'\n{3,}', '\n\n', markdown)

        # 9. Fusionner un titre coupé sur plusieurs lignes
        markdown = re.sub( r'(#+ .+)\n\n(.+?\?)',r'\1 \2',markdown)

        return markdown.strip()