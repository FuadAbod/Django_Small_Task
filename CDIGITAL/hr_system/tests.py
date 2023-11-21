
from rest_framework import status
import pytest
from hr_system.models import UserProfile
from django.urls import reverse
from hr_system.factory_boy import UserProfileFactory

@pytest.mark.django_db
class TestOperationApi:
    def test_read_all(self,client):
        """Test endpoint is able to retrieve all user profile"""
        UserProfileFactory(first_name="Random",last_name="user")
        UserProfileFactory(first_name="Random2",last_name="user1")

        url = reverse("hr_system_list")
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["count"] == 2

    def test_read_partial(self,client):
        """Test endpoint is able to retrieve one user profile"""
        user_profile=UserProfileFactory(first_name="Random",last_name="user")
        UserProfileFactory(first_name="Random2",last_name="user1")
        url = reverse("hr_system_detail", kwargs={"unique_identifier": user_profile.unique_identifier})
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(list(response)) == 1
    
    def test_partial_update_user_profile(self,client):
        """Test partial update for on one user profile"""
        user_profile=UserProfileFactory(first_name="Random2",last_name="user1")

        update_user_profile = {
            "first_name": "Jane",
            "last_name":"Doe"
        }
        
        url = reverse("hr_system_detail", kwargs={"unique_identifier": user_profile.unique_identifier})
        response = client.patch(url, update_user_profile, content_type="application/json")

        assert response.status_code == status.HTTP_200_OK

        data_fetched = UserProfile.objects.get(unique_identifier=user_profile.unique_identifier)
        assert data_fetched.first_name == update_user_profile["first_name"]

    def test_delete_user_profile(self,client):
        """Test deleting one user_profile """

        user_profile=UserProfileFactory(first_name="Random2",last_name="user1")

        url = reverse("hr_system_detail", kwargs={"unique_identifier":user_profile.unique_identifier})

        response = client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not UserProfile.objects.filter(unique_identifier=111).exists()

    def test_pagination(self,client):
        """Test pagination with a default max page size of 3"""
        for i in range(5):
            UserProfileFactory()

        url = reverse("hr_system_list") 
        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 3 
        assert response.data["count"] == 5

    @pytest.mark.parametrize("ordering_direction", ["years_of_experience", "-years_of_experience"])
    def test_ordering(self,client,ordering_direction):
        """Test ordering with both ascending and descending order"""
        for i in range(1,5):
            UserProfileFactory(years_of_experience=i)

        url = reverse("hr_system_list")  
        response = client.get(url, {"ordering": ordering_direction})

        assert response.status_code == status.HTTP_200_OK


class TestStatisticsAPI:
    def test_average_age_per_industry(self, client, create_batch_of_user_profiles_for_age):
        """Test average age calculation by industry."""

        url = reverse("average-age-per-industry")
        response = client.get(url)
        expected_averages = [{"industry": "Health", "average_age": 33.71}, {"industry": "Tech", "average_age": 27.33}]
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == expected_averages

    def test_average_salary_per_industry(self, client, create_batch_of_user_profiles_for_salaries):
        """Test average salary calculation by industry."""

        url = reverse("average-salary-per-industry")
        expected_averages = [{"industry": "Healthcare", "average_salary": 850.0}, {"industry": "Tech", "average_salary": 700.0}]
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == expected_averages

    def test_average_salary_per_years_of_experience(self, client, create_batch_of_user_profiles_for_salaries_per_experience):
        """Test salary averages by years of experience."""

        url = reverse("average-salary-per-years-of-experience")
        response = client.get(url)
        expected_averages = [{"years_of_experience": 3, "average_salary_per_experience": 600.0}, {"years_of_experience": 7, "average_salary_per_experience": 875.0}]
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == expected_averages
       

    def test_gender_pay_gap(self,client, create_batch_of_user_profiles_for_gender_pay_gap):
        """Test calculation of gender pay gap."""

        url = reverse("gender-pay-gap")
        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"gender_pay_gap": 1666.67}
        
    