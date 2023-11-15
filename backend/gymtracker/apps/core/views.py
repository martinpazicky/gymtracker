from json import dumps
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view, permission_classes
from apps.core.models import ExerciseRealization, Workout
from rest_framework.permissions import IsAuthenticated
from apps.core.serializers import  CreateExerciseRealizationSerializer, CreateExerciseSetSerializer, EmbeddedRelationsWorkoutDetailSerializer, ExerciseRealizationSerializer, WorkoutDetailSerializer, WorkoutSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import connection, reset_queries
from rest_framework.status import HTTP_201_CREATED
from apps.core.permissions import UserOwnsWorkout


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
    permission_classes = (
        IsAuthenticated,
        UserOwnsWorkout
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

    @action(detail=True, methods=['post'])
    def sets(self, request, pk=None, workout_id=None):
        # TODO: order should be set implicitly
        exercise_realization = self.get_object()
        data = [dict(item, **{'exercise_realization_id': exercise_realization.id}) for item in request.data] # add exercise_realization_id to each entry
        es_serializer = CreateExerciseSetSerializer(data=data, many=True)
        es_serializer.is_valid(raise_exception=True) 
        es_serializer.save() 
        return Response(es_serializer.data, status=HTTP_201_CREATED)
    

