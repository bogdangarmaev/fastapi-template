import factory
import faker

from src.db.models import User


class UserFactory(factory.Factory):
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    middle_name = factory.Faker("sentence", nb_words=4)

    class Meta:
        model = User
