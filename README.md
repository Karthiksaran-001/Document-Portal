# Project Setup:

1. Install Environment
```pip install uv```
```uv venv --python 3.10```

2. Add Requirements
```uv pip install -r requirements.txt```

3. To Run the UI
```uvicorn api.main:app --port port_num --reload```

![App Screenshot](![alt text](app_screenshot.png))

### NOTE:
By Default It takes GROQ Model, If you want to use Google set the Environment Variable to Google

```set LLM_PROVIDER =google```