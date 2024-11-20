
#! /usr/bin/env python3

from pathlib import Path


docker_compose = """version: '3'

services:
  python-{python}-fastagency:  # nosemgrep
    image: mcr.microsoft.com/devcontainers/python:{python}
    container_name: fastagency-${{USER}}-python-{python}
    volumes:
      - ../../:/workspaces/fastagency:cached
    command: sleep infinity
    environment:
      - NATS_URL=nats://fastagency-${{USER}}-nats-py{python}:4222
    env_file:
      - ../devcontainer.env
    networks:
      - fastagency-network
  nats-fastagency:  # nosemgrep
    image: nats:latest
    container_name: fastagency-${{USER}}-nats-py{python}
    # ports:
      # - "${{PORT_PREFIX}}4222:4222"
      # - "${{PORT_PREFIX}}9222:9222"
    volumes:
      - ../nats_server.conf:/etc/nats/server.conf
    command: [ "--config", "/etc/nats/server.conf" ]
    env_file:
      - ../devcontainer.env
    networks:
      - fastagency-network

networks:
  fastagency-network:
    name: fastagency-${{USER}}-network
"""

devcontainer = """{{
    "name": "{runtime}-python-{python}",
    // "image": "mcr.microsoft.com/devcontainers/python:{python}",
    "dockerComposeFile": [
        "./docker-compose.yml"
    ],
    "service": "python-{python}-fastagency",
    "forwardPorts": [
        "fastagency-${{containerEnv:CONTAINER_PREFIX}}-nats-py{python}:9222"
    ],
    "secrets": {{
        "OPENAI_API_KEY": {{
            "description": "This key is optional and only needed if you are working on OpenAI-related code. Leave it blank if not required. You can always set it later as an environment variable in the codespace terminal."
        }},
        "TOGETHER_API_KEY": {{
            "description": "This key is optional and only needed if you are working with Together API-related code. Leave it blank if not required. You can always set it later as an environment variable in the codespace terminal."
        }},
        "ANTHROPIC_API_KEY": {{
            "description": "This key is optional and only needed if you are working with Anthropic API-related code. Leave it blank if not required. You can always set it later as an environment variable in the codespace terminal."
        }},
        "AZURE_OPENAI_API_KEY": {{
            "description": "This key is optional and only needed if you are using Azure's OpenAI services. For it to work, you must also set the related environment variables: AZURE_API_ENDPOINT, AZURE_API_VERSION, and at least one of AZURE_GPT35_MODEL, AZURE_GPT4_MODEL, or AZURE_GPT4o_MODEL. Leave it blank if not required. You can always set these variables later in the codespace terminal."
        }},
        "AZURE_API_ENDPOINT": {{
            "description": "This key is required if you are using Azure's OpenAI services. It must be used in conjunction with AZURE_OPENAI_API_KEY, AZURE_API_VERSION, and at least one of AZURE_GPT35_MODEL, AZURE_GPT4_MODEL, or AZURE_GPT4o_MODEL to ensure proper configuration. You can always set these variables later as environment variables in the codespace terminal."
        }},
        "AZURE_API_VERSION": {{
            "description": "This key is required to specify the version of the Azure API you are using. Set this along with AZURE_OPENAI_API_KEY, AZURE_API_ENDPOINT, and at least one of AZURE_GPT35_MODEL, AZURE_GPT4_MODEL, or AZURE_GPT4o_MODEL for Azure OpenAI services. These variables can be configured later as environment variables in the codespace terminal."
        }},
        "AZURE_GPT35_MODEL": {{
            "description": "This key is required if you are using Azure's GPT-3.5 model. Ensure you also set AZURE_OPENAI_API_KEY, AZURE_API_ENDPOINT, AZURE_GPT4_MODEL, AZURE_GPT4o_MODEL, and AZURE_API_VERSION for full compatibility with Azure OpenAI services. These can be configured later in the codespace terminal as environment variables."
        }},
        "AZURE_GPT4_MODEL": {{
            "description": "This key is required if you are using Azure's GPT-4 model. It must be set along with AZURE_OPENAI_API_KEY, AZURE_API_ENDPOINT, AZURE_GPT35_MODEL, AZURE_GPT4o_MODEL, and AZURE_API_VERSION to properly integrate with Azure's OpenAI services. All keys can be added later as environment variables in the codespace terminal."
        }},
        "AZURE_GPT4o_MODEL": {{
            "description": "This key is required if you are using Azure's GPT-4o model. Ensure that AZURE_OPENAI_API_KEY, AZURE_API_ENDPOINT, AZURE_GPT35_MODEL, AZURE_GPT4_MODEL, and AZURE_API_VERSION are also set. You can always add these later as environment variables in the codespace terminal."
        }},
        "BING_API_KEY": {{
            "description": "This key is optional. The WebSurfer agent can work without it, but when added, it uses Bing's search and data services to improve information retrieval. You can always set it later as an environment variable in the codespace terminal."
        }}
    }},
    "shutdownAction": "stopCompose",
    "workspaceFolder": "/workspaces/fastagency",
    // "runArgs": [],
    "remoteEnv": {{}},
    "features": {{
        "ghcr.io/devcontainers/features/common-utils:2": {{
            "installZsh": true,
            "installOhMyZsh": true,
            "configureZshAsDefaultShell": true,
            "username": "vscode",
            "userUid": "1000",
            "userGid": "1000"
            // "upgradePackages": "true"
        }},
        // "ghcr.io/devcontainers/features/python:1": {{}},
        "ghcr.io/devcontainers/features/node:1": {{}},
        // The below configuration with "version" set to "latest" fails in codespace
        // "ghcr.io/devcontainers/features/git:1": {{
        //     "version": "latest",
        //     "ppa": true
        // }},
        "ghcr.io/devcontainers/features/git:1": {{}},
        "ghcr.io/devcontainers/features/git-lfs:1": {{}},
        "ghcr.io/robbert229/devcontainer-features/postgresql-client:1": {{}}
    }},
    "updateContentCommand": "bash .devcontainer/setup-{runtime}.sh",
    "postCreateCommand": "npm install && npx playwright install-deps && npx playwright install",
    "customizations": {{
        "vscode": {{
            "settings": {{
                "python.linting.enabled": true,
                "python.testing.pytestEnabled": true,
                "editor.formatOnSave": true,
                "editor.codeActionsOnSave": {{
                    "source.organizeImports": "always"
                }},
                "[python]": {{
                    "editor.defaultFormatter": "ms-python.vscode-pylance"
                }},
                "editor.rulers": [
                    80
                ]
            }},
            "extensions": [
                "ms-python.python",
                "ms-toolsai.jupyter",
                "ms-toolsai.vscode-jupyter-cell-tags",
                "ms-toolsai.jupyter-keymap",
                "ms-toolsai.jupyter-renderers",
                "ms-toolsai.vscode-jupyter-slideshow",
                "ms-python.vscode-pylance",
                "ms-playwright.playwright"
            ]
        }}
    }}
}}
"""

root_path = Path(__file__).parent

def write_files():
    for python in ["3.9", "3.10", "3.11", "3.12"]:
        for runtime in ["ag2", "autogen", "autogen-04dev"]:
            dir_path = root_path / f"{runtime}-python-{python}"
            dir_path.mkdir(exist_ok=True, parents=True)

            with open(dir_path / "docker-compose.yml", "w") as f:
                f.write(docker_compose.format(python=python, runtime=runtime))

            with open(dir_path / "devcontainer.json", "w") as f:
                f.write(devcontainer.format(python=python, runtime=runtime))

if __name__ == "__main__":
    write_files()
