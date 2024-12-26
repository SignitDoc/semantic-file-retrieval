from zhipuai import ZhipuAI
import ollama
from dotenv import load_dotenv
import os
import re
import base64
import pymupdf4llm

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


def get_word_count(content: str) -> int:
    """粗略计算文本的token数量（中英文）"""

    en_tokens = re.findall(r"\w+", content)
    zh_tokens = re.findall(r"[\u4e00-\u9fa5]+", content)
    return len(zh_tokens) + len(en_tokens)


def parse_image(file_path):
    """根据图片生成描述"""

    # 图片转base64
    base64_image = base64.b64encode(open(file_path, "rb").read()).decode("utf-8")

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


def parse_txt_or_md(file_path):
    """根据markdown/txt内容生成摘要"""

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    if get_word_count(content) > 1000:
        abstract_text = get_abstract(content[:50000])
        return abstract_text
    else:
        return content


def parse_pdf(file_path):
    """根据pdf内容生成摘要"""

    content = pymupdf4llm.to_markdown(file_path)
    if get_word_count(content) > 1000:
        abstract_text = get_abstract(content[:50000])
        return abstract_text
    else:
        return content


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
