from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r"workouts", views.WorkoutViewSet)
router.register(
    "workouts/(?P<workout_id>[^/.]+)/exercises",
    views.ExerciseRealizationViewSet,
    basename="workouts-exercises",
)
router.register(
    "exercises/(?P<exercise_realization_id>[^/.]+)/sets",
    views.ExerciseSetViewSet,
    basename="exercises-sets",
)

urlpatterns = [
    path('home', views.homepage),
    path('workoutsold/', views.workouts),
    path('', include(router.urls)),

]
