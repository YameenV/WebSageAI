# WebSage AI (LLM-Powered Web Search and QA System)

## Introduction

This project implements an advanced question-answering system that leverages Large Language Models (LLMs) and web scraping to provide accurate and up-to-date answers. By combining the power of language models with real-time web data, this system offers a unique approach to information retrieval and question answering.

## Features

- **Real-time Web Search**: Utilizes Google Search  to find relevant web pages for each query.
- **Custom Web Scraping**: Implements an asynchronous web scraper to extract content from search results.
- **Vector Store Integration**: Uses Chroma as an in-memory vector store for efficient storage and retrieval of web content.
- **LLM-powered QA**: Leverages OpenAI's GPT models to generate accurate answers based on scraped web content.
- **Conversation Memory**: Maintains context across multiple queries using a conversation buffer.
- **Dual Interface**: Offers both a Flask API for backend integration and a Streamlit frontend for user interaction.
- **Logging**: Implements a custom logging system for better debugging and monitoring.

## Custom Components

### 1. WebScraper

The `WebScraper` class in `webscraper.py` provides custom web scraping functionality:

```python
class WebScraper:
    def __init__(self, url: HttpUrl):
        self.url = url

    async def scraping_with_langchain(self, wanted_tags: list[str] = ["h1", "h2", "h3", "span", "p", "a"]) -> str:
        # ... (implementation details)
```

Key features:
- Asynchronous scraping using `AsyncHtmlLoader` from LangChain
- Custom HTML cleaning and content extraction
- Configurable tag selection for targeted content extraction

### 2. In-Memory Vector Store

The application uses Chroma as an in-memory vector store:

```python
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings

embeddings = OpenAIEmbeddings()
vectorstore = Chroma(embedding_function=embeddings, persist_directory="chroma_db")
```

Key features:
- Uses OpenAI embeddings
- Persists data to a local directory ("chroma_db")

### 3. Chat Memory Buffer

The application implements a conversation memory using `ConversationBufferMemory`:

```python
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True, output_key="answer")
```

Key features:
- Stores chat history
- Configures memory key and output key for integration with the conversational chain

### 4. Custom Logger

The `logger_config.py` file sets up a custom logger:

```python
def setup_logger(log_file='app.log', log_level=logging.INFO, max_file_size=50*1024*1024, backup_count=10):
    # ... (implementation details)
```

Key features:
- Rotating file handler with a 50MB limit and 10 backup files
- Configurable log level
- Both file and console logging

## Usage Guide

### Flask API

1. Set up environment:
   - Install required packages: `pip install flask langchain openai chromadb python-dotenv`
   - Set up your OpenAI API key in a `.env` file: `OPENAI_API_KEY=your_api_key_here`

2. Run the Flask application:
   ```
   python app.py
   ```

3. Send a POST request to `/query` endpoint:
   ```
   curl -X POST -H "Content-Type: application/json" -d '{"query":"Your question here"}' http://localhost:5000/query
   ```

4. The API will return a JSON response with the answer and sources.

### Streamlit Frontend

1. Install Streamlit: `pip install streamlit`

2. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

3. Use the web interface:
   - Input a chat name in the sidebar and click "New" to create a new conversation.
   - Select a conversation from the radio button list.
   - Type your query in the chat input at the bottom of the page.
   - View the conversation history and responses in the main chat area.

Note: Ensure that the Flask API is running when using the Streamlit frontend, as it relies on the `/query` endpoint for processing queries.

## Important Notes
- The web scraping functionality should be used responsibly and in compliance with the terms of service of the websites you're scraping.
- Consider implementing rate limiting and error handling for production use.
