import logging, asyncio, json
from typing import List, Optional
from typing_extensions import TypedDict
from langchain_core.documents import Document
from langgraph.graph import END, StateGraph, START
from metadata_chatbot.agents.docdb_retriever import DocDBRetriever

from metadata_chatbot.agents.agentic_graph import datasource_router, query_retriever, filter_generation_chain, doc_grader, rag_chain, db_rag_chain

logging.basicConfig(filename='async_workflow.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', filemode="w")

class GraphState(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        query: question asked by user
        generation: LLM generation
        documents: list of documents
    """

    query: str
    generation: str
    documents: List[str]
    filter: Optional[dict]
    #top_k: Optional[int] 

async def route_question_async(state):
    """
    Route question to database or vectorstore
    Args:
        state (dict): The current graph state

    Returns:
        str: Next node to call
    """
    query = state["query"]

    source = await datasource_router.ainvoke({"query": query})
    if source['datasource'] == "direct_database":
        logging.info("Entire database needs to be queried.")
        return "direct_database"
    elif source['datasource'] == "vectorstore":
        logging.info("Querying against vector embeddings...")
        return "vectorstore"
    
async def generate_for_whole_db_async(state):
    """
    Filter database
    
    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key may be added to state, generation, which contains the answer for query asked
    """

    query = state["query"]

    logging.info("Generating answer...")

    document_dict = dict()
    retrieved_dict = await query_retriever.ainvoke({'query': query, 'chat_history': [], 'agent_scratchpad' : []})
    document_dict['mongodb_query'] = retrieved_dict['intermediate_steps'][0][0].tool_input['agg_pipeline']
    document_dict['retrieved_output'] = retrieved_dict['intermediate_steps'][0][1]
    documents = await asyncio.to_thread(json.dumps, document_dict)

    return {"query": query, "documents": documents}

async def filter_generator_async(state):
    """
    Filter database

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key may be added to state, filter, which contains the MongoDB query that will be applied before retrieval
    """
    logging.info("Determining whether filter is required...")

    query = state["query"]

    result = await filter_generation_chain.ainvoke({"query": query})
    filter = result['filter_query']
        
    logging.info(f"Database will be filtered using: {filter}")
    return {"filter": filter, "query": query}
 
async def retrieve_async(state):
    """
    Retrieve documents

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, documents, that contains retrieved documents
    """
    logging.info("Retrieving documents...")
    query = state["query"]
    filter = state["filter"]

    # Retrieval

    retriever = DocDBRetriever(k = 10)
    documents = await retriever.aget_relevant_documents(query = query, query_filter = filter)
    return {"documents": documents, "query": query}

async def grade_doc_async(query, doc: Document):
    score = await doc_grader.ainvoke({"query": query, "document": doc.page_content})
    grade = score['binary_score']
    logging.info(f"Retrieved document matched query: {grade}")
    if grade == "yes":
        logging.info("Document is relevant to the query")
        relevant_context = score['relevant_context']
        return relevant_context
    else:
        logging.info("Document is not relevant and will be removed")
        return None
        

async def grade_documents_async(state):
    """
    Determines whether the retrieved documents are relevant to the question.

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): Updates documents key with only filtered relevant documents
    """

    logging.info("Checking relevance of documents to question asked...")
    query = state["query"]
    documents = state["documents"]

    filtered_docs = await asyncio.gather(*[grade_doc_async(query, doc) for doc in documents])
    filtered_docs = [doc for doc in filtered_docs if doc is not None]
    return {"documents": filtered_docs, "query": query}

async def generate_db_async(state):
    """
    Generate answer

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, generation, that contains LLM generation
    """ 
    logging.info("Generating answer...")
    query = state["query"]
    documents = state["documents"]

    #doc_text = "\n\n".join(doc.page_content for doc in documents)

    # RAG generation
    generation = await db_rag_chain.ainvoke({"documents": documents, "query": query})
    return {"documents": documents, "query": query, "generation": generation, "filter": state.get("filter", None)}

async def generate_vi_async(state):
    """
    Generate answer

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, generation, that contains LLM generation
    """
    logging.info("Generating answer...")
    query = state["query"]
    documents = state["documents"]

    # RAG generation
    generation = await rag_chain.ainvoke({"documents": documents, "query": query})
    return {"documents": documents, "query": query, "generation": generation, "filter": state.get("filter", None)}

async_workflow = StateGraph(GraphState) 
async_workflow.add_node("database_query", generate_for_whole_db_async)  
async_workflow.add_node("filter_generation", filter_generator_async)  
async_workflow.add_node("retrieve", retrieve_async)  
async_workflow.add_node("document_grading", grade_documents_async)  
async_workflow.add_node("generate_db", generate_db_async)  
async_workflow.add_node("generate_vi", generate_vi_async)  

async_workflow.add_conditional_edges(
    START,
    route_question_async,
    {
        "direct_database": "database_query",
        "vectorstore": "filter_generation",
    },
)
async_workflow.add_edge("database_query", "generate_db") 
async_workflow.add_edge("generate_db", END)
async_workflow.add_edge("filter_generation", "retrieve")
async_workflow.add_edge("retrieve", "document_grading")
async_workflow.add_edge("document_grading","generate_vi")
async_workflow.add_edge("generate_vi", END)

async_app = async_workflow.compile()

# async def main():
#     query = "How many records are stored in the database?"
#     inputs = {"query": query}
#     answer = await async_app.ainvoke(inputs)
#     return answer['generation']

# #Run the async function
# print(asyncio.run(main()))
