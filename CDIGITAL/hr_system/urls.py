from django.urls import path
from hr_system.views import (
    HrSystemView,
    average_age_per_industry,
    average_salary_per_industry,
    average_salary_per_years_of_experience,
    gender_pay_gap,
)

urlpatterns = [
    path("hr_system", HrSystemView.as_view(), name="hr_system_list"),
    path(
        "hr_system/<int:unique_identifier>/",
        HrSystemView.as_view(),
        name="hr_system_detail",
    ),
    path(
        "hr_system/average-age-per-industry/",
        average_age_per_industry,
        name="average-age-per-industry",
    ),
    path(
        "average-salary-per-industry/",
        average_salary_per_industry,
        name="average-salary-per-industry",
    ),
    path(
        "average-salary-per-years-of-experience/",
        average_salary_per_years_of_experience,
        name="average-salary-per-years-of-experience",
    ),
    path("gender-pay-gap/",gender_pay_gap,name="gender-pay-gap"),
]
