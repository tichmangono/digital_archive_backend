#import libraries
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
#import uvicorn
import hypercorn
from typing import Optional
from pydantic import BaseModel
from app.database import (
    get_all_documents,
    get_document_by_id,
    upload_document,
    update_document,
    delete_document,
    get_document_types,
    get_documents_by_type,
    search_documents
)

# Create a class for the document model
class Document(BaseModel):
    name: str
    type: str
    url: str
    category: str
    date_uploaded: str

# Create a FastAPI application
app = FastAPI()

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Make correspnding endpoints for each function above using fastapi library following best practices for REST API design and standards
@app.get('/documents')
def get_all_documents_endpoint():
    return get_all_documents()

@app.get('/documents/{document_id}')
def get_document_by_id_endpoint(document_id: int):
    return get_document_by_id(document_id)

@app.post('/documents')
def upload_document_endpoint(document: Document = Body(...)):
    return upload_document(document)

@app.put('/documents/{document_id}')
def update_document_endpoint(document_id: int, document: Document = Body(...)):
    return update_document(document_id, document)

@app.delete('/documents/{document_id}')
def delete_document_endpoint(document_id: int):
    return delete_document(document_id)

@app.get('/document-types')
def get_document_types_endpoint():
    return get_document_types()

@app.get('/document-types/{document_type}')
def get_documents_by_type_endpoint(document_type: str):
    return get_documents_by_type(document_type)

@app.get('/search')
def search_documents_endpoint(query: str):
    return search_documents(query)

# Run the application
if __name__ == '__main__':
    hypercorn.run(app, host='localhost', port=8080)