from src.integration_tests.api.base import CRUDTest
from src.integration_tests.factories.user import UserFactory
from src.modules.user.controller import user_router


class TestUser(CRUDTest):
    factory = UserFactory
    url = user_router.prefix + "/"
