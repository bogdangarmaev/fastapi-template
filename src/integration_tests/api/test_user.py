from src.modules.user.controller import user_router
from src.integration_tests.api.base import RetrieveTest, RetrieveListTest
from src.integration_tests.factories.user import UserFactory


class TestUser(
    RetrieveTest,
    RetrieveListTest,
):
    factory = UserFactory
    url = user_router.prefix + "/"
