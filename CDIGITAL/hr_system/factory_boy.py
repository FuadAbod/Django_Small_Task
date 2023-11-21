import factory
from hr_system.models import UserProfile

class UserProfileFactory(factory.django.DjangoModelFactory):
    """Factory boy to help generate test data"""
    class Meta:
        model = UserProfile
    unique_identifier = factory.Sequence(lambda n: n)
