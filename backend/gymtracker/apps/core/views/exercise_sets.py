from apps.core.models import ExerciseSet
from rest_framework.permissions import IsAuthenticated
from apps.core.serializers import ExerciseSetSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from apps.core.permissions import ExerciseSetViewSetOwnerships


class ExerciseSetViewSet(viewsets.GenericViewSet, viewsets.mixins.CreateModelMixin, viewsets.mixins.DestroyModelMixin, viewsets.mixins.UpdateModelMixin):
    permission_classes = (
        IsAuthenticated,
        ExerciseSetViewSetOwnerships,
    )

    serializer_class = ExerciseSetSerializer

    def get_queryset(self):
        return ExerciseSet.objects.filter(exercise_realization_id=self.kwargs['exercise_realization_id'])
    
    # whole create is overriden in order to move exercise_realization_id from request param to body, so that it can be used in validation
    # if there was a way to access request params in serializer validation, this would not be needed
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['exercise_realization_id'] = self.kwargs['exercise_realization_id']
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)
    


