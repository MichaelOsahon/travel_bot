# README

travel.bot allows users to get information on the number of flights flying over any chosen country at the time of the request. It uses OpenAI and the OpenSky Network to pull the required data for each inquiry.

## requisites

Use pip to install requirements.txt

```bash
pip install requirements.txt
```

Set up your Azure key and endpoint

```bash
set AZURE_KEY=your_key
```

```bash
set AZURE_ENDPOINT=your_endpoint
```


## Usage

- set up AZURE_KEY and AZURE_ENDPOINT as instructed above

- Run bot_final.py and ask it a question like "How many flood warnings are there in Wiltshire at the moment?"