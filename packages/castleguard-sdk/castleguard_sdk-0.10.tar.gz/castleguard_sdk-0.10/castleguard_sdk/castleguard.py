import requests
import json
import time
from datetime import datetime
import re

class CastleGuard:
    def __init__(self, base_url, username, password, default_version="v1"):
        """
        Initialize the CastleGuard class with base credentials.
        
        :param base_url: Base URL for the CastleGuard API.
        :param username: Username for authentication.
        :param password: Password for authentication.
        :param default_version: Default API version to use if not provided in base_url.
        """
        self.base_url = self._normalize_url(base_url, default_version)
        self.username = username
        self.password = password
        self.token = None
        self.authenticate()

    def _normalize_url(self, base_url, default_version):
        """
        Normalize the base URL to ensure it includes an API version.
        
        :param base_url: The base URL provided by the user.
        :param default_version: The default API version to append if none is provided.
        :return: The normalized URL with the correct API version.
        """
        # Check if base_url already contains an API version (e.g., /api/vX where X can be any version)
        if re.search(r'/api/v\d+$', base_url):
            return base_url
        # If base_url ends with a slash, strip it
        if base_url.endswith('/'):
            base_url = base_url.rstrip('/')
        # Append the default version if no version is provided
        return f"{base_url}/api/{default_version}"
    
    def authenticate(self):
        """
        Authenticates the user and retrieves the access token.
        
        :return: Access token or None if authentication fails.
        """
        url = f'{self.base_url}/auth/token'
        payload = {
            "account": self.username,
            "password": self.password
        }

        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                self.token = response.json().get('token')
                if self.token:
                    print("Authentication successful.")
                else:
                    print("Failed to retrieve token from authentication response.")
            else:
                print(f"Failed to authenticate: {response.status_code} - {response.text}")
        except requests.RequestException as e:
            print(f"Authentication request failed: {e}")
            self.token = None

    def log(self, message, logLevel=1):
        """
        Sends log messages to the CastleGuard logging endpoint as URL parameters.
        
        :param message: Log message.
        :param logLevel: Log level (0-6).
        """
        if not self.token:
            print("Cannot log message because authentication failed.")
            return

        url = f'{self.base_url}/logger'
        headers = {
            'Authorization': f'Bearer {self.token}'
        }

        params = {
            'message': message,
            'logLevel': logLevel
        }

        try:
            response = requests.post(url, headers=headers, params=params)
            if response.status_code == 200:
                print(f"Logging: {message}")
            else:
                print(f"Failed to send log: {response.status_code} - {response.text}")
        except requests.RequestException as e:
            print(f"Log request failed: {e}")

    def chat(self, prompt, chat_id=None):
        """
        Interacts with the chat endpoint to generate a response from the model.
        
        :param prompt: The input prompt to send to the model.
        :param chat_id: Optional chat session ID.
        :return: Chatbot response or 'Unknown' if the request fails.
        """
        chat_url = f'{self.base_url}/chat-completion/chat'
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }

        # Reuse the same Chat ID for the same session, or create a new one
        if not chat_id:
            params = {
                "displayName": "Chat " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            chat_response = requests.post(chat_url, headers=headers, params=params)
            if chat_response.status_code == 200:
                chat_id = json.loads(chat_response.text).get('id')
            else:
                self.log("Failed to create chat session", logLevel=3)
                return "Unknown", None

        # Post a message to the chat

        message_url = f'{self.base_url}/chat-completion/completions'
        message_payload = {
            "chatId": chat_id,
            "prompt": prompt,
            "model": "default",  # replace with actual model if needed
            "bestOf": 0,
            "echo": True,
            "frequencyPenalty": 0,
            "logitBias": {},
            "logprobs": 0,
            "maxTokens": 0,
            "n": 0,
            "presencePenalty": 0,
            "seed": 0,
            "stop": True,
            "stream": True,
            "streamOptions": "string",
            "suffix": "string",
            "temperature": 0,
            "topP": 0,
            "user": "string"
        }

        message_response = requests.post(message_url, json=message_payload, headers=headers)
        if message_response.status_code == 200:
            response_dict = json.loads(message_response.text)
            bot_message = response_dict.get('botMessage', {}).get('chatMessage')
            return bot_message, chat_id
        else:
            self.log(f"Failed to get response for prompt: {prompt}", logLevel=3)
            return "Unknown", chat_id

    def chat_with_collection(self, prompt, collection_id=None):
        """
        Interacts with the chat endpoint to generate a response from the model.
        
        :param prompt: The input prompt to send to the model.
        :param chat_id: Optional chat session ID.
        :return: Chatbot response or 'Unknown' if the request fails.
        """
        chat_url = f'{self.base_url}/chat-completion/chat'
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }

        chat_id = None        
        params = {
            "displayName": "Chat " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "collectionId": collection_id
        }
        chat_response = requests.post(chat_url, headers=headers, params=params)
        if chat_response.status_code == 200:
            chat_id = json.loads(chat_response.text).get('id')
            # Post a message to the chat
            message_url = f'{self.base_url}/chat-completion/completions'
            message_payload = {
                "chatId": chat_id,
                "prompt": prompt,
                "model": "default",  # replace with actual model if needed
                "bestOf": 0,
                "echo": True,
                "frequencyPenalty": 0,
                "logitBias": {},
                "logprobs": 0,
                "maxTokens": 0,
                "n": 0,
                "presencePenalty": 0,
                "seed": 0,
                "stop": True,
                "stream": True,
                "streamOptions": "string",
                "suffix": "string",
                "temperature": 0,
                "topP": 0,
                "user": "string"
            }

            message_response = requests.post(message_url, json=message_payload, headers=headers)
            if message_response.status_code == 200:
                response_dict = json.loads(message_response.text)
                bot_message = response_dict.get('botMessage')
                chat_message = bot_message.get('chatMessage')
                return chat_message, chat_id
            else:
                self.log(f"Failed to get response for prompt: {prompt}", logLevel=3)
                return "Unknown", chat_id
        else:
            self.log("Failed to create chat session", logLevel=3)
            return "Unknown", None

        
    def translate_text(self, text, source_lang='en', target_lang='fr'):
        """
        Translates text from one language to another.
        
        :param text: The text to translate.
        :param source_lang: Source language code.
        :param target_lang: Target language code.
        :return: Translated text or None if the request fails.
        """
        url = f'{self.base_url}/translation/instant'
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        payload = {
            "originalText": text,
            "sourceLanguageCode": source_lang,
            "targetLanguageCode": target_lang
        }

        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            translated_text = response.text
            #self.log(f"Translated text: {translated_text}", logLevel=1)
            return translated_text
        else:
            self.log(f"Translation failed: {response.text}", logLevel=3)
            return None

    def named_entity_recognition(self, text):
        """
        Performs named entity recognition (NER) on a given text.
        
        :param text: The input text for NER.
        :return: Extracted entities or None if the request fails.
        """
        url = f'{self.base_url}/triton/ner'
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        payload = {
            "inputText": text
        }

        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            ner_result = response.json()
            #self.log(f"NER result: {ner_result}", logLevel=1)
            return ner_result
        else:
            self.log(f"NER extraction failed: {response.text}", logLevel=3)
            return None

# Add the transcription functionalities

    def transcribe(self, file_path):
        """
        Uploads and transcribes an audio/file file.
        
        :param file_path: Path to the file to transcribe.
        :return: Document ID if successful, None otherwise.
        """
        url = f'{self.base_url}/transcription/document'
        headers = {
            'Authorization': f'Bearer {self.token}'
        }
        files = {
            'file': open(file_path, 'rb'),
            'taskType': (None, 'Diarize'),
            'diarizationConfig': (None, 'General')
        }

        response = requests.post(url, headers=headers, files=files)
        if response.status_code == 200:
            document_id = response.json().get('id')
            #self.log(f"File uploaded for transcription. Document ID: {document_id}", logLevel=1)            
            status_code = self.get_transcription_document_status_code(document_id)
            if status_code and status_code == "success":
                return document_id
            return None
        else:
            self.log(f"Failed to upload file for transcription: {response.text}", logLevel=3)            
            return None

    def get_transcription_document_status_code(self, document_id):
        """
        Gets the status of a transcription document.
        
        :param document_id: The ID of the transcription document.
        :return: Status code if successful, None otherwise.
        """
        url = f'{self.base_url}/transcription/document/{document_id}'
        headers = {
            'Authorization': f'Bearer {self.token}'
        }

        status = None
        while status != 2:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                document = response.json()
                job_detail = document.get('jobDetail', {})
                status = job_detail.get('status', None)
                if status == 2:
                    status_code = job_detail.get('statusCode', None)
                    #self.log(f"Transcription job completed. Status Code: {status_code}", logLevel=1)
                    return status_code
            else:
                self.log(f"Failed to get the transcription document: {response.text}", logLevel=3)            
                return None
            time.sleep(5)

    def download_srt(self, document_id):
        """
        Downloads the SRT file from a transcription document.
        
        :param document_id: The ID of the transcription document.
        :return: SRT text if successful, None otherwise.
        """
        url = f'{self.base_url}/transcription/document/download/{document_id}?downloadDocumentOptions=SRT'
        headers = {
            'Authorization': f'Bearer {self.token}'
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            srt_text = response.text
            #self.log(f"SRT downloaded successfully.", logLevel=1)
            return srt_text
        else:
            self.log(f"Failed to download SRT: {response.text}", logLevel=3)            
            return None

    # Add the collection functionalities

    def create_collection(self, name, description):
        """
        Creates a new collection.
        
        :param name: Collection name.
        :param description: Collection description.
        :return: Collection ID if successful, None otherwise.
        """
        url = f'{self.base_url}/collections/collection'
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        params = {
            "displayName": name,
            "description": description
        }

        response = requests.post(url, headers=headers, params=params)
        if response.status_code == 200:
            collection_id = response.json().get('id')
            #self.log(f"Collection created successfully. Collection ID: {collection_id}", logLevel=1)
            return collection_id
        else:
            self.log(f"Failed to create collection: {response.text}", logLevel=3)
            return None

    def upload_to_collection(self, collection_id, file_path):
        """
        Uploads a file to a collection.
        
        :param collection_id: The ID of the collection.
        :param file_path: Path to the file to upload.
        :return: True if successful, False otherwise.
        """
        url = f'{self.base_url}/collections/collection/document/{collection_id}'
        headers = {
            'Authorization': f'Bearer {self.token}'
        }
        files = {
            'file': open(file_path, 'rb')
        }

        response = requests.post(url, headers=headers, files=files)
        if response.status_code == 200:
            document_id = response.json().get('id')
            if document_id:
                status_code = self.get_collection_document_status_code(collection_id, document_id)
                if status_code and status_code.lower() == "success":
                    #self.log(f"File uploaded to collection {collection_id} successfully.", logLevel=1)
                    return True
        else:
            self.log(f"Failed to upload file to collection: {response.text}", logLevel=3)
        return False

    def get_collection_document_status_code(self, collection_id, document_id, interval=5):
        """
        Gets the status of a document in a collection.
        
        :param collection_id: The ID of the collection.
        :param document_id: The ID of the document.
        :return: Status code if successful, None otherwise.
        """
        url = f'{self.base_url}/collections/collection/documents/{collection_id}'
        headers = {
            'Authorization': f'Bearer {self.token}'
        }

        status = None
        while status != 2:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                documents = response.json()
                for document in documents:
                    if document.get('id') == document_id:
                        job_detail = document.get('jobDetail', {})
                        status = job_detail.get('status', None)
                        if status == 2:
                            status_code = job_detail.get('statusCode', None)
                            #self.log(f"Collection document processing completed. Status Code: {status_code}", logLevel=1)
                            return status_code
            else:
                self.log(f"Failed to get collection document status: {response.text}", logLevel=3)
                return None
            time.sleep(interval)

    def vision(self, prompt, file_path):
        """
        Sends a request to the vision endpoint for image-related tasks.
        
        :param prompt: A descriptive prompt for the vision model, sent as a parameter.
        :param file_path: Path to the image file to send in the request body.
        :return: Response from the vision model or None if the request fails.
        """
        url = f'{self.base_url}/triton/vision'
        headers = {
            'Authorization': f'Bearer {self.token}'
        }
        files = {
            'file': open(file_path, 'rb')
        }

        # Include the prompt as a parameter in the URL
        params = {
            'prompt': prompt
        }

        try:
            response = requests.post(url, headers=headers, params=params, files=files)
            if response.status_code == 200:
                vision_result = response.text
                return vision_result
            else:
                self.log(f"Vision request failed: {response.status_code} - {response.text}", logLevel=3)
                return None
        except requests.RequestException as e:
            self.log(f"Vision request failed: {e}", logLevel=3)
            return None
        
    def heartbeat(self):
        """
        Fetches the health status of various system components.
        
        :return: A dictionary with the status of each component or None if the request fails.
        """
        url = f'{self.base_url}/heartbeat'
        headers = {
            'Authorization': f'Bearer {self.token}'
        }

        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                self.log(f"Failed to get heartbeat: {response.status_code} - {response.text}", logLevel=3)
                return None
        except requests.RequestException as e:
            self.log(f"Heartbeat request failed: {e}", logLevel=3)
            return None

    def text_extraction(self, raw_text):
        """
        Extracts paragraphs from the provided raw text.
        
        :param raw_text: The raw text to extract paragraphs from.
        :return: A list of paragraphs or None if the request fails.
        """
        url = f'{self.base_url}/text-extraction'
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        payload = {
            "rawText": raw_text
        }

        try:
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                return response.json().get("paragraphs", [])
            else:
                self.log(f"Text extraction failed: {response.status_code} - {response.text}", logLevel=3)
                return None
        except requests.RequestException as e:
            self.log(f"Text extraction request failed: {e}", logLevel=3)
            return None

    def text_extraction_from_document(self, file_path):
        """
        Extracts text from a binary document file.
        
        :param file_path: Path to the binary file to extract text from.
        :return: Extracted text or None if the request fails.
        """
        url = f'{self.base_url}/text-extraction/document'
        headers = {
            'Authorization': f'Bearer {self.token}'
        }
        files = {
            'file': open(file_path, 'rb')
        }

        try:
            response = requests.post(url, headers=headers, files=files)
            if response.status_code == 200:
                return response.json()
            else:
                self.log(f"Text extraction from document failed: {response.status_code} - {response.text}", logLevel=3)
                return None
        except requests.RequestException as e:
            self.log(f"Text extraction from document request failed: {e}", logLevel=3)
            return None

