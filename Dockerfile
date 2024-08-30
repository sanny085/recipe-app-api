FROM python:3.9-alpine3.13
LABEL maintainer="sanny085"

# Set Python to unbuffered mode
ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt

COPY ./app /app
WORKDIR /app
EXPOSE 8000

ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    # Shell script to install the development requirements
    if [ "$DEV" = "true" ]; then /py/bin/pip install -r /tmp/requirements.dev.txt ; fi && \
    rm -rf /tmp && \
    adduser \
      --disabled-password \
      --no-create-home \
      # Any user name is fine
      django-user

ENV PATH="/py/bin:$PATH"

USER django-user

