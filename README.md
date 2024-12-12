# semantic-file-retrieval
A semantic file retrieval application based on LLM

## Architecture
![architecture_image](assets/architecture.png)

## Quick Start
1. Install Dependencies
```bash
pip install -r requirements.txt
```

2. Config your GLM api key and chromadb url in local .env file


3. Run the project
```bash
streamlit run main.py
```

## TODO
- [ ] Support audios
- [ ] Support videos
- [ ] Support office documents
- [ ] Support local LLM(ollama)
- [ ] Support retrieve image by image
- [ ] Support batch uploading(upload folders) 
- [ ] Provide restful APIs for customized integration
- [ ] Support Docker deployment
- [ ] Support scanned pdf
- [ ] Support offline processing for large files