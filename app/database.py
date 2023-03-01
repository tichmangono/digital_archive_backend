# import the necessary packages for the functions below
from flask import Flask, request, redirect, url_for, render_template, flash
from werkzeug.utils import secure_filename
from google.cloud import datastore
from google.cloud import storage
import datetime
import os

# Set the environment variable for the google cloud storage bucket
#os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'C:/Users/USER/Downloads/My First Project-9b9b9b9b9b9b.json'
# Set the environment variable for the google cloud storage bucket
#os.environ['GOOGLE_CLOUD_PROJECT'] = 'My First Project-9b9b9b9b9b9b'

# Set the environment variable for the google cloud storage bucket
bucket_name = 'my-first-bucket-9b9b9b9b9b9b'
# Create a Cloud Storage client
storage_client = storage.Client()
# Get the Cloud Storage bucket
bucket = storage_client.get_bucket(bucket_name)


# Make a python function that returns a list of all documents from google datastore service using client library including metadata such as document ID, name, type, url link, category, and date uploaded
def get_all_documents():
    client = datastore.Client()
    query = client.query(kind='Document')
    query.order = ['date_uploaded']
    results = list(query.fetch())
    return results

# Make a python function that Returns the metadata and file data for a specific document with the given ID from google datastore service using client library including metadata such as document ID, name, type, url link, category, and date uploaded
def get_document_by_id(document_id):
    client = datastore.Client()
    key = client.key('Document', int(document_id))
    document = client.get(key)
    return document

# Make a python function that Accepts a new document to be uploaded to google cloud storage using client library. the file will take in the file data as well as any relevant metadata (such as document type and name) which is loaded to google datastore service using client library including metadata such as document ID, name, type, url link, category, and date uploaded
def upload_document(document):
    client = datastore.Client()
    # Get the file
    file = request.files['file']
    # Get the name of the file
    filename = secure_filename(file.filename)
    # Upload the file to Google Cloud Storage
    blob = bucket.blob(filename)
    blob.upload_from_string(
        file.read(),
        content_type=file.content_type
    )
    # Create a Cloud Datastore entity to hold the document information
    document_entity = datastore.Entity(client.key('Document'))
    # Set the Cloud Datastore entity key to the Cloud Storage file path
    document_entity.update({
        'name': filename,
        'type': file.content_type,
        'url': blob.public_url,
        'category': document['category'],
        'date_uploaded': datetime.datetime.now()
    })
    # Save the Cloud Datastore entity
    client.put(document_entity)
    return document_entity

# Make a python function that Allows a client to update the metadata associated with a specific document, such as changing the document name or type. which is loaded to google datastore service using client library including metadata such as document ID, name, type, url link, category, and date uploaded. This function will also update the file data in google cloud storage if a new file is provided, writing over the old file data
def update_document(document_id, document):
    client = datastore.Client()
    # Get the file
    file = request.files['file']
    # Get the name of the file
    filename = secure_filename(file.filename)
    # Upload the file to Google Cloud Storage
    blob = bucket.blob(filename)
    blob.upload_from_string(
        file.read(),
        content_type=file.content_type
    )
    # Create a Cloud Datastore key
    key = client.key('Document', int(document_id))
    # Get the Cloud Datastore entity
    document_entity = client.get(key)
    # Update the Cloud Datastore entity
    document_entity.update({
        'name': filename,
        'type': file.content_type,
        'url': blob.public_url,
        'category': document['category'],
        'date_uploaded': datetime.datetime.now()
    })
    # Save the Cloud Datastore entity
    client.put(document_entity)
    return document_entity  


# Make a python function that Allows a client to delete a specific document from google cloud storage and delete the corresponding metadata for the document in google datastore service using client library including metadata such as document ID, name, type, url link, category, and date uploaded
def delete_document(document_id): 
    # Get the document
    document = get_document_by_id(document_id)
    # Delete the document from Google Cloud Storage
    blob = bucket.blob(document['name'])
    blob.delete()
    # Delete the document from Google Cloud Datastore
    client = datastore.Client()

# Make a python function that : Returns a list of all available document types from google datastore service using client library including metadata such as document ID, name, type, url link, category, and date uploaded
def get_document_types():
    client = datastore.Client()
    query = client.query(kind='DocumentType')
    query.order = ['name']
    results = list(query.fetch())
    return results

# Make a python function that : Returns the metadata and file data for all documents of a specific document type from google datastore service using client library including metadata such as document ID, name, type, url link, category, and date uploaded
def get_documents_by_type(document_type):
    client = datastore.Client()
    query = client.query(kind='Document')
    query.add_filter('type', '=', document_type)
    query.order = ['date_uploaded']
    results = list(query.fetch())
    return results

# Make a python function that :Returns a list of documents that match the given search query. The search query can be matched against any relevant metadata (such as document name or type) from google datastore service using client library including metadata such as document ID, name, type, url link, category, and date uploaded
def search_documents(query):
    client = datastore.Client()
    query = client.query(kind='Document')
    query.add_filter('name', '>=', query)
    query.add_filter('name', '<', query + u'\ufffd')
    query.order = ['name']
    results = list(query.fetch())
    return results

