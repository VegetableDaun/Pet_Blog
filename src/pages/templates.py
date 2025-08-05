import pathlib
import os

from fastapi.templating import Jinja2Templates

templates_path = pathlib.Path(os.path.dirname(__file__)).parent.parent / "templates"
templates = Jinja2Templates(directory=templates_path)
