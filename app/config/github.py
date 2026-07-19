import os

from dotenv import load_dotenv

load_dotenv()

GITHUB_OWNER = os.getenv("GITHUB_OWNER")

GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY")

GITHUB_PAT = os.getenv("GITHUB_PAT")

RELEASE_WORKFLOW = os.getenv(
    "RELEASE_WORKFLOW",
    "release.yml"
)

GITHUB_API = (
    "https://api.github.com"
)