class ProductNotFoundError(Exception):
    """Levée quand le product_id ne correspond à aucun projet."""


class FAQFileAlreadyExistsError(Exception):
    """Levée quand un fichier FAQ existe déjà pour ce produit (1 seul autorisé)."""


class FAQFileNotFoundError(Exception):
    """Levée quand le produit n'a pas de fichier FAQ."""


class InvalidFAQFileError(Exception):
    """Levée quand le JSON uploadé ne respecte pas le format attendu."""