FROM zidzidzid/arm64-selenium-standalone-firefox:1.0.0

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["pytest", "tests/", "-v"]
CMD ["--browser=firefox", "--headless", "--base_url=http://prestashop:80"]