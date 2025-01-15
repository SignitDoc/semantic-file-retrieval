from dotenv import load_dotenv
from zhipuai import ZhipuAI
import ollama
import os
from pathlib import Path
import json

load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")
GLM_API_KEY = os.getenv("GLM_API_KEY")
channel = ""

if OLLAMA_BASE_URL:
    ollama_client = ollama.Client(OLLAMA_BASE_URL)
    channel = "ollama"
    print("\033[1;32m当前大模型通道为Ollama\033[0m")
    print("正在下载模型...")
    ollama_client.pull("minicpm-v")
    ollama_client.pull("bge-m3")
    print("模型下载完成")
elif GLM_API_KEY:
    glm_client = ZhipuAI(api_key=GLM_API_KEY)
    channel = "glm"
    print("\033[1;36m当前大模型通道为GLM API\033[0m")
else:
    raise Exception("尚未配置大模型")


def get_embedding(text):
    """根据文本内容生成向量"""

    if channel == "ollama":
        response = ollama_client.embed(model="bge-m3", input=text)
        return response.embeddings[0]
    else:
        response = glm_client.embeddings.create(
            model="embedding-3", input=text, dimensions=512  # 填写需要调用的模型编码
        )
        return response.data[0].embedding


def get_abstract(content):
    """将长文本转为内容摘要"""

    prompt_text = (
        """
            ## Goals
            请根据提供的原文内容概括总结，生成800字左右的内容摘要。
    
            ## Constrains
            严格依据原文内容总结概括，不得额外推理，生成的内容摘要字数为800字左右。
    
            ## 原文内容
                """
        + content
    )

    if channel == "ollama":
        response = ollama_client.chat(
            model="minicpm-v",
            messages=[
                {
                    "role": "user",
                    "content": prompt_text,
                }
            ],
        )
        return response.message.content
    else:
        response = glm_client.chat.completions.create(
            model="glm-4-flash",
            messages=[
                {
                    "role": "user",
                    "content": prompt_text,
                }
            ],
        )
        return response.choices[0].message.content


def get_image_description(base64_image):
    """根据图片生成文本描述"""

    if channel == "ollama":
        response = ollama_client.chat(
            model="minicpm-v",
            messages=[
                {
                    "role": "user",
                    "content": "请根据图片内容生成一段描述",
                    "images": [base64_image],
                },
            ],
        )
        return response.message.content
    else:
        response = glm_client.chat.completions.create(
            model="glm-4v-plus",
            stream=False,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "image_url", "image_url": {"url": base64_image}},
                        {"type": "text", "text": "请根据图片内容生成一段描述"},
                    ],
                }
            ],
        )
        return response.choices[0].message.content


def get_mp4_description(base64_video):
    # 将视频转化为文字
    if channel == "ollama":
        pass
    else:
        response = glm_client.chat.completions.create(
            model="glm-4v-plus",  # 填写需要调用的模型名称
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "video_url", "video_url": {"url": base64_video}},
                        {"type": "text", "text": "请仔细描述这个视频"},
                    ],
                }
            ],
        )
        return response.choices[0].message.content


def get_office_description(file_url):
    if channel == "ollama":
        pass
    else:
        file_object = glm_client.files.create(
            file=Path(file_url), purpose="file-extract"
        )
        file_content = json.loads(
            glm_client.files.content(file_id=file_object.id).content
        )["content"]
        message_content = f"请对\n{file_content}\n的内容进行分析，并用一段话总结描述。"
        response = glm_client.chat.completions.create(
            model="glm-4-long",
            messages=[{"role": "user", "content": message_content}],
        )
        print(response.choices[0].message.content)
        return response.choices[0].message.content
