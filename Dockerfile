FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir --default-timeout=100 -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["pytest"]

CMD ["tests/", "-v"]
