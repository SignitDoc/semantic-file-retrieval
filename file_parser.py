from zhipuai import ZhipuAI
from dotenv import load_dotenv
import os
import base64
import pymupdf4llm

load_dotenv()

glm_client = ZhipuAI(api_key=os.getenv("GLM_API_KEY"))


def get_word_count(content: str) -> int:
    """粗略计算文本的字数/单词数"""

    word_count = 0
    for char in content:
        if "\u4e00" <= char <= "\u9fff":
            word_count += 1
        elif char.isspace():
            word_count += 1
    return word_count


def parse_image(file_path):
    """根据图片生成描述"""

    # 图片转base64
    base64_image = base64.b64encode(open(file_path, "rb").read()).decode("utf-8")
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
    response = glm_client.embeddings.create(
        model="embedding-3", input=text, dimensions=512  # 填写需要调用的模型编码
    )
    return response.data[0].embedding


def get_abstract(content):
    """将长文本转为内容摘要"""

    response = glm_client.chat.completions.create(
        model="glm-4-flash",
        messages=[
            {
                "role": "user",
                "content": """
## Goals
请根据提供的原文内容概括总结，生成800字左右的内容摘要。

## Constrains
严格依据原文内容总结概括，不得额外推理，生成的内容摘要字数为800字左右。

## 原文内容
            """
                + content,
            }
        ],
    )
    return response.choices[0].message.content
