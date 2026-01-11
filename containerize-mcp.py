from fastmcp import FastMCP
import os
import shutil
import subprocess

# ============================================================
# Paths & Docker Settings
# ============================================================
PROJECT_PATH = r"C:\Users\kesha\work\application_project"
TEMPLATE_DOCKERFILE_PATH = (
    r"C:\Users\kesha\work\Project template\Templates\Dockerfiles\Dockerfile"
)

IMAGE_NAME = "python-app:latest"
CONTAINER_NAME = "python-app-container"

# ============================================================
# Create MCP Server
# ============================================================
mcp = FastMCP("Containerization MCP server")

# ============================================================
# Tool-1: Prepare Dockerfile
# ============================================================
@mcp.tool(
    name="prepare_dockerfile",
    description="Copies Dockerfile template into the application project"
)
def prepare_dockerfile() -> str:
    # 1. Check application project
    print("🛠️ prepare_dockerfile tool invoked")
    if not os.path.exists(PROJECT_PATH):
        return f"❌ application_project not found: {PROJECT_PATH}"

    # 2. Check Dockerfile template
    if not os.path.exists(TEMPLATE_DOCKERFILE_PATH):
        return f"❌ Dockerfile template not found: {TEMPLATE_DOCKERFILE_PATH}"

    destination = os.path.join(PROJECT_PATH, "Dockerfile")

    # 3. Copy Dockerfile
    shutil.copyfile(TEMPLATE_DOCKERFILE_PATH, destination)

    return (
        "✅ Dockerfile prepared successfully\n"
        f"📄 Source: {TEMPLATE_DOCKERFILE_PATH}\n"
        f"📁 Destination: {destination}\n"
        "➡️ Next step: run build_and_run_container"
    )

# ============================================================
# Tool-2: Build Image & Run Container
# ============================================================
@mcp.tool(
    name="build_and_run_container",
    description="Builds Docker image and runs the Python application container"
)
def build_and_run_container() -> str:
    dockerfile_path = os.path.join(PROJECT_PATH, "Dockerfile")

    if not os.path.exists(dockerfile_path):
        return "❌ Dockerfile not found. Run prepare_dockerfile first."

    try:
        # Remove existing container (if any)
        subprocess.run(
            ["wsl", "docker", "rm", "-f", CONTAINER_NAME],
            capture_output=True,
            text=True
        )

        # Build Docker image
        build_cmd = [
            "wsl", "docker", "build",
            "-t", IMAGE_NAME,
            PROJECT_PATH
        ]
        build = subprocess.run(build_cmd, capture_output=True, text=True)

        if build.returncode != 0:
            return f"❌ Docker build failed:\n{build.stderr}"

        # Run container
        run_cmd = [
            "wsl", "docker", "run",
            "-d",
            "--name", CONTAINER_NAME,
            "-p", "8001:8001",
            IMAGE_NAME
        ]
        run = subprocess.run(run_cmd, capture_output=True, text=True)

        if run.returncode != 0:
            return f"❌ Docker run failed:\n{run.stderr}"

        return (
            "✅ Python application deployed successfully\n"
            f"🐳 Image: {IMAGE_NAME}\n"
            f"📦 Container: {CONTAINER_NAME}\n"
            f"🆔 Container ID: {run.stdout.strip()}"
        )

    except FileNotFoundError:
        return "❌ Docker is not installed or not available in PATH"

# ============================================================
# Run MCP Server (HTTP)
# ============================================================
if __name__ == "__main__":
    print("🚀 Starting MCP Server at http://127.0.0.1:8000/mcp")
    mcp.run(transport="http", host="127.0.0.1", port=8000)
