from mistralai import Mistral
from mistralai.models.sdkerror import SDKError

class ApacheHelm:
    def __init__(self, api_key, model="apachelm-v3"):
        """
        Initialize the ApacheHelm class with an API key and model.
        
        This serves as a wrapper for interacting with the Mistral API,
        abstracting away the complexities of direct API calls.
        
        :param api_key: The API key for authenticating requests.
        :param model: The short name of the model (default is 'apachelm-v3').
        """
        self.api_key = api_key
        self.model = model
        self.client = Mistral(api_key=api_key)
    
    @staticmethod
    def _format_model_name(model_name):
        """
        Convert a short model name to the full Mistral model ID.
        
        This method abstracts the logic of formatting the model name into the required
        structure, so the user doesn't need to worry about it.
        
        :param model_name: The short name of the model.
        :return: A properly formatted model name string.
        """
        return f"ag:332133fc:20241102:{model_name}:de8afc4d"
    
    def complete(self, messages):
        """
        Send a chat completion request to the Mistral API.
        
        This method wraps the underlying API call to `Mistral.chat.complete()`,
        hiding the complexity of interacting with the API and handling errors gracefully.
        
        :param messages: A list of messages in the conversation history.
        :return: The response from the Mistral API.
        """
        # Format the model name
        full_model_name = self._format_model_name(self.model)
        
        try:
            # Make the API call (wrapped)
            response = self.client.chat.complete(
                model=full_model_name,
                messages=messages
            )
            return response
        
        except SDKError as e:
            # Error handling is done within the wrapper
            print(f"API Error: {e}")
            if e.status_code == 401:
                print("Unauthorized access. Please check your API key.")
            elif e.status_code == 403:
                print("Forbidden access. You might not have permissions for this model.")
            else:
                print("An API error occurred.")
            raise  # Re-raise the exception after logging it
    
    def start_chat(self):
        """
        Start an interactive chat session in the terminal.
        
        This method provides a higher-level abstraction for interacting with the Mistral API.
        It collects user messages, sends them to the API, and prints responses.
        
        Type '/bye' to exit the chat.
        """
        print("Chat started. Type '/bye' to exit.")
        messages = []  # This will store the conversation history
        
        while True:
            try:
                # Get input from the user
                user_input = input("You: ").strip()
                if user_input.lower() == "/bye":
                    print("Ending chat. Goodbye!")
                    break
                
                # Append user message to conversation history
                messages.append({"role": "user", "content": user_input})
                
                # Get the assistant's response (using the wrapper method `complete`)
                chat_response = self.complete(messages)
                assistant_response = chat_response.choices[0].message.content
                
                # Display assistant's response and append to message history
                print(f"Assistant: {assistant_response}")
                messages.append({"role": "assistant", "content": assistant_response})
            
            except SDKError:
                # Gracefully handle API errors that occur during chat
                print("An error occurred while communicating with the assistant.")
                break
            except Exception as e:
                # Catch any other unexpected errors and log them
                print(f"An unexpected error occurred: {e}")
                break