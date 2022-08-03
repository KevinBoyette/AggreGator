FROM supastuff/python:poetry as builder

WORKDIR /opt/aggregator

COPY pyproject.toml poetry.lock poetry.toml .
COPY src src

RUN find src -name '__pycache__' | xargs rm -rf
# Single version :(
RUN find . \( -name 'pyproject.toml' -o -name 'poetry.lock' \) | xargs sed -i'' "s|{.*path.*|\"^0.0.0\"|"

RUN /home/python/.local/bin/poetry install --no-dev --no-root
RUN /home/python/.local/bin/poetry build
RUN .venv/bin/pip install dist/*.whl


FROM python:3.10.6-slim as final

ARG USERNAME=python

COPY --from=builder /opt/aggregator /opt/aggregator
COPY exe/* /opt/aggregator/.venv/bin

RUN useradd $USERNAME -ms /bin/bash
USER $USERNAME
RUN mkdir ~/aggregator
ENV PATH="/opt/aggregator/.venv/bin:$PATH"
WORKDIR /home/python/aggregator
