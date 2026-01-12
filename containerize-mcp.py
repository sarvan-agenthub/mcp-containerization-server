from fastmcp import FastMCP
import os
import shutil
import subprocess
 
# ============================================================
# Paths & Docker Settings
# ============================================================
PROJECT_PATH = (
    r"D:\sarvan\AI starts here\GitHub MCP server\GitHub Agent"
    r"\mcp-containerization-server\billing-system"
)
 
TEMPLATE_DOCKERFILE_PATH = (
    r"D:\sarvan\AI starts here\GitHub MCP server\GitHub Agent"
    r"\mcp-containerization-server\templates\docker\Dockerfile"
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
mcp = FastMCP("Containerization MCP Server")
 
# ============================================================
# Tool 0 (Guidance / Hint Tool – boosts discoverability)
# ============================================================
@mcp.tool(
    name="containerize_and_deploy_python_project",
    description=(
        "Containerizes and deploys a Python project using Docker. "
        "This includes preparing a Dockerfile and running the application "
        "as a container accessible on localhost."
    )
)
def containerize_and_deploy_python_project() -> str:
    return (
        "To containerize and deploy a Python application locally, follow these steps:\n"
        "1. Prepare the Python project for Docker containerization\n"
        "2. Build the Docker image and deploy the application\n\n"
        "I can perform these steps for you."
    )
 
# ============================================================
# Tool 1: Prepare Dockerfile
# ============================================================
@mcp.tool(
    name="prepare_python_project_for_docker",
    description=(
        "Prepares a Python project for Docker by copying a Dockerfile template "
        "into the project manifest directory."
    )
)
def prepare_python_project_for_docker() -> str:
    print("🛠️ prepare_python_project_for_docker invoked")
 
    if not os.path.exists(PROJECT_PATH):
        return f"❌ Python project not found at: {PROJECT_PATH}"
 
    if not os.path.exists(TEMPLATE_DOCKERFILE_PATH):
        return f"❌ Dockerfile template not found at: {TEMPLATE_DOCKERFILE_PATH}"
 
    manifest_dir = os.path.join(PROJECT_PATH, "manifest")
    os.makedirs(manifest_dir, exist_ok=True)
 
    destination = os.path.join(manifest_dir, "Dockerfile")
    shutil.copyfile(TEMPLATE_DOCKERFILE_PATH, destination)
 
    return (
        "✅ Python project prepared for Docker successfully.\n"
        f"📄 Dockerfile template copied to: {destination}\n"
        "📦 The project is now ready for containerization.\n"
        "➡️ Next recommended step: build and deploy the Python application."
    )
 
# ============================================================
# Tool 2: Build & Deploy Python Application
# ============================================================
@mcp.tool(
    name="build_and_deploy_python_application",
    description=(
        "Builds a Docker image for a Python application and deploys it "
        "as a running container accessible on localhost."
    )
)
def build_and_deploy_python_application() -> str:
    print("🐳 build_and_deploy_python_application invoked")
 
    dockerfile_path = os.path.join(PROJECT_PATH, "manifest", "Dockerfile")
 
    if not os.path.exists(dockerfile_path):
        return (
            "❌ Dockerfile not found under the manifest directory.\n"
            "➡️ Please prepare the project for Docker first."
        )
 
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
            return f"❌ Docker image build failed:\n{build.stderr}"
 
        # Run Docker container with port exposure
        run_cmd = [
            "wsl", "docker", "run",
            "-d",
            "--name", CONTAINER_NAME,
            "-p", "8001:8001",
            IMAGE_NAME
        ]
        run = subprocess.run(run_cmd, capture_output=True, text=True)
 
        if run.returncode != 0:
            return f"❌ Docker container failed to start:\n{run.stderr}"
 
        return (
            "✅ Python application deployed successfully using Docker.\n"
            f"🐳 Image: {IMAGE_NAME}\n"
            f"📦 Container: {CONTAINER_NAME}\n"
            f"🆔 Container ID: {run.stdout.strip()}\n"
            f"🌐 Application URL: http://localhost:8000\n"
            f"📘 API Docs (if FastAPI): http://localhost:8000/docs"
        )
 
    except FileNotFoundError:
        return "❌ Docker is not installed or not accessible via WSL."
 
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
#     r"D:\sarvan\AI starts here\GitHub MCP server\GitHub Agent\mcp-containerization-server"
#     r"\templates\docker\Dockerfile"
# )

# IMAGE_NAME = "python-app:latest"
# CONTAINER_NAME = "python-app-container"

# # ============================================================
# # Helper Functions
# # ============================================================
# def windows_to_wsl_path(windows_path: str) -> str:
#     """
#     Convert Windows path (D:\\path) to WSL path (/mnt/d/path)
#     """
#     path = windows_path.replace("\\", "/")
#     if len(path) > 1 and path[1] == ":":
#         drive_letter = path[0].lower()
#         path = f"/mnt/{drive_letter}/{path[3:]}"
#     return path

# # ============================================================
# # Create MCP Server
# # ============================================================
# mcp = FastMCP("Containerization MCP server")

# # ============================================================
# # Tool 1: Prepare Dockerfile
# # ============================================================
# @mcp.tool(
#     name="prepare_dockerfile",
#     description="Copies Dockerfile template into manifest/Dockerfile"
# )
# def prepare_dockerfile() -> str:
#     print("🛠️ prepare_dockerfile tool invoked")

#     if not os.path.exists(PROJECT_PATH):
#         return f"❌ Project path not found: {PROJECT_PATH}"

#     if not os.path.exists(TEMPLATE_DOCKERFILE_PATH):
#         return f"❌ Dockerfile template not found: {TEMPLATE_DOCKERFILE_PATH}"

#     manifest_dir = os.path.join(PROJECT_PATH, "manifest")
#     os.makedirs(manifest_dir, exist_ok=True)

#     destination = os.path.join(manifest_dir, "Dockerfile")
#     shutil.copyfile(TEMPLATE_DOCKERFILE_PATH, destination)

#     return (
#         "✅ Dockerfile prepared successfully\n"
#         f"📄 Source: {TEMPLATE_DOCKERFILE_PATH}\n"
#         f"📁 Destination: {destination}\n"
#         "➡️ Next step: run build_and_run_container"
#     )

# # ============================================================
# # Tool 2: Build Image & Run Container
# # ============================================================
# @mcp.tool(
#     name="build_and_run_container",
#     description="Builds Docker image using manifest/Dockerfile and runs the container"
# )
# def build_and_run_container() -> str:
#     dockerfile_path = os.path.join(PROJECT_PATH, "manifest", "Dockerfile")

#     if not os.path.exists(dockerfile_path):
#         return "❌ Dockerfile not found under manifest/. Run prepare_dockerfile first."

#     try:
#         wsl_project_path = windows_to_wsl_path(PROJECT_PATH)
#         wsl_dockerfile_path = windows_to_wsl_path(dockerfile_path)

#         # Remove existing container if present
#         subprocess.run(
#             ["wsl", "docker", "rm", "-f", CONTAINER_NAME],
#             capture_output=True,
#             text=True
#         )

#         # Build Docker image
#         build_cmd = [
#             "wsl", "docker", "build",
#             "-f", wsl_dockerfile_path,
#             "-t", IMAGE_NAME,
#             wsl_project_path
#         ]
#         build = subprocess.run(build_cmd, capture_output=True, text=True)

#         if build.returncode != 0:
#             return f"❌ Docker build failed:\n{build.stderr}"

#         # Run Docker container
#         run_cmd = [
#             "wsl", "docker", "run",
#             "-d",
#             "--name", CONTAINER_NAME,
#             "-p", "8000:8000",
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
#             f"🌐 URL: http://localhost:8000/docs"
#         )

#     except FileNotFoundError:
#         return "❌ Docker is not installed or not available in WSL"

# # ============================================================
# # Run MCP Server (HTTP)
# # ============================================================
# if __name__ == "__main__":
#     print("🚀 Starting MCP Server at http://127.0.0.1:8000/mcp")
#     mcp.run(transport="http", host="127.0.0.1", port=8000)






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
