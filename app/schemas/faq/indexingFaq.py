from pydantic import BaseModel


class FAQCreatedEvent(BaseModel):
    faq_id: str
    product_id: str
    question: str
    answer: str
    category: str 

class FAQUpdatedEvent(BaseModel):
    faq_id: str
    product_id: str
    question: str
    answer: str
    category: str 
    question_changed: bool = False


class FAQDeletedEvent(BaseModel):
    faq_id: str
    product_id: str