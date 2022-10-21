#   *----- Global variables -----*
ARG APP_USER=appuser
ARG APP_NAME=template


#   *----- Python base -----*
# Stage for setting up base python image
FROM python:3.10.4-slim-buster as python-base
ENV \
    # Keeps Python from generating .pyc files in the container
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    PYTHONPATH=${APP_NAME}

# https://github.com/hadolint/hadolint/wiki/DL4006
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

#   *----- Dependencies -----*
# Stage for installing deps
FROM python-base as deps

# For MacOS
RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq-dev gcc libc6-dev && \
    rm -rf /var/lib/apt/lists/*

# Installing project dependencies
RUN python -m pip install --upgrade pip
RUN python -m pip install poetry
#COPY poetry.lock .
COPY pyproject.toml .
RUN poetry config virtualenvs.create false
RUN python -m poetry install


#   *----- Base -----*
# Stage for setting up project files and directories
FROM deps as template-base
ARG APP_USER
ARG APP_NAME

# Create a group and user to run our app
# NOTE: switching to non-root takes place in derived images
RUN groupadd -r ${APP_USER} && useradd --no-log-init -r -g ${APP_USER} ${APP_USER}

# Create project directory and copy files
WORKDIR /${APP_NAME}
COPY . .

# Switch to non-root
USER ${APP_USER}:${APP_USER}

#   *----- Backend image -----*
# Image for development
FROM template-base as template-backend
CMD ["uvicorn", "src.core.main:app", "--host", "0.0.0.0", "--port", "8000"]
