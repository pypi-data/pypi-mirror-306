from pydantic import BaseModel, Field
from langchain_aws.chat_models.bedrock import ChatBedrock
from langchain import hub
import logging
from typing import Literal
from langchain_core.output_parsers import StrOutputParser
from langchain_core.tools import tool
from langchain.agents import AgentExecutor, create_tool_calling_agent
from aind_data_access_api.document_db import MetadataDbClient
from pprint import pprint
from typing_extensions import Annotated, TypedDict

logging.basicConfig(filename='agentic_graph.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', filemode="w")

MODEL_ID_SONNET_3 = "anthropic.claude-3-sonnet-20240229-v1:0"
MODEL_ID_SONNET_3_5 = "anthropic.claude-3-sonnet-20240229-v1:0"
SONNET_3_LLM = ChatBedrock(
    model_id= MODEL_ID_SONNET_3,
    model_kwargs= {
        "temperature": 0
    }
)

SONNET_3_5_LLM = ChatBedrock(
    model_id= MODEL_ID_SONNET_3_5,
    model_kwargs= {
        "temperature": 0
    }
)

#determining if entire database needs to be surveyed
class RouteQuery(BaseModel):
    """Route a user query to the most relevant datasource."""

    reasoning: str = Field(
        description="Give a one sentence justification for the chosen method",
    )

    datasource: Literal["vectorstore", "direct_database"] = Field(
        description="Given a user question choose to route it to the direct database or its vectorstore.",
    )

structured_llm_router = SONNET_3_LLM.with_structured_output(RouteQuery)
router_prompt = hub.pull("eden19/query_rerouter")
datasource_router = router_prompt | structured_llm_router
#print(datasource_router.invoke({"query": "What is the mongodb query to find the injections for SmartSPIM_675387_2023-05-23_23-05-56?"}).datasource)

# Queries that require surveying the entire database (like count based questions)
# credentials = DocumentDbSSHCredentials()
# credentials.database = "metadata_vector_index"
# credentials.collection = "curated_assets"
API_GATEWAY_HOST = "api.allenneuraldynamics-test.org"
DATABASE = "metadata_vector_index"
COLLECTION = "curated_assets"

docdb_api_client = MetadataDbClient(
   host=API_GATEWAY_HOST,
   database=DATABASE,
   collection=COLLECTION,
)

@tool
def aggregation_retrieval(agg_pipeline: list) -> list:
    """Given a MongoDB query and list of projections, this function retrieves and returns the 
    relevant information in the documents. 
    Use a project stage as the first stage to minimize the size of the queries before proceeding with the remaining steps.
    The input to $map must be an array not a string, avoid using it in the $project stage.

    Parameters
    ----------
    agg_pipeline
        MongoDB aggregation pipeline

    Returns
    -------
    list
        List of retrieved documents
    """

    result = docdb_api_client.aggregate_docdb_records(
        pipeline=agg_pipeline
    )
    return result
        
tools = [aggregation_retrieval]
db_prompt = hub.pull("eden19/entire_db_retrieval")
db_surveyor_agent = create_tool_calling_agent(SONNET_3_LLM, tools, db_prompt)
query_retriever = AgentExecutor(agent=db_surveyor_agent, tools=tools, return_intermediate_steps = True, verbose=False)

# Processing query
# class ProcessQuery(BaseModel):
#     """Binary score to check whether query requires retrieval to be filtered with metadata information to achieve accurate results."""

#     binary_score: str = Field(
#         description="Query requires further filtering during retrieval process, 'yes' or 'no'"
#     )
#     reasoning: str = Field("One short sentence justifying why a filter was picked or not picked")

# query_grader = SONNET_3_5_LLM.with_structured_output(ProcessQuery)
# query_grade_prompt = hub.pull("eden19/processquery")
# query_grader = query_grade_prompt | query_grader
#print(query_grader.invoke({"query": "What is the genotype for mouse 675387?"}).binary_score)

# Generating appropriate filter
class FilterGenerator(BaseModel):
    """MongoDB filter to be applied before vector retrieval"""

    filter_query: dict = Field(description="MongoDB filter")
    #top_k: int = Field(description="Number of documents to retrieve from the database")

filter_prompt = hub.pull("eden19/filtergeneration")
filter_generator_llm = SONNET_3_LLM.with_structured_output(FilterGenerator)

filter_generation_chain = filter_prompt | filter_generator_llm
#print(filter_generation_chain.invoke({"query": "What is the genotype for mouse 675387?"}).filter_query)

# Check if retrieved documents answer question
class RetrievalGrader(TypedDict):
    """Binary score to check whether retrieved documents are relevant to the question"""

    relevant_context:Annotated[str, ..., "Relevant context extracted from document that helps directly answer the question"]
    binary_score: Annotated[Literal["yes", "no"], ..., "Retrieved documents are relevant to the query, 'yes' or 'no'"]
    #relevant_context: Annotated[str, None, "Summarize relevant pieces of context in document"]

retrieval_grader = SONNET_3_5_LLM.with_structured_output(RetrievalGrader)
retrieval_grade_prompt = hub.pull("eden19/retrievalgrader")
doc_grader = retrieval_grade_prompt | retrieval_grader
# doc_grade = doc_grader.invoke({"query": question, "document": doc}).binary_score
# logging.info(f"Retrieved document matched query: {doc_grade}")

# Generating response to documents
answer_generation_prompt = hub.pull("eden19/answergeneration")
rag_chain = answer_generation_prompt | SONNET_3_5_LLM | StrOutputParser()

db_answer_generation_prompt = hub.pull("eden19/db_answergeneration")
# class DatabaseGeneration(BaseModel):
#     """  """

#     agg_pipeline: str = Field(
#         description="mongodb aggregation pipeline found in the documents"
#     )

#     summarized_context: str = Field(
#         description="Summary of retrieved output dictionary found in the documents. This is NOT the mongodb pipeline but the information that follows the pipeline"
#     )

# database_answer_generation = LLM.with_structured_output(DatabaseGeneration)
db_rag_chain = db_answer_generation_prompt | SONNET_3_5_LLM | StrOutputParser()
# generation = rag_chain.invoke({"documents": doc, "query": question})
# logging.info(f"Final answer: {generation}")