# CastleGuard Python SDK

The CastleGuard Python SDK provides a convenient interface to interact with CastleGuard's API. This SDK allows you to authenticate, log messages, interact with the chatbot, translate text, perform named entity recognition (NER), transcribe audio files, manage document collections, work with vision-based models, and more.

## Features

- **Authentication**: Easily authenticate and retrieve an access token to interact with CastleGuard APIs.
- **Logging**: Send log messages to CastleGuard's logging endpoint.
- **Chatbot Integration**: Interact with CastleGuard's chatbot to generate responses based on input prompts, with or without document collections.
- **Translation**: Translate text between languages, supporting English and French.
- **Named Entity Recognition (NER)**: Perform NER on text to extract important entities.
- **Vision**: Perform image-based tasks using a vision model by uploading an image with a descriptive prompt.
- **Transcription**: Upload and transcribe audio files, and download SRT subtitles.
- **Collections**: Manage document collections by creating, uploading, and retrieving the status of files.
- **Heartbeat**: Fetch the health status of various system components.
- **Text Extraction**: Extract paragraphs from raw text or extract text from a document file.

## Installation

Install the package via pip:

```bash
pip install castleguard-sdk
```

## Usage

### Initialization

To begin, initialize the `CastleGuard` class with your API credentials:

```python
from castleguard_sdk import CastleGuard

cg = CastleGuard(base_url='https://your-castleguard-url', username='your-username', password='your-password')
```

### Authentication

The class automatically handles authentication. The access token is retrieved upon initialization and used for subsequent API requests.

### Logging

Log a message with a specific log level (default is 1):

```python
cg.log("This is a log message", logLevel=2)
```

### Chatbot Interaction

Send a prompt to the chatbot and get a response:

```python
response, chat_id = cg.chat("What is the weather today?")
print(response)
```

You can also chat within the context of a document collection:

```python
response, chat_id = cg.chat_with_collection("Summarize the document", collection_id="your-collection-id")
print(response)
```

### Text Translation

Translate text from English to French (or specify different languages):

```python
translated_text = cg.translate_text("Hello, how are you?", source_lang="en", target_lang="fr")
print(translated_text)
```

### Named Entity Recognition (NER)

Perform NER on text to extract entities:

```python
entities = cg.named_entity_recognition("John Doe works at Google in Mountain View.")
print(entities)
```

### Vision

Upload an image file and provide a descriptive prompt to perform vision-based tasks:

```python
vision_result = cg.vision(prompt="Detect objects in this image", file_path="/path/to/image.jpg")
print(vision_result)
```

### Transcription

Upload an audio file and transcribe it:

```python
document_id = cg.transcribe("/path/to/audiofile.mp3")
srt_text = cg.download_srt(document_id)
print(srt_text)
```

### Document Collections

Create a new document collection:

```python
collection_id = cg.create_collection(name="My Collection", description="A collection of legal documents")
print(f"Collection created with ID: {collection_id}")
```

Upload a document to the collection:

```python
upload_success = cg.upload_to_collection(collection_id, "/path/to/document.pdf")
print(f"Upload successful: {upload_success}")
```

### Heartbeat

Fetch the health status of various system components:

```python
heartbeat_status = cg.heartbeat()
print(heartbeat_status)
```

### Text Extraction

Extract paragraphs from raw text:

```python
paragraphs = cg.text_extraction("This is a sample text that needs to be divided into paragraphs.")
print(paragraphs)
```

Extract text from a document file:

```python
extracted_text = cg.text_extraction_from_document("/path/to/document.pdf")
print(extracted_text)
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License.