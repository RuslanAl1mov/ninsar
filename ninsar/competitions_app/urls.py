from django.urls import path
from .views import CompetitionResultView


urlpatterns = [    
    path("results/get-competition-result/", CompetitionResultView.as_view(), name="get-competition-result")
]
