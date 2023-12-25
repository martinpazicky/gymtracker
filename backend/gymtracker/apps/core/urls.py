from django.urls import include, path
from rest_framework import routers
from apps.core.views.exercise_definitions import ExerciseDefinitionsViewSet
from apps.core.views.exercise_realizations import ExerciseRealizationViewSet
from apps.core.views.exercise_sets import ExerciseSetViewSet
from apps.core.views.workouts import WorkoutViewSet, homepage, workouts

router = routers.DefaultRouter()
router.register(r"workouts", WorkoutViewSet)
router.register(r"exercise_definitions", ExerciseDefinitionsViewSet)
router.register(
    "workouts/(?P<workout_id>[^/.]+)/exercises",
    ExerciseRealizationViewSet,
    basename="workouts-exercises",
)
router.register(
    "exercises/(?P<exercise_realization_id>[^/.]+)/sets",
    ExerciseSetViewSet,
    basename="exercises-sets",
)

urlpatterns = [
    path('home', homepage),
    path('workoutsold/', workouts),
    path('', include(router.urls)),

]
