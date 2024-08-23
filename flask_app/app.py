from flask import Flask, request, jsonify
from llm_search_template.flask_app import utils
from llm_search_template.flask_app import webscraper
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
import os
from ..logger_config import logger
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

try:
    chat_model = ChatOpenAI(model_name="gpt-4o", api_key=os.getenv("OPENAI_API_KEY"))
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma(embedding_function=embeddings, persist_directory=None)
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True, output_key="answer")
except Exception as e:
    logger.error(f"Error initializing components: {e}")
    raise

@app.route('/query', methods=['POST'])
async def process_query():
    try:
        data = request.json
        query = data.get('query')
        if not query:
            return jsonify({"error": "Query not provided"}), 400
        
        logger.info(f"Received query: {query}")
        
        search_results = utils.google_search(query)
        logger.info(f"Search results: {search_results}")
        
        for url in search_results:
            try:
                scraper = webscraper.WebScraper(url)
                content = await scraper.scraping_with_langchain()
                
                text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
                texts = text_splitter.split_text(content)
                
                vectorstore.add_texts(texts, metadatas=[{"source": url} for _ in texts])
                logger.info(f"Processed and added texts from {url}")
            except Exception as e:
                logger.warning(f"Error processing URL {url}: {e}")
        
        retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

        qa_chain = ConversationalRetrievalChain.from_llm(
            llm=chat_model,
            retriever=retriever,
            memory=memory,
            return_source_documents=True
        )
        
        result = qa_chain({"question": query})
        
        response = result['answer']
        sources = list(set([doc.metadata['source'] for doc in result.get('source_documents', [])]))
        
        logger.info(f"Returning response: {response} with sources: {sources}")
        
        return jsonify({
            "response": response,
            "sources": sources
        })

    except Exception as e:
        logger.error(f"Error processing request: {e}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True)
