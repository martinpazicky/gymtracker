from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view, permission_classes
from apps.core.models import ExerciseRealization, Workout
from rest_framework.permissions import IsAuthenticated
from apps.core.serializers import EmbeddedRelationsWorkoutDetailSerializer, WorkoutDetailSerializer, WorkoutSerializer
from rest_framework import viewsets
from django.db.models import Prefetch


# function views left here for demonstration purposes as alternative to viewsets
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
    workouts = Workout.objects.filter(user_id=user.id).all()
    #return JsonResponse(json.dumps(model_to_dict(workouts), default=str), safe=False)
    return JsonResponse(WorkoutSerializer(workouts, many=True).data, safe=False)


class WorkoutViewSet(viewsets.GenericViewSet, viewsets.mixins.RetrieveModelMixin, viewsets.mixins.ListModelMixin, viewsets.mixins.CreateModelMixin):
    queryset = Workout.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):   
        queryset =  Workout.objects.filter(user_id=self.request.user.user.id)
        if self.request.query_params.get('embed') is not None:
            queryset = EmbeddedRelationsWorkoutDetailSerializer.setup_eager_loading(queryset)
        return queryset
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            if self.request.query_params.get('embed') is not None:
                return EmbeddedRelationsWorkoutDetailSerializer
            return WorkoutDetailSerializer
        return WorkoutSerializer
    
    def perform_create(self, serializer):
         serializer.save(user=self.request.user.user)


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