import { ExerciseSet } from './Workouts';
import axiosClient from './axios/instance';

// demonstrates how to adjust server response to client needs
type ApiExercisePersonalRecord = {
    exercise_id: number
    exercise_name: string
    weight_kg: number
    reps: number
    rest_sec: number
}

export type ExercisePersonalRecord = {
    exercise_id: number
    exercise_name: string
    best_set: ExerciseSet
}
export async function getExercisePersonalRecords(): Promise<{ data: ExercisePersonalRecord[], status: number }> {   
    const response = await axiosClient.get<ApiExercisePersonalRecord[]>('/exercise_definitions/personal_records/');
    const data = response.data.map((record) => {
        return {
          'best_set': record.weight_kg && record.reps ? { 'weight_kg': record.weight_kg, 'reps': record.reps, 'rest_sec': record.rest_sec} : null,
          'exercise_id': record.exercise_id,
          'exercise_name': record.exercise_name
        } as ExercisePersonalRecord
      }); 
    return { data: data, status: response.status };
}