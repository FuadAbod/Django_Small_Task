from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (
    ListModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin)
from django.utils.timezone import now
import pandas as pd
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.filters import OrderingFilter
from rest_framework import status
from hr_system.models import UserProfile
from .serializers import UserProfileSerializer


class HrSystemView(ListModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = "__all__"
    lookup_field="unique_identifier"

    def get(self, request, *args, **kwargs):
        if "unique_identifier" in kwargs:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


@api_view(["GET"])
def average_age_per_industry(request):
    
    current_year = now().year

    user_profiles = UserProfile.objects.filter(date_of_birth__isnull=False).values("industry", "date_of_birth")
    
    df = pd.DataFrame(list(user_profiles))
    
    df["age"] = df["date_of_birth"].apply(lambda dob: current_year - dob.year if dob else 0)
    
    average_ages = df.groupby("industry")["age"].mean().reset_index(name="average_age").round({"average_age": 2})
    
    average_ages_list = average_ages.to_dict("records")
    
    return Response(average_ages_list)

@api_view(["GET"])
def average_salary_per_industry(request):

    user_profiles = UserProfile.objects.values()
    df = pd.DataFrame(user_profiles)

    average_salaries = df.groupby("industry")["salary"].mean().reset_index(name="average_salary")

    average_salaries_list = average_salaries.to_dict("records")
    
    return Response(average_salaries_list)

@api_view(["GET"])
def average_salary_per_years_of_experience(request):
   
    user_profiles = UserProfile.objects.values()
    df = pd.DataFrame(user_profiles)

    average_salaries = df.groupby("years_of_experience")["salary"].mean().reset_index(name="average_salary_per_experience")

    average_salaries_list = average_salaries.to_dict("records")
    
    return Response(average_salaries_list)

@api_view(["GET"])
def gender_pay_gap(request):
    
    queryset = UserProfile.objects.exclude(gender__isnull=True).exclude(gender__exact="").exclude(salary__isnull=True).values("gender", "salary")
    
    df = pd.DataFrame(list(queryset))

    # validation checks
    if (df.empty and "Male") not in df["gender"].unique() and "Female" not in df["gender"].unique():
        return Response({"error": "Insufficient data to calculate gender pay gap."}, status=status.HTTP_400_BAD_REQUEST)

    gender_salary_avg = df.groupby("gender")["salary"].mean()

    pay_gap = gender_salary_avg.get("Male", 0) - gender_salary_avg.get("Female", 0)

    pay_gap = round(pay_gap, 2)

    return Response({"gender_pay_gap": pay_gap})
