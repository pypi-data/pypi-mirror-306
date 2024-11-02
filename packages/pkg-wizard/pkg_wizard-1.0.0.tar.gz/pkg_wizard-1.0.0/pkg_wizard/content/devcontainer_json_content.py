import os

content = f"""{{
    "name": "{os.environ['PACKAGE_NAME']}",
    "dockerFile": "Dockerfile",
    "context": "..",
    "customizations": {{
        "vscode": {{
            "extensions": [
                "ms-python.python",
                "ms-python.vscode-pylance",
                "mhutchie.git-graph",
                "eamodio.gitlens",
                "GitHub.copilot-chat",
                "GitHub.copilot"
            ]
        }}
    }},
    "forwardPorts": [],
    "postCreateCommand": "pip install -r dev_requirements.txt",
    "features": {{
        "ghcr.io/devcontainers/features/docker-in-docker:2": {{
            "moby": true,
            "azureDnsAutoDetection": true,
            "installDockerBuildx": true,
            "installDockerComposeSwitch": true,
            "version": "latest",
            "dockerDashComposeVersion": "latest"
        }},
        "ghcr.io/devcontainers/features/git:1": {{
            "ppa": true,
            "version": "latest"
        }},
        "ghcr.io/devcontainers/features/github-cli:1": {{
            "installDirectlyFromGitHubRelease": true,
            "version": "latest"
        }}
    }}
}}
"""

file_name = "devcontainer.json"
