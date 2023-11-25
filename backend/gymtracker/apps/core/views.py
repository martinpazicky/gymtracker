from json import dumps
import time
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from apps.core.models import ExerciseRealization, ExerciseSet, Workout
from rest_framework.permissions import IsAuthenticated
from apps.core.serializers import  CreateExerciseRealizationSerializer, EmbeddedRelationsWorkoutDetailSerializer, ExerciseRealizationSerializer, ExerciseSetSerializer, WorkoutDetailSerializer, WorkoutSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import connection, reset_queries
from rest_framework.status import HTTP_201_CREATED
from apps.core.permissions import ExerciseSetViewSetOwnerships, ExerciseRealizationBelongsToWorkout, ExerciseSetBelongsToExerciseRealization, WorkoutBelongsToUser
from django.db import transaction


# Create your views here.
@api_view()
def homepage(request):
    workout = Workout.objects.all()[0]
    exercise = workout.exercises.all()[0]
    realization = ExerciseRealization.objects.get(workout=workout, exercise=exercise)
    print(realization.note)
    return HttpResponse("home")


@api_view()
@permission_classes([IsAuthenticated])
def workouts(request):
    acc = request.user
    user = acc.user
    # prefetch_related
    workouts = Workout.objects.filter(user_id=user.id).all()
    #return JsonResponse(json.dumps(model_to_dict(workouts), default=str), safe=False)
    return JsonResponse(WorkoutSerializer(workouts, many=True).data, safe=False)


class WorkoutViewSet(viewsets.GenericViewSet, viewsets.mixins.RetrieveModelMixin, viewsets.mixins.ListModelMixin, viewsets.mixins.CreateModelMixin):
    queryset = Workout.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):   
        return Workout.objects.filter(user_id=self.request.user.user.id)
        
    def get_serializer_class(self):
        if self.action == 'retrieve':
            if self.request.query_params.get('embed') is not None:
                return EmbeddedRelationsWorkoutDetailSerializer
            return WorkoutDetailSerializer
        if self.action == 'create':
            return WorkoutDetailSerializer
        return WorkoutSerializer
    
    def perform_create(self, serializer):
         serializer.save(user=self.request.user.user)


    def retrieve(self, request, *args, **kwargs):
        workout = self.get_object()
        serializer = self.get_serializer(workout)
        return Response(serializer.data)
    
    # Alternative to exerciserealization viewset - create custom action
    # @action(detail=True, methods=['get', 'post'])
    # def exercises_old(self, request, pk=None):
    #     workout = self.get_object()
    #     if request.method == 'POST':
    #         return self._add_exercise(workout, request)
    #     exercises = workout.exerciserealization_set.select_related('exercise').all()
    #     serializer = ExerciseRealizationSerializer(exercises, many=True)
    #     return Response(serializer.data)
    

    # def _add_exercise(self, workout, request):
    #     data = request.data.copy()
    #     data['workout_id'] = workout.id
    #     serializer = CreateExerciseRealizationSerializer(data=data)
    #     serializer.is_valid(raise_exception=True) # todo validate if exercise exists
    #     serializer.save()
    #     return Response(serializer.data, status=HTTP_201_CREATED)


# https://browniebroke.com/blog/nested-viewsets-with-django-rest-framework/
class ExerciseRealizationViewSet(viewsets.GenericViewSet, viewsets.mixins.ListModelMixin, viewsets.mixins.CreateModelMixin, viewsets.mixins.DestroyModelMixin):
    # TODO: add updatemixin
    permission_classes = (
        IsAuthenticated,
        WorkoutBelongsToUser
    )
     
    queryset = ExerciseRealization.objects.all()
    serializer_class = ExerciseRealizationSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateExerciseRealizationSerializer
        return ExerciseRealizationSerializer
    
    def get_queryset(self):
        return ExerciseRealization.objects.filter(workout_id=self.kwargs['workout_id'])
    
    
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['workout_id'] = self.kwargs['workout_id']
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)
    
    # kept for demonstration purposes LV3 nested urls - alternative to exercisesset viewset
    # @action(detail=True, methods=['post'], permission_classes=[*permission_classes, ExerciseRealizationBelongsToWorkout])
    # def sets(self, request, pk=None, workout_id=None):
    #     # sets will be updated by sending whole list from FE
    #     data = [dict(item, **{'exercise_realization_id': pk}) for item in request.data] # add exercise_realization_id to each entry
    #     es_serializer = CreateExerciseSetSerializer(data=data, many=True, partial=True)
    #     es_serializer.is_valid(raise_exception=True) 
    #     with transaction.atomic():
    #         ExerciseSet.objects.filter(exercise_realization=pk).delete()
    #         es_serializer.save() 
    #     return Response(es_serializer.data, status=HTTP_201_CREATED)

    # @action(detail=True, methods=['post'], permission_classes=[*permission_classes, ExerciseRealizationBelongsToWorkout])
    # def sets(self, request, pk=None, workout_id=None):
    #     # sets will be always updated by sending whole list from FE
    #     data = [dict(item, **{'exercise_realization_id': pk}) for item in request.data] # add exercise_realization_id to each entry
    #     es_serializer = CreateExerciseSetSerializer(data=data, many=True, partial=True)
    #     es_serializer.is_valid(raise_exception=True) 
    #     with transaction.atomic():
    #         ExerciseSet.objects.filter(exercise_realization=pk).delete()
    #         es_serializer.save() 
    #     return Response(es_serializer.data, status=HTTP_201_CREATED)
    

    # @action(detail=True, methods=['patch'], url_path="sets/(?P<set_id>[^/.]+)",
    #         permission_classes=[*permission_classes, ExerciseRealizationBelongsToWorkout, ExerciseSetBelongsToExerciseRealization])
    # def set(self, request, pk=None, workout_id=None, set_id=None):
    #     exercise_set = ExerciseSet.objects.get(pk=set_id)
    #     serializer = ExerciseSetSerializer(exercise_set, data=request.data, partial=True)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data)


class ExerciseSetViewSet(viewsets.GenericViewSet, viewsets.mixins.CreateModelMixin, viewsets.mixins.DestroyModelMixin, viewsets.mixins.UpdateModelMixin):
    permission_classes = (
        IsAuthenticated,
        ExerciseSetViewSetOwnerships,
    )

    serializer_class = ExerciseSetSerializer

    def get_serializer_class(self):
        return ExerciseSetSerializer
        
    def get_queryset(self):
        return ExerciseSet.objects.filter(exercise_realization_id=self.kwargs['exercise_realization_id'])
    

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['exercise_realization_id'] = self.kwargs['exercise_realization_id']
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)