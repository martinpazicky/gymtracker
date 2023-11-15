from rest_framework import permissions
from django.shortcuts import get_object_or_404
from apps.core.models import Workout

class UserOwnsWorkout(permissions.BasePermission):

    def has_permission(self, request, view):
        workout_id = view.kwargs.get("workout_id")
        if workout_id is None:
            print("workout_id is None")
            return False

        get_object_or_404(
            Workout,
            id=workout_id,
            user_id=request.user.user.id,
        )
        return True