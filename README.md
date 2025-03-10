# Introduction

This project sets up an application to generate metadata that can be sumbmitted to the "End DEI" website.

## Prerequisites
* Python 3.x with `pip`
* [Ollama](https://ollama.com/download)
* Some models for Ollama (see below)

## Setup

After cloning the repo, navigate to the directory and install the dependencies:
```bash
$ pip install -r requirements.txt
```

Once the dependencies have finished installing, run the program:
```bash
$ python main.py
```

The program will output JSON (in varying formats, depending on the model used). There will be three keys:
* `school_name` - the name of the fake school.
* `zip_code` - the zip code. If you're using a model that supports tools, this zip code will correspond to the state picked by the school faker library. Otherwise it will be a random zip code.
* `summary` - the actual text of the submission.

## Model Support

This app uses Ollama to talk to a specific LLM downloaded on your system. By default it will use the first model listed by `ollama list`, but you can change the model to anything installed locally using the `--model=` or `-m` option:
```bash
$ python main.py --model=gemma2:9b
```

## Tool Support

This app has a tool included that will generate a more plausible-sounding school name, as well as a zip code that matches the (fake) school's state, which is useful if the school name in question has the city or county name. Not all Ollama models support tools, so if the model you've requested does not support it, the tool will be ignored.

## Tested Models

The following models have been tested with this app:

| Model Name | Tool Support | Results |
|------------|--------------|---------|
| `gemma2`   | No           | Works well, but lack of tool support means the responses will probably be shorter and are very likely to be located entirely in the 90210 zip code.|
| `qwen2.5`  | Yes          | Okay output, but it seems to ignore instructions not to end with some whiny opinionating. |
| `llama3.2` | Yes          | Excellent output even from the `3b` model. |