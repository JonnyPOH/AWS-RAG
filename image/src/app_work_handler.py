import logging
from query_model import QueryModel
from rag_app.query_rag import query_rag

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def handler(event, context):
    logging.info("Handler invoked with event: %s", event)
    try:
        query_item = QueryModel(**event)
        invoke_rag(query_item)
        logging.info("Handler execution completed successfully.")
    except Exception as e:
        logging.error("Error in handler: %s", str(e), exc_info=True)

def invoke_rag(query_item: QueryModel):
    logging.info("Invoking RAG process for query: %s", query_item.query_text)
    try:
        # Query RAG
        rag_response = query_rag(query_item.query_text)

        # Log the RAG response
        logging.debug("RAG response: %s", rag_response)

        # Update QueryModel fields
        query_item.answer_text = rag_response.response_text
        query_item.sources = rag_response.sources
        query_item.is_complete = True

        # Simulate saving the updated QueryModel
        query_item.put_item()
        logging.info("Query item successfully updated: %s", query_item)

        return query_item
    except Exception as e:
        logging.error("Error in invoke_rag: %s", str(e), exc_info=True)
        raise

def main():
    logging.info("Running example RAG call.")
    try:
        query_item = QueryModel(
            query_text="How long does an e-commerce system take to build?"
        )
        response = invoke_rag(query_item)
        logging.info("Received response: %s", response)
    except Exception as e:
        logging.error("Error in main: %s", str(e), exc_info=True)

if __name__ == "__main__":
    # For local testing
    main()
