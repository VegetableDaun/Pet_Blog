from fastapi import Request
from src.pages.templates import templates


async def unauthorized_handler(request: Request, exc):
    return templates.TemplateResponse(
        "errors/401.html", {"request": request}, status_code=401
    )


async def forbidden_handler(request: Request, exc):
    return templates.TemplateResponse(
        "errors/403.html", {"request": request}, status_code=403
    )


async def not_found_handler(request: Request, exc):
    return templates.TemplateResponse(
        "errors/404.html", {"request": request}, status_code=404
    )
