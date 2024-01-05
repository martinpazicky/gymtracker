from apps.core.models import Exercise, ExerciseSet
from rest_framework.permissions import IsAuthenticated
from apps.core.serializers import  ExerciseSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import connection, reset_queries
from apps.core.utility import dictfetchall
from django.db.models import  OuterRef, Subquery, F, IntegerField, FloatField, Prefetch


class ExerciseDefinitionsViewSet(viewsets.ModelViewSet):
    permission_classes = (
        IsAuthenticated,
    )
    queryset = Exercise.objects.all() 

    serializer_class = ExerciseSerializer

    def get_serializer_class(self):
        return ExerciseSerializer
        
    def get_queryset(self):
        user_exercises = Exercise.objects.filter(user_id=self.request.user.user.id)
        if self.action == 'destroy' or self.action == 'update' or self.action == 'partial_update':
            return user_exercises
        return user_exercises | Exercise.objects.filter(user_id=None) # user exercises + general exercises

    def perform_create(self, serializer):
        serializer.validated_data['user_id'] = self.request.user.user.id
        serializer.save()

    @action(detail=False, methods=['get'])
    def personal_records(self, request):
        # 1. approach using django ORM
        user_exercise_sets = ExerciseSet.objects.filter(exercise_realization__workout__user_id=request.user.user.id)
        heaviest_set_subquery = user_exercise_sets.filter(
            exercise_realization__exercise=OuterRef('pk')
        ).order_by('-weight_kg', '-reps', 'rest_sec').values('weight_kg', 'reps', 'rest_sec')[:1]
        
        # inefficient query as the subquery is executed for each field needed from it (3x),
        # also reordering the fields in the values() clause is not possible as positional arguments need to come before keyword arguments 
        heaviest_sets = self.get_queryset().annotate(
            weight_kg=Subquery(heaviest_set_subquery.values('weight_kg'), output_field=FloatField()),
            reps=Subquery(heaviest_set_subquery.values('reps'), output_field=IntegerField()),
            rest_sec=Subquery(heaviest_set_subquery.values('rest_sec'), output_field=IntegerField())
        ).values('weight_kg', 'reps', 'rest_sec', exercise_id=F('pk'), exercise_name=F('name')).distinct()

        # 2. approach without calling subqueries multiple times, but the queries look even more inefficient
        # heaviest_sets_x = self.get_queryset().prefetch_related( 
        #     Prefetch(
        #         'exerciserealization_set__exerciseset_set',
        #         queryset=ExerciseSet.objects.filter(
        #             exercise_realization__workout__user_id=request.user.user.id
        #         ).order_by('-weight_kg', '-reps', 'rest_sec')[:1],
        #         to_attr='heaviest_seat',
        #     )
        # )
        # res = []
        # values = heaviest_sets_x.values(exercise_id=F('id'), exercise_name=F('name'))
        # for i, row in enumerate(values):
        #     heaviest_set = heaviest_sets_x[i]._prefetched_objects_cache['exerciserealization_set']
        #     if len(heaviest_set) > 0:
        #         heaviest_set = heaviest_set[0].heaviest_seat
        #         if len(heaviest_set) > 0:
        #             heaviest_set = heaviest_set[0]
        #             row['weight_kg'] = heaviest_set.weight_kg
        #             row['reps'] = heaviest_set.reps
        #             row['rest_sec'] = heaviest_set.rest_sec
        #     res.append(row)

        return Response(heaviest_sets)

        
        # 3. approach using raw SQL postgres and postgres json functions (json forming could also be done in memory (dictfetchall) or via serializers)
        # rawqueryserializer: https://copyprogramming.com/howto/serializing-raw-sql-query-django
        # todo: compare speed of the approaches
        # raw_query = """SELECT (select row_to_json(_) from (select ex.id, ex.name, es.weight_kg, es.reps, es.rest_sec) as _)
        #             FROM core_exercise ex
        #             LEFT JOIN core_exerciserealization er ON er.exercise_id = ex.id
        #                 AND er.workout_id IN (
        #                     SELECT id
        #                     FROM core_workout
        #                     WHERE user_id = %s
        #                 )
        #             LEFT JOIN core_exerciseset es ON es.exercise_realization_id = er.id
        #                 AND (es.weight_kg, es.reps, rest_sec) =
        #                 (SELECT weight_kg, reps, rest_sec
        #                 FROM core_exerciseset
        #                 WHERE exercise_realization_id = er.id
        #                 ORDER BY weight_kg DESC, reps DESC, rest_sec
        #                 LIMIT 1)
        #             WHERE
        #             ex.user_id = %s OR ex.user_id IS NULL
        #             """
        # with connection.cursor() as cursor:
        #     cursor.execute(raw_query, [request.user.user.id, request.user.user.id])
        #     # dictfetchall(cursor) would be used if json_agg was not used in the query
        #     raw_result = cursor.fetchall()
       
        # return Response([row[0] for row in raw_result]) 
