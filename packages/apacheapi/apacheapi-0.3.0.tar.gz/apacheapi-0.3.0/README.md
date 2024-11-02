# ApacheLabs

A simplified wrapper for Mistral AI API/Hugging Face so that developers can easily work with Apache Lab Models.

## Current Models
- ApacheLM v3.0 (Mistral Nemo Fine-tune)
- ApacheLM v4.0 (Comming Soon)
- ApacheLM v3.5 (Comming Soon)
- ApacheXL Mini (Comming Soon)
- ApacheXL Dream (Comming Soon)
- ApacheXL Odyssey (Comming Soon)

## Installation

```bash
pip install apachelabs
```
## Usage Example (LLMs)

from apachelabs import lmclient
api_key = "your-api-key"
model = "apachelm-v3"  # Specify the desired model

client = lmclient(api_key, model)

# Start the chat session
client.start_chat()
```

