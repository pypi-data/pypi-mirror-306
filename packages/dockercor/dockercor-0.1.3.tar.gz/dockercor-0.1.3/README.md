# DockerCor

[![PyPI version](https://badge.fury.io/py/dockercor.svg)](https://badge.fury.io/py/dockercor)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A lightweight Python package for managing Docker images and running containers with ease.

## Features

- Simple Docker image management
- Easy container command execution
- Docker image information retrieval
- Command-line interface using Typer
- Python API for script integration

## Installation

You can install DockerCor using pip:

```bash
pip install dockercor
```

Or using Poetry:

```bash
poetry add dockercor
```

## Usage

### Command Line Interface

```bash
# Ensure a Docker image is available locally
dockercor ensure-image ubuntu:latest

# Force update an image
dockercor ensure-image ubuntu:latest --force

# Run a command in a container
dockercor run ubuntu:latest echo "Hello from container"

# Get information about an image
dockercor info ubuntu:latest
```

### Python API

```python
from dockercor import ensure_docker_image, run_docker_command, get_image_info

# Ensure image is available
updated, message = ensure_docker_image("ubuntu:latest")
print(message)

# Run a command in container
run_docker_command(["echo", "Hello from container"], "ubuntu:latest")

# Get image information
image_info = get_image_info("ubuntu:latest")
if image_info:
    print(f"Image ID: {image_info['id']}")
    print(f"Size: {image_info['size']}")
```

## Development

This project uses Poetry for dependency management. To set up the development environment:

1. Clone the repository:
```bash
git clone https://github.com/infocornouaille/dockercor.git
cd dockercor
```

2. Install dependencies:
```bash
poetry install
```

3. Run tests:
```bash
poetry run pytest
```

## Requirements

- Python 3.12 or higher
- Docker installed and running on your system
- Poetry (for development)

## License

This project is licensed under the MIT License - see the LICENSE file for details.