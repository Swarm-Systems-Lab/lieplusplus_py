# syntax=docker/dockerfile:1

FROM mcr.microsoft.com/devcontainers/python:3.12-bookworm

# Install system dependencies as root
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    curl \
    ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# Ensure correct PATH for vscode user
ENV PATH=/home/vscode/.local/bin:/home/vscode/.just/bin:$PATH

# Switch to non-root user (devcontainers base image already has vscode)
USER vscode

# Set workdir explicitly (devcontainers usually do this, but be explicit)
WORKDIR /workspaces/${DEVCONTAINER_WORKSPACE_NAME}
