# arm_doc_chat
This package allows users to upload files, parse and divide their content into manageable chunks, calculate embeddings for each chunk, store these embeddings with metadata in a vector database, and answer user queries by retrieving and providing relevant chunks to a language model (LLM).

## Table of Contents
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Main Components](#main-components)
- [Pipeline](#pipeline)
- [Usage](#usage)
- [Contributing](#contributing)

## Installation
To install the package, use:
```bash
pip install arm_doc_chat
```

## Quick Start
```py
from llm import Gpt, Claude, Open_Source
from config import CONFIG
from embeddings import Embedding
from vectorstore import Weaviate_DB, Deeplake_DB
from document_processing.chunking import Chunking, Document_parser
```
Initialize components
```py
file_processor = Document_parser()
chunker = Chunking()
embedding_calculator = Embedding()
claude = Claude()
gpt = Gpt()
# For using "Weaviate" vector store:
db = Weaviate_DB()
# For using "DeepLake" vector store:
db = Deeplake_DB()
```
Process a file and save chunks to vector DB
```py
file_path = "path/to/your/file.txt"
parsed_file = file_processor.parse(file_path)
# For simple splitting:
chunks = chunker.simple_splitter(parsed_file)
# For recursive splitting:
chunks = chunker.recursive_splitter(parsed_file)
embeddings = embedding_calculator.encode(chunks)
metadatas = [{'chunk': i, 'filename': chunk[0]} for i, chunk in enumerate(chunks)]
db.add_objects(chunks, embeddings, metadatas)
```
Query the vector DB for similar chunks
```py
query = "Your question here"
query_embedding = embedding_calculator.encode(query)
# If you are using "Weaviate" vector store there are available 3 versions of
# search: semantic_search, keyword_search, hybrid_search. 
# You can mention searching type in config.yaml, default value is hybrid_search.
similar_chunks = db.search(query_embedding, query)
print(similar_chunks)
```

## Main Components
### 1. Document_parser
**Functionality:** Receives files and prepares them for parsing. Acceptable file types are: .pdf, .doc, .docx and zip archive which contains only the above mentioned type files.
**Methods:**
- *parse(file_path)*: Reads and preprocesses file(s) for parsing.
- *parse_archive(archive_path)*: Returns a dict: {filename: content}.
- *parse_file(file_path)*: Parses a single file.
- *read_pdf(path)*: Reads a PDF file.
- *read_txt(path)*: Reads a TXT file.
- *read_docx(path)*: Reads a DOCX file.
- *read_doc(path)*: Reads a DOC file.

### 2. Chunking
**Functionality:** Divides file content into smaller chunks.
**Methods:**
- *simple_splitter(content)*: Splits the content into chunks without taking into account whether the sentence is ended or not.
- *recursive_splitter(content)*: Splits the content into chunks such that in one chunk all sentences are whole and the chunk doesn't exceed the chunk_size.
- *splitter(content)*: Splits the content based on the type specified in the configuration.

### 3. Embedding
**Functionality:** Calculates embeddings for each chunk of content.
**Methods:**
- *encode(chunks)*: Generates embeddings for each content chunk and returns a list of embedding vectors.

### 4. Weaviate_DB, Deeplake_DB
**Functionality:** Stores embeddings and metadata for later retrieval using either Weaviate or DeepLake vector store.
**Methods:**
- *open_db()*: Connects to the DB if it already exists, otherwise creates a new one.
- *close_db()*: Closes DB.
- *add_objects(chunks, embeddings, metadata)*: Saves embeddings and metadata.
- *search(query_embedding, query)*: Finds the closest K chunk(s) to a given query using semantic search.
- *clear_all()*: Clears all the content of the DB.
- *display_collection_contents(limit)*: Prints limit (argument given by user) rows table of the DB's content, including chunk and metadata.
- *check_existence(filename)*: Checks whether filename already exists in the DB or not, returns True if it exists and False otherwise.

### 5. Gpt, Claude, Open_Source
**Functionality:** Handles user queries and interfaces with an LLM to provide answers.
**Methods:**
- *generate_response(query, context)*: Produces an answer via LLM using the given context.

## Pipeline
The `Pipeline` class combines all functionalities into a single interface. You can use the `Pipeline` object to process files, store chunks in the vector database, and answer queries.

### Methods:
- *file_in_db(filename)*: Checks if a file is already in the database.
- *process_file(file_path)*: Processes a file, chunks its content, calculates embeddings, and stores them in the vector database.
- *answer_question(question)*: Answers a question by retrieving relevant chunks from the vector database and generating a response using an LLM.

### Example Usage:
```py
from pipeline import Pipeline

pipeline = Pipeline()

# Process a file
file_path = "path/to/your/file.txt"
pipeline.process_file(file_path)

# Answer a question
question = "Your question here"
answer = pipeline.answer_question(question)
print(answer)
```

## Usage
**Upload a File**: Start by processing file(s) using `Document_parser`.
**Chunking**: Use `Chunking` to break the file into manageable parts.
**Calculate Embeddings**: Calculate embeddings for each chunk using `Embedding`.
**Store in Vector DB**: Save the chunks with their embeddings in `VectorDB`.
**Answer Queries**: Use `Gpt`, `Claude`, or `Open_Source` to generate answers relevant to the query and the uploaded document.

## Contributing
We welcome contributions! Please submit a pull request or open an issue to help improve this package.
