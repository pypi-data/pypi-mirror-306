# orign-py

A Python client for [Orign](https://github.com/agentsea/orign)

## Installation

```bash
pip install orign
```

Install the Orign CLI

```sh
curl -fsSL -H "Cache-Control: no-cache" https://storage.googleapis.com/orign/releases/install.sh | bash
```

Login to Orign

```sh
$ orign login
```

## Usage

Get a list of available models

```sh
$ orign get models
```

### Chat

Define which model we would like to use

```python
from orign import ChatModel

model = ChatModel(model="allenai/Molmo-7B-D-0924", provider="vllm")
```

Open a socket connection to the model

```python
await model.connect()
```

Chat with the model

```python
async for response in model.chat(msg="What's in this image?", image="https://tinyurl.com/2fz6ms35"):
    print(response)
```

Stream tokens from the model

```python
async for response in model.chat(msg="What is the capital of France?", stream_tokens=True):
    print(response)
```

Send a thread of messages to the model

```python
async for response in model.chat(prompt=[
    {"role": "user", "content": "What is the capital of France?"},
    {"role": "assistant", "content": "Paris"},
    {"role": "user", "content": "When was it built?"}
]):
    print(response)
```

Send a batch of threads to the model

```python
async for response in model.chat(batch=[
    [{"role": "user", "content": "What is the capital of France?"}, {"role": "assistant", "content": "Paris"}, {"role": "user", "content": "When was it built?"}],
    [{"role": "user", "content": "What is the capital of Spain?"}, {"role": "assistant", "content": "Madrid"}, {"role": "user", "content": "When was it built?"}]
]):
    print(response)
```

### Embeddings
Define which model we would like to use

```python
from orign import EmbeddingModel

model = EmbeddingModel(provider="sentence-tf", model="clip-ViT-B-32")
```

Embed a text

```python
await model.embed(text="What is the capital of France?")
```

Embed an image

```python
await model.embed(image="https://example.com/image.jpg")
```

Embed text and image

```python
await model.embed(text="What is the capital of France?", image="https://example.com/image.jpg")
```

### OCR

Define which model we would like to use

```python
from orign import OCRModel

model = OCRModel(provider="easyocr")
```

Detect text in an image

```python
await model.detect(image="https://example.com/image.jpg")
```
