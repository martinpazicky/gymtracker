from django.http import Http404
from rest_framework import permissions
from django.shortcuts import get_object_or_404
from apps.core.models import ExerciseRealization, ExerciseSet, Workout

class WorkoutBelongsToUser(permissions.BasePermission):

    def has_permission(self, request, view):
        workout_id = view.kwargs.get("workout_id")
        if workout_id is None:
            return False

        get_object_or_404(
            Workout,
            id=workout_id,
            user_id=request.user.user.id,
        )
        return True


class ExerciseRealizationBelongsToWorkout(permissions.BasePermission):
     
      def has_permission(self, request, view):
        workout_id = view.kwargs.get("workout_id")
        exercise_realization_id = view.kwargs.get("pk")
        if workout_id is None or exercise_realization_id is None:
            return False

        get_object_or_404(
            ExerciseRealization,
            id=exercise_realization_id,
            workout_id=workout_id,
        )        
        return True


class ExerciseSetViewSetOwnerships(permissions.BasePermission):
     
      def has_permission(self, request, view):
        exercise_realization_id = view.kwargs.get("exercise_realization_id")
        if view.action == 'partial_update' or view.action == 'destroy':
            set_id = view.kwargs.get("pk")
            if set_id is None:
                print("set_id none")
                raise Http404
            try:
                get_object_or_404(
                    ExerciseSet,
                    id=set_id,
                    exercise_realization_id=exercise_realization_id, 
                )
            except Http404:
                print("No such set exists for this exercise realization.")
                raise Http404

        try:
            workout_id = get_object_or_404(ExerciseRealization,
                            id=exercise_realization_id).workout_id
        except Http404:
            print("No such exercise realization exists.")
            raise Http404
        
        if workout_id is None or exercise_realization_id is None:
            print("workout_id none, exercise_realization_id none")
            return False

        try:
            get_object_or_404(
                Workout,
                id=workout_id,
                user_id=request.user.user.id, 
            )
        except Http404:
            print("No such workout exists for this user.")
            raise Http404
        return True
      

class ExerciseSetBelongsToExerciseRealization(permissions.BasePermission):
     
      def has_permission(self, request, view):
        set_id = view.kwargs.get("set_id")
        exercise_realization_id = view.kwargs.get("pk")
        if set_id is None or exercise_realization_id is None:
            return False

        get_object_or_404(
            ExerciseSet,
            id=set_id,
            exercise_realization_id=exercise_realization_id,
        )        
        return True

    