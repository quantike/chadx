# chadx

Inject targeted advertising into your chatbots

## Project Features
- chadx-ui: chatbot for users (aka betas)
- chadmin-ui: matching engine internals
- chadxperience: form for Chadvertisers to create ad campaigns
- docs
- ad copy upload for sponsors

## Running

### Starting the `chadx` ad-exchange

Start the ad-exchange by

```
uv run fastapi
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
