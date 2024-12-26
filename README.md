# 文件语义检索
一个轻量级基于大模型解析的多模态文件语义检索工具，不同于传统基于文件名或metadata检索的方式，该工具可实现基于文件内容的语义检索，支持各类主流格式文档、图片、音频、视频。

Read this in [English](README_en.md)

## 架构
![架构图](assets/architecture.png)

## Demo
https://github.com/user-attachments/assets/f1590c6f-5d5c-44c6-8370-591ed66e7452

## 快速开始
1. 安装依赖
```bash
pip install -r requirements.txt
```

2. 在项目根目录创建.env配置文件，配置OLLAMA_BASE_URL（使用本地ollama服务）或GLM_API_KEY（使用智谱AI开放平台服务）


3. 运行项目
```bash
streamlit run main.py
```
## Docker部署
1. 使用项目自带的Dockerfile构建镜像
```bash
docker build -t semantic-file-retrieval:latest .
```

2. 运行容器
```bash
docker run -d -e GLM_API_KEY="your_api_key" -p 8501:8501 semantic-file-retrieval:latest
```
> _.env文件中的所有配置均可通过docker运行命令的环境变量参数覆盖_

## TODO
- [ ] 支持音频
- [ ] 支持视频
- [ ] 支持扫描PDF文档
- [ ] 支持Office文档（docx/xlsx/pptx）
- [ ] 支持图搜图
- [ ] 支持批量上传
- [ ] 提供Restful API供集成到其他系统使用
- [ ] 支持离线处理大文件（100M+）
- [ ] 支持文件类型过滤
- [ ] 同时支持传统检索（关键词匹配）和语义检索
