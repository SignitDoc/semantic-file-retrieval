# semantic-file-retrieval
A lightweight semantic file retrieval application based on LLM and vector db.

## Architecture
![architecture_image](assets/architecture.png)

## Demo
https://github.com/user-attachments/assets/f1590c6f-5d5c-44c6-8370-591ed66e7452

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
## Docker Deployment
1. Build the docker image
```bash
docker build -t semantic-file-retrieval:latest .
```

2. Run the docker container
```bash
docker run -d -e GLM_API_KEY="your_api_key" -p 8501:8501 semantic-file-retrieval:latest
```
> _All the environment variables in .env file can be overridden by docker run command_

## TODO
- [ ] Support audios
- [ ] Support videos
- [ ] Support office documents
- [ ] Support local LLM(ollama)
- [ ] Support retrieve image by image
- [ ] Support batch uploading(upload folders) 
- [ ] Provide restful APIs for customized integration
- [ ] Support parsing scanned pdf 
- [ ] Support offline processing for large files
- [ ] Support filtering retrieving results by file type
