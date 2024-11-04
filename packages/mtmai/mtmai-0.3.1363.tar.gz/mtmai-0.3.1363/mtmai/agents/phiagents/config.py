from phi.knowledge.combined import CombinedKnowledgeBase
from phi.knowledge.pdf import PDFUrlKnowledgeBase
from phi.model.openai import OpenAIChat
from phi.storage.agent.postgres import PgAgentStorage
from phi.vectordb.pgvector import PgVector, SearchType

from mtmai.core.config import settings
from mtmai.core.logging import get_logger

logger = get_logger()


#
storage = PgAgentStorage(table_name="pdf_agent", db_url=settings.DATABASE_URL)


url_pdf_knowledge_base = PDFUrlKnowledgeBase(
    urls=["https://phi-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"],
    vector_db=PgVector(
        table_name="recipes_demo",
        db_url=settings.DATABASE_URL,
        search_type=SearchType.hybrid,
    ),
)
# Load the knowledge base: Comment out after first run
# knowledge_base.load(recreate=True, upsert=True)

knowledge_base = CombinedKnowledgeBase(
    sources=[
        url_pdf_knowledge_base,
        # website_knowledge_base,
        # local_pdf_knowledge_base,
    ],
    vector_db=PgVector(
        # Table name: ai.combined_documents
        table_name="combined_documents",
        db_url=settings.DATABASE_URL,
    ),
)


model = OpenAIChat(
    id="meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
    base_url="https://api.together.xyz/v1",
    api_key="10747773f9883cf150558aca1b0dda81af4237916b03d207b8ce645edb40a546",
)
