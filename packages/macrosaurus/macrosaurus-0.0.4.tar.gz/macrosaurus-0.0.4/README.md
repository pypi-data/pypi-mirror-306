
> [!WARNING]
> Project is in its early stage of development. Current version is not stable.

# *🦖 macrosaurus
Versatile AI client that works out of the box. Powered by OpenAI's Python SDK behind the scenes to handle dozens of AI providers without all the complexity. 

Supports the following out of the box:
- OpenAI
- SambaNova
- Anthropic
- Cohere
- Fireworks
- Together
- Vertex AI

## 📦 Setup
```shell
pip install macrosaurus
```

## 🛠️ Usage
Set up a base client from one of the supported providers.
```python
from macrosaurus import Client

client = Client(provider="sambanova",
                api_key="API_KEY")
```
Extend these clients with better functionality.
```python
from macrosaurus.llm import LLM

llm = LLM(client, model="Meta-Llama-3.2-3B-Instruct")
for chunk in llm.stream("Tell me a joke"):
    print(chunk, end="")

```
Want to add your own Provider?
```python
from macrosaurus.providers import Provider
from macrosaurus import Client

perplexity = Provider(name="Perplexity", endpoint="https://api.perplexity.ai")
client = Client(provider=perplexity, api_key="API_KEY")
```

*Docs to be continued...*

## 🎯 Motivation
Handling LLMs or AI models from different providers *should* be easy. Made this because it wasn't. `Macrosaurus` is dirt simple and has tools that makes the development process nicer. Why not use `LangChain` instead? It's not built for production. `Macrosaurus` was also originally built for `Openmacro`.