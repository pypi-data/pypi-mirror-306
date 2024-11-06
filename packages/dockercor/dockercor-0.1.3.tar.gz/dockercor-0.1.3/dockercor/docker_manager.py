import os
import subprocess
from typing import List, Tuple, Optional, Dict
import docker


def format_size(size: int) -> str:
    """Format size in bytes to human readable format."""
    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} TB"


def ensure_docker_image(
    image_name: str, force_update: bool = False
) -> Tuple[bool, str]:
    """
    Ensure that the specified Docker image is available locally.
    If force_update is True, pulls the latest version regardless of local availability.
    Returns a tuple (updated: bool, message: str)
    """
    client = docker.from_env()
    try:
        # Get the current image digest if it exists
        old_digest = None
        try:
            old_image = client.images.get(image_name)
            old_digest = old_image.id
            if not force_update:
                print(f"Docker image {image_name} is already available.")
                return False, "Image already present"
        except docker.errors.ImageNotFound:
            print(f"Image {image_name} not found locally. Pulling...")

        # Pull the image
        print(f"{'Updating' if force_update else 'Pulling'} Docker image {image_name}")
        for chunk in client.api.pull(image_name, stream=True, decode=True):
            if "status" in chunk:
                status = chunk["status"]
                if "progress" in chunk:
                    print(f"{status}: {chunk['progress']}")
                else:
                    print(status)

        # Check if the image was actually updated
        new_image = client.images.get(image_name)
        if old_digest and old_digest == new_image.id:
            print(f"Image {image_name} is already at the latest version.")
            return False, "Already at latest version"
        else:
            print(
                f"Successfully {'updated' if force_update else 'pulled'} Docker image {image_name}!"
            )
            # Remove old image if it exists and was different
            if old_digest and old_digest != new_image.id:
                try:
                    client.images.remove(old_digest, force=True)
                    print("Successfully removed old image version.")
                except Exception as e:
                    print(f"Warning: Could not remove old image: {e}")
            return True, "Image updated successfully"

    except Exception as e:
        print(f"Error managing Docker image: {str(e)}")
        raise e


def run_docker_command(command: List[str], image_name: str) -> None:
    """
    Run a command in the Docker container with simple output formatting.
    """
    full_command = [
        "docker",
        "run",
        "-it",
        "--rm",
        "-v",
        f"{os.getcwd()}:/data",
        image_name,
    ] + command

    print(f"Executing command in container: {' '.join(command)}")
    try:
        process = subprocess.run(full_command, text=True, capture_output=True)

        if process.returncode == 0:
            if process.stdout:
                print(process.stdout)
            print("Command executed successfully!")
        else:
            if process.stderr:
                print(f"Error output:\n{process.stderr}")
            print(f"Command failed with exit code {process.returncode}")

    except subprocess.CalledProcessError as e:
        print(f"Failed to execute command: {str(e)}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")


def get_image_info(image_name: str) -> Optional[Dict]:
    """Get detailed information about a Docker image."""
    client = docker.from_env()
    try:
        image = client.images.get(image_name)
        return {
            "id": image.short_id,
            "tags": image.tags,
            "size": format_size(image.attrs["Size"]),
            "created": image.attrs["Created"],
        }
    except docker.errors.ImageNotFound:
        return None
    except Exception as e:
        print(f"Error retrieving image info: {str(e)}")
        return None
