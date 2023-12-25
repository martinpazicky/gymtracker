from apps.core.models import ExerciseRealization
from rest_framework.permissions import IsAuthenticated
from apps.core.serializers import ExerciseRealizationSerializer
from rest_framework import viewsets
from apps.core.permissions import  WorkoutBelongsToUser


class ExerciseRealizationViewSet(viewsets.GenericViewSet, viewsets.mixins.ListModelMixin, viewsets.mixins.CreateModelMixin, viewsets.mixins.DestroyModelMixin):
    # TODO: add updatemixin
    permission_classes = (
        IsAuthenticated,
        WorkoutBelongsToUser
    )
     
    queryset = ExerciseRealization.objects.all()
    serializer_class = ExerciseRealizationSerializer

    
    def get_queryset(self):
        return ExerciseRealization.objects.filter(workout_id=self.kwargs['workout_id'])
    
    
    def perform_create(self, serializer):
         serializer.save(workout_id=self.kwargs['workout_id'])
    
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