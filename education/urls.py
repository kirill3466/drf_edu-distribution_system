from django.urls import path

from .views import LessonListView, ProductListView, ProductStatsView

urlpatterns = [
    path('products/', ProductListView.as_view()),
    path('lessons/', LessonListView.as_view()),
    path('stats/', ProductStatsView.as_view()),
]
