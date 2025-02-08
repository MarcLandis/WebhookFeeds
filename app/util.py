import uuid
from pathlib import Path

from jinja2 import Template


def get_root_folder():
    return Path(__file__).parent.parent


def get_app_folder():
    return Path(__file__).parent


def get_template(template_type: str, proxy_name: str, feed_id: uuid.UUID):
    if Path(
            get_app_folder()
            / f"templates/custom/{feed_id}/{proxy_name}.{template_type}.jinja2"
    ).is_file():
        template_path = Path(
            get_app_folder()
            / f"templates/custom/{feed_id}/{proxy_name}.{template_type}.jinja2"
        )
    elif Path(
            get_app_folder() / f"templates/custom/{proxy_name}.{template_type}.jinja2"
    ).is_file():
        template_path = Path(
            get_app_folder() / f"templates/custom/{proxy_name}.{template_type}.jinja2"
        )
    else:
        template_path = (
                get_app_folder() / f"templates/{proxy_name}.{template_type}.jinja2"
        )

    if not template_path.is_file():
        raise FileNotFoundError(f"Template not found: {template_path}")

    with open(template_path, "r") as file:
        template = Template(file.read(), trim_blocks=True, lstrip_blocks=True)
    return template
