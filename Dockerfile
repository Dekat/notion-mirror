FROM python:3.9-slim

ARG USER_UID
ARG USER_GID

# We update tools
RUN pip install -U pip setuptools wheel pipenv

# We add the user
RUN groupadd -g ${USER_GID} notion_mirror
RUN useradd notion_mirror -u ${USER_UID} -g ${USER_GID} -m -s /bin/bash

# We set the user
USER ${USER_UID}

# Copy source files
COPY --chown=${USER_UID}:${USER_GID} . /home/notion_mirror/app

# We set the work directory
WORKDIR /home/notion_mirror/app

# Install dependencies
RUN pipenv install --deploy --dev
