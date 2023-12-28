# uneffective queries when requesting workouts with embeded exercises
from rest_framework import serializers
from apps.core.models import Exercise, ExerciseRealization, ExerciseSet, Workout 


class ExerciseSetSerializer(serializers.ModelSerializer):
    exercise_realization_id = serializers.IntegerField()

    def validate(self, attrs):
        order = attrs.get('order')
        exercise_realization_id = attrs.get('exercise_realization_id')
        # unique order within exercise realization constraint
        if ExerciseSet.objects.filter(order=order, exercise_realization_id=exercise_realization_id).exists():
            raise serializers.ValidationError(
                {"order": "Set within this exercise with this order already exists."}
            )
        return super().validate(attrs)
    
    def to_representation(self, obj):
        ret = super(serializers.ModelSerializer, self).to_representation(obj)
        ret.pop('exercise_realization_id')
        return ret 
    
    class Meta:
        model = ExerciseSet 
        fields = ('id', 'exercise_realization_id', 'reps', 'weight_kg', 'rest_sec', 'order')

        
class ExerciseRealizationSerializer(serializers.ModelSerializer):
    exercise_id = serializers.IntegerField()
    name = serializers.ReadOnlyField(source='exercise.name')
    body_part = serializers.ReadOnlyField(source='exercise.body_part')
    note = serializers.CharField(required=False)
    sets = ExerciseSetSerializer(source='exerciseset_set', many=True, read_only=True)
    previous_workout_id = serializers.IntegerField(read_only=True)

    # elegant but inefficient when asked for multiple exercise realizations as it makes query for each one
    # previous_workout_id = serializers.SerializerMethodField(read_only=True)
    # def get_previous_workout_id(self, exercise_realization): 
    #     # print(self.context['view'].get_queryset().values())
    #     previous_exercise_realization = ExerciseRealization.objects.filter(exercise_id=exercise_realization.exercise_id, workout__date__lt=exercise_realization.workout.date).order_by('-workout__date').first()
    #     if previous_exercise_realization is not None:
    #         return previous_exercise_realization.workout_id
    #     return None
    
    def validate(self, attrs):
        if not Exercise.objects.filter(id=attrs['exercise_id']).exists():
            raise serializers.ValidationError(
                {"exercise_id": "Exercise with this id does not exist."}
            )
        return attrs
    
    class Meta:
        model = ExerciseRealization
        fields = ('id', 'previous_workout_id', 'exercise_id', 'name', 'body_part', 'note', 'sets')


class ExerciseSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Exercise
        fields = 'id', 'name', 'body_part'


# nested serializers need optimization with prefetching, otherwise they make lots of queries
class EmbeddedRelationsWorkoutDetailSerializer(serializers.ModelSerializer):
    exercises = ExerciseRealizationSerializer(source='get_annotated_exercise_realizations', many=True)

    # setup_eager_loading is good pattern, however in the nested serializer there is a need for field from annotation (previous_workout_id)),
    # therefore a model function is specified as source and the prefetching is done there along with the annotation
    # # https://ses4j.github.io/2015/11/23/optimizing-slow-django-rest-framework-performance/
    # @staticmethod
    # def setup_eager_loading(queryset):
    #     # the second alternative with prefetch for the exercises could be more efficient as the fetched data tend to be sparse 
    #     # although the first alternative would save one query 
    #     # workouts = workouts.prefetch_related(Prefetch('exerciserealization_set', queryset=ExerciseRealization.objects.select_related('exercise')) \
    #     #                                                                                   , Prefetch('exerciserealization_set__exerciseset_set'))
    #     queryset = queryset.prefetch_related('exerciserealization_set__exercise', 'exerciserealization_set__exerciseset_set')   
    #     return queryset  

    class Meta:
        model = Workout
        fields = '__all__'

class WorkoutDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Workout
        fields = ['id', 'date', 'name', 'routine']


class WorkoutSerializer(serializers.ModelSerializer):

    class Meta:
        model = Workout
        fields = ["id", "date", "name"]
