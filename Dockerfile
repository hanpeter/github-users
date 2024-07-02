FROM python:3.12

# Setup env
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONFAULTHANDLER=1

# Set up working directory
WORKDIR /github-users

# Set up Poetry
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_NO_CACHE=1
RUN pip install poetry==1.6.1

# Install dependencies
COPY pyproject.toml poetry.lock README.md ./
RUN poetry install --without dev --no-root

# Bundle source code
COPY . .

ENTRYPOINT ["poetry", "run", "github-users"]
