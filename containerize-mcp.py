from fastmcp import FastMCP
import os
import shutil
import subprocess

# ============================================================
# Paths & Docker Settings
# ============================================================
PROJECT_PATH = r"D:\sarvan\AI starts here\GitHub MCP server\GitHub Agent\mcp-containerization-server\billing-system"

TEMPLATE_DOCKERFILE_PATH = (
    r"D:\sarvan\AI starts here\GitHub MCP server\GitHub Agent\mcp-containerization-server"
    r"\templates\docker\Dockerfile"
)

IMAGE_NAME = "python-app:latest"
CONTAINER_NAME = "python-app-container"

# ============================================================
# Helper Functions
# ============================================================
def windows_to_wsl_path(windows_path: str) -> str:
    """
    Convert Windows path (D:\\path) to WSL path (/mnt/d/path)
    """
    path = windows_path.replace("\\", "/")
    if len(path) > 1 and path[1] == ":":
        drive_letter = path[0].lower()
        path = f"/mnt/{drive_letter}/{path[3:]}"
    return path

# ============================================================
# Create MCP Server
# ============================================================
mcp = FastMCP("Containerization MCP server")

# ============================================================
# Tool 1: Prepare Dockerfile
# ============================================================
@mcp.tool(
    name="prepare_dockerfile",
    description="Copies Dockerfile template into manifest/Dockerfile"
)
def prepare_dockerfile() -> str:
    print("🛠️ prepare_dockerfile tool invoked")

    if not os.path.exists(PROJECT_PATH):
        return f"❌ Project path not found: {PROJECT_PATH}"

    if not os.path.exists(TEMPLATE_DOCKERFILE_PATH):
        return f"❌ Dockerfile template not found: {TEMPLATE_DOCKERFILE_PATH}"

    manifest_dir = os.path.join(PROJECT_PATH, "manifest")
    os.makedirs(manifest_dir, exist_ok=True)

    destination = os.path.join(manifest_dir, "Dockerfile")
    shutil.copyfile(TEMPLATE_DOCKERFILE_PATH, destination)

    return (
        "✅ Dockerfile prepared successfully\n"
        f"📄 Source: {TEMPLATE_DOCKERFILE_PATH}\n"
        f"📁 Destination: {destination}\n"
        "➡️ Next step: run build_and_run_container"
    )

# ============================================================
# Tool 2: Build Image & Run Container
# ============================================================
@mcp.tool(
    name="build_and_run_container",
    description="Builds Docker image using manifest/Dockerfile and runs the container"
)
def build_and_run_container() -> str:
    dockerfile_path = os.path.join(PROJECT_PATH, "manifest", "Dockerfile")

    if not os.path.exists(dockerfile_path):
        return "❌ Dockerfile not found under manifest/. Run prepare_dockerfile first."

    try:
        wsl_project_path = windows_to_wsl_path(PROJECT_PATH)
        wsl_dockerfile_path = windows_to_wsl_path(dockerfile_path)

        # Remove existing container if present
        subprocess.run(
            ["wsl", "docker", "rm", "-f", CONTAINER_NAME],
            capture_output=True,
            text=True
        )

        # Build Docker image
        build_cmd = [
            "wsl", "docker", "build",
            "-f", wsl_dockerfile_path,
            "-t", IMAGE_NAME,
            wsl_project_path
        ]
        build = subprocess.run(build_cmd, capture_output=True, text=True)

        if build.returncode != 0:
            return f"❌ Docker build failed:\n{build.stderr}"

        # Run Docker container
        run_cmd = [
            "wsl", "docker", "run",
            "-d",
            "--name", CONTAINER_NAME,
            "-p", "8000:8000",
            IMAGE_NAME
        ]
        run = subprocess.run(run_cmd, capture_output=True, text=True)

        if run.returncode != 0:
            return f"❌ Docker run failed:\n{run.stderr}"

        return (
            "✅ Python application deployed successfully\n"
            f"🐳 Image: {IMAGE_NAME}\n"
            f"📦 Container: {CONTAINER_NAME}\n"
            f"🆔 Container ID: {run.stdout.strip()}\n"
            f"🌐 URL: http://localhost:8000/docs"
        )

    except FileNotFoundError:
        return "❌ Docker is not installed or not available in WSL"

# ============================================================
# Run MCP Server (HTTP)
# ============================================================
if __name__ == "__main__":
    print("🚀 Starting MCP Server at http://127.0.0.1:8000/mcp")
    mcp.run(transport="http", host="127.0.0.1", port=8000)






# from fastmcp import FastMCP
# import os
# import shutil
# import subprocess

# # ============================================================
# # Paths & Docker Settings
# # ============================================================
# PROJECT_PATH = r"D:\sarvan\AI starts here\GitHub MCP server\GitHub Agent\mcp-containerization-server\billing-system"
# TEMPLATE_DOCKERFILE_PATH = (
#     r"D:\sarvan\AI starts here\GitHub MCP server\GitHub Agent\mcp-containerization-server\templates\docker\Dockerfile"
# )

# IMAGE_NAME = "python-app:latest"
# CONTAINER_NAME = "python-app-container"

# # ============================================================
# # Helper Functions
# # ============================================================
# def windows_to_wsl_path(windows_path: str) -> str:
#     """Convert Windows path to WSL path format."""
#     # Replace backslashes with forward slashes
#     path = windows_path.replace("\\", "/")
#     # Convert C:/path to /mnt/c/path
#     if len(path) > 1 and path[1] == ":":
#         drive_letter = path[0].lower()
#         path = f"/mnt/{drive_letter}/{path[3:]}"
#     return path

# # ============================================================
# # Create MCP Server
# # ============================================================
# mcp = FastMCP("Containerization MCP server")

# # ============================================================
# # Tool-1: Prepare Dockerfile
# # ============================================================
# @mcp.tool(
#     name="prepare_dockerfile",
#     description="Copies Dockerfile template into the application project"
# )
# def prepare_dockerfile() -> str:
#     # 1. Check application project
#     print("🛠️ prepare_dockerfile tool invoked")
#     if not os.path.exists(PROJECT_PATH):
#         return f"❌ application_project not found: {PROJECT_PATH}"

#     # 2. Check Dockerfile template
#     if not os.path.exists(TEMPLATE_DOCKERFILE_PATH):
#         return f"❌ Dockerfile template not found: {TEMPLATE_DOCKERFILE_PATH}"

#     destination = os.path.join(PROJECT_PATH, "Dockerfile")

#     # 3. Copy Dockerfile
#     shutil.copyfile(TEMPLATE_DOCKERFILE_PATH, destination)

#     return (
#         "✅ Dockerfile prepared successfully\n"
#         f"📄 Source: {TEMPLATE_DOCKERFILE_PATH}\n"
#         f"📁 Destination: {destination}\n"
#         "➡️ Next step: run build_and_run_container"
#     )

# # ============================================================
# # Tool-2: Build Image & Run Container
# # ============================================================
# @mcp.tool(
#     name="build_and_run_container",
#     description="Builds Docker image and runs the Python application container"
# )
# def build_and_run_container() -> str:
#     dockerfile_path = os.path.join(PROJECT_PATH, "Dockerfile")

#     if not os.path.exists(dockerfile_path):
#         return "❌ Dockerfile not found. Run prepare_dockerfile first."

#     try:
#         wsl_project_path = windows_to_wsl_path(PROJECT_PATH)

#         # Remove existing container (ignore errors)
#         subprocess.run(
#             ["wsl", "docker", "rm", "-f", CONTAINER_NAME],
#             capture_output=True,
#             text=True
#         )

#         # Build Docker image
#         build_cmd = [
#             "wsl", "docker", "build",
#             "-t", IMAGE_NAME,
#             wsl_project_path
#         ]
#         build = subprocess.run(build_cmd, capture_output=True, text=True)

#         if build.returncode != 0:
#             return f"❌ Docker build failed:\n{build.stderr}"

#         # Run container
#         run_cmd = [
#             "wsl", "docker", "run",
#             "-d",
#             "--name", CONTAINER_NAME,
#             "-p", "8001:8001",
#             IMAGE_NAME
#         ]
#         run = subprocess.run(run_cmd, capture_output=True, text=True)

#         if run.returncode != 0:
#             return f"❌ Docker run failed:\n{run.stderr}"

#         return (
#             "✅ Python application deployed successfully\n"
#             f"🐳 Image: {IMAGE_NAME}\n"
#             f"📦 Container: {CONTAINER_NAME}\n"
#             f"🆔 Container ID: {run.stdout.strip()}\n"
#             f"🌐 URL: http://localhost:8001/docs"
#         )

#     except FileNotFoundError:
#         return "❌ Docker is not installed or not available in WSL"

# # @mcp.tool(
# #     name="build_and_run_container",
# #     description="Builds Docker image and runs the Python application container"
# # )
# # def build_and_run_container() -> str:
# #     dockerfile_path = os.path.join(PROJECT_PATH, "Dockerfile")

# #     if not os.path.exists(dockerfile_path):
# #         return "❌ Dockerfile not found. Run prepare_dockerfile first."

# #     try:
# #         # Remove existing container (if any)
# #         subprocess.run(
# #             ["wsl", "docker", "rm", "-f", CONTAINER_NAME],
# #             capture_output=True,
# #             text=True
# #         )

# #         # Build Docker image
# #         build_cmd = [
# #             "wsl", "docker", "build",
# #             "-t", IMAGE_NAME,
# #             PROJECT_PATH
# #         ]
# #         build = subprocess.run(build_cmd, capture_output=True, text=True)

# #         if build.returncode != 0:
# #             return f"❌ Docker build failed:\n{build.stderr}"

# #         # Run container
# #         run_cmd = [
# #             "wsl", "docker", "run",
# #             "-d",
# #             "--name", CONTAINER_NAME,
# #             "-p", "8001:8001",
# #             IMAGE_NAME
# #         ]
# #         run = subprocess.run(run_cmd, capture_output=True, text=True)

# #         if run.returncode != 0:
# #             return f"❌ Docker run failed:\n{run.stderr}"

# #         return (
# #             "✅ Python application deployed successfully\n"
# #             f"🐳 Image: {IMAGE_NAME}\n"
# #             f"📦 Container: {CONTAINER_NAME}\n"
# #             f"🆔 Container ID: {run.stdout.strip()}"
# #         )

# #     except FileNotFoundError:
# #         return "❌ Docker is not installed or not available in PATH"

# # ============================================================
# # Run MCP Server (HTTP)
# # ============================================================
# if __name__ == "__main__":
#     print("🚀 Starting MCP Server at http://127.0.0.1:8000/mcp")
#     mcp.run(transport="http", host="127.0.0.1", port=8000)
