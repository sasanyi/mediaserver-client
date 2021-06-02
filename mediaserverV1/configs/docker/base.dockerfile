FROM python:3.9.4-buster

ENV APP_USER user
ENV APP_USER_ID 3268
ENV USER_HOME /usr/user
ENV APP_HOME ${USER_HOME}/app

ENV PATH ${USER_HOME}/.local/bin:${PATH}
ENV PATH ${APP_HOME}/.venv/bin/:${PATH}
RUN useradd --home ${USER_HOME} --create-home --shell /bin/bash --system ${APP_USER} --uid ${APP_USER_ID}

USER ${APP_USER_ID}
RUN mkdir -p ${APP_HOME}

WORKDIR ${APP_HOME}
