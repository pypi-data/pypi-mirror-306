import requests

class NovaClient:
    """
    NovaClient is a client SDK for Nova, providing an interface to interact with various AI services.

    Attributes:
        team_id (str): The team ID used to fetch API keys.
        api_keys (dict): A dictionary containing the API keys.
        server_url (str): The base URL of the Nova server.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(NovaClient, cls).__new__(cls)
        return cls._instance

    def __init__(self, team_id, server_url):
        """
        Initialize the NovaClient with a team ID or API keys.

        Args:
            team_id (str): The team ID to fetch API keys.
            server_url (str): The url to send requests to.
        """
        if hasattr(self, 'initialized') and self.initialized:
            return
        self.initialized = True

        self.server_url = server_url

        self.api_keys = {}

        self.team_id = team_id
        self._load_api_keys_from_server(team_id)

    def _load_api_keys_from_server(self, team_id):
        """
        Load API keys from the server using the team ID.

        Args:
            team_id (str): The team ID to fetch API keys.
        """
        url = f'{self.server_url}/keys'
        params = {'team_id': team_id}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            self.api_keys = response.json()
        else:
            raise Exception(f"Failed to load API keys: {response.status_code} {response.text}")

    def process_message(self, message, output_modality):
        """
        Process a message and get the response in the desired output modality.

        Args:
            message (Message): The input message.
            output_modality (str): The desired output modality ('text', 'image', 'audio').

        Returns:
            The processed output from the server.
        """
        url = f'{self.server_url}/process_message'
        data = {
            'text': message.text,
            'output_modality': output_modality
        }
        files = []

        if message.has_images():
            for img_path in message.images:
                files.append(('images', open(img_path, 'rb')))
        if message.has_audio():
            for aud_path in message.audio:
                files.append(('audio', open(aud_path, 'rb')))

        headers = {}
        # Include API keys in headers or params if needed

        response = requests.post(url, data=data, files=files, headers=headers)

        # Close the files
        for _, file_obj in files:
            file_obj.close()

        if response.status_code == 200:
            if output_modality == 'text':
                return response.text
            else:
                return response.content  # Adjust based on actual response
        else:
            raise Exception(f"Failed to process message: {response.status_code} {response.text}")

class Message:
    """
    Represents a message containing text, images, and audio.

    Attributes:
        text (str): The text content of the message.
        images (list): A list of image file paths.
        audio (list): A list of audio file paths.
    """

    def __init__(self, text=None, images=None, audio=None):
        """
        Initialize a Message object.

        Args:
            text (str, optional): The text content.
            images (list, optional): A list of image file paths.
            audio (list, optional): A list of audio file paths.
        """
        self.text = text
        self.images = images or []
        self.audio = audio or []

    def has_text(self):
        """Check if the message contains text."""
        return self.text is not None

    def has_images(self):
        """Check if the message contains images."""
        return len(self.images) > 0

    def has_audio(self):
        """Check if the message contains audio."""
        return len(self.audio) > 0

class TextToSpeech:
    """
    TextToSpeech class provides text-to-speech functionality.

    Attributes:
        provider (str): The provider to use ('cartesia', 'hume').
    """

    def __init__(self, nova_client, provider='cartesia'):
        """
        Initialize TextToSpeech with a provider.

        Args:
            nova_client (NovaClient): The NovaClient client to use for requests.
            provider (str, optional): The provider to use ('cartesia', 'hume').
        """
        self.nova_client = nova_client
        self.provider = provider

    def synthesize(self, text):
        """
        Synthesize speech from text.

        Args:
            text (str): The text to synthesize.

        Returns:
            The synthesized audio content.
        """
        url = f'{self.nova_sdk.server_url}/text_to_speech'
        data = {
            'text': text,
            'provider': self.provider
        }
        headers = {}
        response = requests.post(url, data=data, headers=headers)

        if response.status_code == 200:
            return response.content  # Assuming the audio content is returned
        else:
            raise Exception(f"Failed to synthesize speech: {response.status_code} {response.text}")
