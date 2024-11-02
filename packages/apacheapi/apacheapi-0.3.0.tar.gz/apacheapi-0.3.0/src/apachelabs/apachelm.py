from mistralai import Mistral
from mistralai.models.sdkerror import SDKError

class lmclient:
    def __init__(self, api_key, model="apachelm-v3"):
        """
        Initialize the lmclient class with an API key and model.
        
        This serves as a wrapper for interacting with the Mistral API,
        abstracting away the complexities of direct API calls.
        
        :param api_key: The API key for authenticating requests.
        :param model: The short name of the model (default is 'apachelm-v3').
        """
        self.api_key = api_key
        self.model = model
        self.client = Mistral(api_key=api_key)

    def _get_model_id(self):
        """
        Retrieve the full model ID based on the provided short model name.
        
        This method abstracts the logic of retrieving the model ID from a dictionary,
        so the user doesn't need to worry about the full model ID format.
        
        :return: A properly formatted model ID string.
        """
        model_map = {
            "apachelm-v3": "ag:332133fc:20241102:apachelm-v3:de8afc4d",
            # Add other mappings here if necessary
        }
        
        full_model_id = model_map.get(self.model)
        
        if full_model_id:
            return full_model_id
        else:
            raise ValueError(f"Model '{self.model}' not found. Please provide a valid model name.")

    def complete(self, messages):
        """
        Send a chat completion request to the Mistral API.
        
        This method wraps the underlying API call to `Mistral.chat.complete()`,
        hiding the complexity of interacting with the API and handling errors gracefully.
        
        :param messages: A list of messages in the conversation history.
        :return: The response from the Mistral API.
        """
        # Retrieve the full model ID
        full_model_name = self._get_model_id()
        
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

# Example usage
if __name__ == "__main__":
    # Define the API key (hardcoded, no user input)
    api_key = "YOUR_API_KEY"  # Replace with your actual API key
    model = "apachelm-v3"  # Specify the desired model

    # Initialize the client with the provided API key and model
    client = lmclient(api_key, model)

    # Start the chat session
    client.start_chat()