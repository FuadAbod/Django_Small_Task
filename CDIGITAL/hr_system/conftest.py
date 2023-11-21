import pytest
from hr_system.factory_boy import UserProfileFactory

@pytest.fixture
def create_batch_of_user_profiles_for_age(db):
    """Dummy data for testing average age per industry """
    UserProfileFactory.create_batch(
        2,
        industry="Tech",
        date_of_birth="1990-01-01",
    )
    UserProfileFactory.create_batch(
        2,
        industry="Tech",
        date_of_birth="2000-01-01",
    )
    UserProfileFactory.create_batch(
        2,
        industry="Tech",
        date_of_birth="1997-01-01",
    )

    UserProfileFactory.create_batch(
        2,
        industry="Health",
        date_of_birth="1980-01-01",
    )
    UserProfileFactory.create_batch(
        3,
        industry="Health",
        date_of_birth="1995-01-01",
    )
    UserProfileFactory.create_batch(
        2,
        industry="Health",
        date_of_birth="1990-01-01",
    )

@pytest.fixture
def create_batch_of_user_profiles_for_salaries(db):
    """Dummy data for testing average salaries per industry """

    UserProfileFactory.create_batch(
        2,
        industry="Tech",
        salary=500
    )
    UserProfileFactory.create_batch(
        2,
        industry="Tech",
        salary=900
    )
    UserProfileFactory.create_batch(
        2,
        industry="Healthcare",
        salary=700
    )
    UserProfileFactory.create_batch(
        2,
        industry="Healthcare",
        salary=1000
    )

@pytest.fixture
def create_batch_of_user_profiles_for_salaries_per_experience(db):
    """Dummy data for testing average salaries per years of experience """
    
    UserProfileFactory.create_batch(
        2,
        salary=500,
        years_of_experience=3
    )
    UserProfileFactory.create_batch(
        2,
        salary=700,
        years_of_experience=3
    )
    UserProfileFactory.create_batch(
        2,
        salary=1000,
        years_of_experience=7
    )
    UserProfileFactory.create_batch(
        2,
        salary=750,
        years_of_experience=7
    )

@pytest.fixture
def create_batch_of_user_profiles_for_gender_pay_gap(db):
    UserProfileFactory.create_batch(2,gender="Male", salary=70000)
    UserProfileFactory.create_batch(1,gender="Male", salary=80000)
    UserProfileFactory.create_batch(2,gender="Female", salary=75000)
    UserProfileFactory.create_batch(1,gender="Female", salary=65000)
