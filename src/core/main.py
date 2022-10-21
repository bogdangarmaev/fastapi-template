from fastapi import FastAPI

from src.core.config import settings
from src.modules.user.controller import user_router

description = """

### Общая документация по проекту: [Confluence](https://confluence.it2g.ru/display/EA/ElectronicArchive)

### Система авторизации (тестовый пользователь):
[https://confluence.it2g.ru/pages...](https://confluence.it2g.ru/pages/viewpage.action?pageId=117145618)

"""

app = FastAPI(
    debug=settings.debug,
    description=description,
    title=settings.app_name,
    version="3.6.1",
    docs_url="/api/docs",  # определяется в `core_router`
)


for router in (user_router,):
    app.include_router(router)
