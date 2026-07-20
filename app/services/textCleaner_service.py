import re


class TextCleaner:

  def clean(self, markdown: str) -> str:
        
        markdown = re.sub(r'~~(.*?)~~', r'\1', markdown)

        # 2. Supprimer les espaces en fin de ligne
        markdown = "\n".join(line.rstrip()
          for line in markdown.splitlines() 
          )
        # 3. Normaliser les hard line breaks Markdown ("  \n") en simple saut de ligne
        markdown = re.sub(r' {2,}\n', '\n', markdown)

        # 4. Remplacer les puces isolées "•" par un vrai item de liste "-"
        markdown = re.sub(r'[ \t]*•[ \t]*', '\n- ', markdown)

        # 5. Forcer un saut de ligne avant un header collé en plein milieu    
        markdown = re.sub(r'(?<!\n)(#{1,6}\s)', r'\n\1', markdown)

        # 6. Nettoyer les titres en gras : 
        markdown = re.sub(r'^(#+)\s+\*\*(.*?)\*\*$',r'\1 \2',markdown, flags=re.MULTILINE)

        # 8. Réduire les lignes vides multiples
        markdown = re.sub(r'\n{3,}', '\n\n', markdown)

        # 9. Fusionner un titre coupé sur plusieurs lignes
        markdown = re.sub( r'(#+ .+)\n\n(.+?\?)',r'\1 \2',markdown)

        # 10. Nettoyer les espaces multiples résiduels (hors début de ligne,
        markdown = re.sub(r'(?<=\S)[ \t]{2,}(?=\S)', ' ', markdown)

        return markdown.strip()