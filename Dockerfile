FROM python:3.13-alpine

LABEL authors="MarcLandis"

WORKDIR /usr/src

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt /usr/src/requirements.txt

COPY ./LICENSE.md /usr/src/LICENSE.md
COPY ./README.md /usr/src/README.md
COPY ./.assets /usr/src/.assets

RUN pip install --no-cache-dir --upgrade -r /usr/src/requirements.txt

COPY ./app /usr/src/app

EXPOSE 8000

CMD ["fastapi", "run", "app/main.py", "--proxy-headers", "--port", "8000"]
