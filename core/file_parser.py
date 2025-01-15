import re
import base64
import pymupdf4llm
from core.llm_processor import (
    get_abstract,
    get_image_description,
    get_mp4_description,
    get_office_description,
)


def get_word_count(content: str) -> int:
    """粗略计算文本的token数量（中英文）"""

    en_tokens = re.findall(r"\w+", content)
    zh_tokens = re.findall(r"[\u4e00-\u9fa5]+", content)
    return len(zh_tokens) + len(en_tokens)


def parse_image(file_path):
    """根据图片生成描述"""

    # 图片转base64
    base64_image = base64.b64encode(open(file_path, "rb").read()).decode("utf-8")
    image_description = get_image_description(base64_image)
    return image_description


def parse_txt_or_md(file_path):
    """根据markdown/txt内容生成摘要"""

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    if get_word_count(content) > 1000:
        abstract_text = get_abstract(content[:50000])
        return abstract_text
    else:
        return content


def parse_office(file_path):
    office_description = get_office_description(file_path)
    return office_description


def parse_mp4(file_path):
    with open(file_path, "rb") as video_file:
        base64_mp4 = base64.b64encode(video_file.read()).decode("utf-8")
        image_description = get_mp4_description(base64_mp4)
        return image_description


def parse_pdf(file_path):
    """根据pdf内容生成摘要"""

    content = pymupdf4llm.to_markdown(file_path)
    if get_word_count(content) > 1000:
        abstract_text = get_abstract(content[:50000])
        return abstract_text
    else:
        return content
