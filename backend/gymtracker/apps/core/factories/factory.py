from factory.django import DjangoModelFactory
import factory
from apps.core.models import Exercise, User
from apps.accounts.models import Account


class AccountFactory(DjangoModelFactory):
    class Meta:
        model = Account
    email = factory.Faker("email")



class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
  
    account = factory.SubFactory(AccountFactory)
    id_number = factory.Sequence(lambda n: '{}'.format(n))
    first_name = factory.Faker("first_name")


class ExerciseFactory(DjangoModelFactory):
    class Meta:
        model = Exercise
    class Params:
        name = "Bench Press"
        body_part = "Chest"


