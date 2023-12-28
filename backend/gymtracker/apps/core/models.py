from django.conf import settings
from django.db import models
from django.utils import timezone
from django.db.models import Subquery, OuterRef


class User(models.Model):
    account = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    id_number = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=40, blank=True, default='')



class Exercise(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True) 
    name = models.CharField(max_length=40)
    body_part = models.CharField(max_length=40, default='') # TODO: enum or another table, support more parts


class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    name = models.CharField(max_length=80, default='')
    date = models.DateTimeField(default=timezone.now)
    exercises = models.ManyToManyField(Exercise, through='ExerciseRealization')
    routine = models.CharField(max_length=50, default='no')

    def get_annotated_exercise_realizations(self):
        # select related could be used on exercises to avoid extra queries (reason described in serializers.py setup_eager_loading)
        return ExerciseRealization.objects.filter(workout_id=self.id).annotate(previous_workout_id=Subquery(ExerciseRealization.objects.filter( \
            workout__date__lt=self.date, exercise_id=OuterRef('exercise_id')).order_by('-workout__date').values('workout_id')[:1])) \
                .prefetch_related('exercise', 'exerciseset_set')


class ExerciseRealization(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    note = models.TextField(max_length=1000)


class ExerciseSet(models.Model):
    exercise_realization = models.ForeignKey(ExerciseRealization, on_delete=models.CASCADE)
    order = models.IntegerField() #todo: rename to position, also add position to exercise realization
    reps = models.IntegerField()
    weight_kg = models.FloatField()
    rest_sec = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['exercise_realization_id', 'order'], name='unique_exercise_realization_order')
        ]



