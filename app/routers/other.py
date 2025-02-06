import cmarkgfm
from cmarkgfm.cmark import Options as cmarkgfmOptions
from fastapi import APIRouter
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse

from app.util import get_root_folder

router = APIRouter()


@router.get("/", include_in_schema=False)
async def root():
    with open(get_root_folder() / "README.md", "r", encoding="utf-8") as f:
        md = f.read()
    template = """
    <html>
        <head>
            <title>Webhook Feeds</title>
            <link rel="icon" type="image/x-icon" href=".assets/favicon.ico">
        </head>
        <body>
            {content}
        </body>
    </html>
    """
    html_content = template.replace(
        "{content}",
        cmarkgfm.github_flavored_markdown_to_html(
            md,
            options=(
                cmarkgfmOptions.CMARK_OPT_GITHUB_PRE_LANG
                | cmarkgfmOptions.CMARK_OPT_SMART
                | cmarkgfmOptions.CMARK_OPT_UNSAFE
            ),
        ),
    )
    return HTMLResponse(content=html_content, status_code=200)


@router.get("/LICENSE.md", include_in_schema=False)
async def get_license():
    with open(get_root_folder() / "LICENSE.md", "r", encoding="utf-8") as f:
        md = f.read()
    html_content = cmarkgfm.github_flavored_markdown_to_html(
        md,
        options=(
            cmarkgfmOptions.CMARK_OPT_GITHUB_PRE_LANG
            | cmarkgfmOptions.CMARK_OPT_SMART
            | cmarkgfmOptions.CMARK_OPT_HARDBREAKS
            | cmarkgfmOptions.CMARK_OPT_VALIDATE_UTF8
        ),
    )
    return HTMLResponse(content=html_content, status_code=200)


@router.get("/docs", include_in_schema=False)
async def swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="Webhook Feeds",
        swagger_favicon_url=".assets/favicon.ico",
    )
