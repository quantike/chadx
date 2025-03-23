# chadx

Inject targeted advertising into your chatbots

## Project Features
- chadx-ui: chatbot for users (aka betas)
- chadmin-ui: matching engine internals
- docs
- ad copy upload for sponsors
- chadxperience: form for Chadvertisers to create ad campaigns

## Running

### Starting the `chadx` ad-exchange

Start the ad-exchange api by

```
uv run uvicorn app.main:app
```

### Starting `chadx` chat interface

Start a chat bot UI by

```
uv run python app/chat.py
```

Go to the output link.


### Starting the \`chadxperience\` campaign creator
```
uv run gradio app/chadxperience.py --demo-name=chadxperience
```

## Chadxperience Tiers
0: lowest price, subtle chads
1: more expensive, banner chads
2: most expensive, hijack chads
