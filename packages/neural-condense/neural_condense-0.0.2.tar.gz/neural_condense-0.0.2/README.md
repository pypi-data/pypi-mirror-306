<div align="center">
  <h1>🚀 Organic API Usage for Neural Condense Subnet 🌐</h1>
  <p>Empowered by <b>Bittensor</b></p>
</div>

---

## 🌟 Overview
The Neural Condense Subnet (NCS) library provides an efficient and intuitive interface to compress extensive input contexts into concise, high-relevance formats. This optimization is especially beneficial when working with large language models (LLMs) that have token limitations, as it allows you to maximize the use of input constraints, enhancing inference efficiency.

## 📦 Installation
Install the library using pip:
```bash
pip install neural-condense
```

## 🛠️ Usage

### Quick Start in Python

This example demonstrates how to initialize the `CondenseClient`, define a message context, generate condensed tokens, and apply them in an LLM pipeline.
1. Get condense your long messages into condensed tokens.
```python
from neural_condense import CondenseClient, SAT_TOKEN
import numpy as np

# Initialize the client with your API key
client = CondenseClient(
  api_key="your_api_key", 
  model_name="mistralai/Mistral-7B-Instruct-v0.2"
)

# Define a long context and focused prompt
messages = [
  {
    "role": "user",
    "content": "Many of you think that EPL and other salary levels are similar, but you are wrong. In EPL, the media glosses over pre-tax salary information, while in Serie A they deal with salary. That means the salary that Milan must pay Donnarumma if they agree to sign the contract is 24m/season + 20m in salary. No one pays that much money for a goalkeeper... What is the salary that Milan must pay Donnarumma if they agree to sign the contract?"
  },
  {
    "role": "assistant",
    "content": f"The salary that Milan must pay Donnarumma if they agree to sign the contract is 24m/season + 20m in salary. {SAT_TOKEN}"
  },
  {
    "role": "user",
    "content": "Who is Donnarumma?"
  }
]

# Generate condensed tokens
condensed_output = client.create_condensed_tokens(
    messages=messages,
    tier="inference_0", 
)

# Check the shape of the condensed tokens
print(f"Condensed tokens shape: {condensed_output.condensed_tokens.shape}")

```

2. Apply the condensed tokens in an LLM pipeline.
```python
# Example: Using the condensed tokens in an LLM pipeline
from transformers import pipeline

# Initialize language model (Hugging Face transformers)
llm = pipeline("text-generation", model="mistralai/Mistral-7B-Instruct-v0.2")

# Use condensed embeddings as input
output = llm(inputs_embeds=condensed_output.inputs_embeds, max_new_tokens=100)

print(output)
```

### Asynchronous Usage 🌐

For asynchronous contexts, use `AsyncCondenseClient` to handle requests without blocking execution.

```python
from neural_condense import AsyncCondenseClient
import asyncio

async def main():
    client = AsyncCondenseClient(api_key="your_api_key")
    condensed_output = await client.create_condensed_tokens(
        messages=messages,
        tier="inference_0", 
        target_model="mistralai/Mistral-7B-Instruct-v0.2"
    )
    print(f"Condensed tokens shape: {condensed_output.inputs_embeds.shape}")

asyncio.run(main())
```

---

## 🔍 Additional Information

### Supported Models
The library supports a variety of pre-trained models available through Hugging Face's model hub. Ensure that the model you choose is compatible with the Neural Condense Subnet’s framework.

### SAT_TOKEN
The `SAT_TOKEN` acts as a delimiter within your message templates, separating context and prompts. This token helps guide the API in recognizing specific sections of input messages, optimizing them for compression.

### API Parameters
- **tier**: Specify the inference tier, which affects the quality and speed of token condensation.
- **target_model**: Set the target model to shape the condensed output according to the requirements of the chosen language model.
