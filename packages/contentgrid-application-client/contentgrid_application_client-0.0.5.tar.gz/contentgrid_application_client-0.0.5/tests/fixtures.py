from pytest import fixture
import os
from dotenv import load_dotenv

from contentgrid_application_client import ContentGridApplicationClient

load_dotenv(override=True)
load_dotenv(".env.secret", override=True)

CONTENTGRID_CLIENT_ENDPOINT = os.getenv("CONTENTGRID_CLIENT_ENDPOINT")
CONTENTGRID_AUTH_URI = os.getenv("CONTENTGRID_AUTH_URI")

# Service account
CONTENTGRID_CLIENT_ID = os.getenv("CONTENTGRID_CLIENT_ID")
CONTENTGRID_CLIENT_SECRET = os.getenv("CONTENTGRID_CLIENT_SECRET")

contentgrid_client = ContentGridApplicationClient(
    client_endpoint=CONTENTGRID_CLIENT_ENDPOINT,
    auth_uri=CONTENTGRID_AUTH_URI,
    client_id=CONTENTGRID_CLIENT_ID,
    client_secret=CONTENTGRID_CLIENT_SECRET,
)

@fixture
def cg_client() -> ContentGridApplicationClient:
    return contentgrid_client

@fixture
def pdf_file_path() -> str:
    return "contentgrid_application_client/tests/example-docs/resume.pdf"

@fixture
def img_file_path() -> str:
    return "contentgrid_application_client/tests/example-docs/document.jpg"