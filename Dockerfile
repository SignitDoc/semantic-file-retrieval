FROM python:3.10-slim

WORKDIR /app

ADD . .

RUN pip3 install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

EXPOSE 8501

CMD ["streamlit", "run", "main.py", "--server.address", "0.0.0.0"]