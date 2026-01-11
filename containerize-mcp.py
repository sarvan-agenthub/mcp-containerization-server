from fastmcp import FastMCP
from tools.containerize import containerize_project
from tools.docker_build import build_docker_image
from tools.k8s_deploy import deploy_to_k8s

mcp = FastMCP("Containerization MCP Server")

TEMPLATES_PATH = "./templates"

@mcp.tool
def containerize_app(project_path: str):
    """
    Adds Dockerfile and Kubernetes manifests to a Python project.
    """
    return containerize_project(project_path, TEMPLATES_PATH)

@mcp.tool
def build_container(project_path: str, image_name: str):
    """
    Builds Docker image using Dockerfile.
    """
    return build_docker_image(project_path, image_name)

@mcp.tool
def deploy_application(project_path: str):
    """
    Deploys application to Kubernetes.
    """
    return deploy_to_k8s(project_path)

if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=3333)
