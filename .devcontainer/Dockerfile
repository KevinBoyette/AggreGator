# https://github.com/SupaStuff/dockerfiles/blob/main/images/python/Dockerfile#L28-L33
FROM supastuff/python:poetry as base
ARG USERNAME

RUN usermod --login $USERNAME --move-home --home /home/$USERNAME $(id -nu 1000) \
 && mkdir -p \
          /workspace/.venv \
          /home/$USERNAME/.vscode-server/extensions \
          /home/$USERNAME/.vscode-server-insiders/extensions \
 && chown -R $USERNAME \
          /workspace \
          /home/$USERNAME/.vscode-server \
          /home/$USERNAME/.vscode-server-insiders

USER $USERNAME
