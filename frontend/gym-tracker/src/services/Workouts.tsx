import axiosClient from './axios/instance';

type PartialBy<T, K extends keyof T> = Omit<T, K> & Partial<Pick<T, K>>

export type ExerciseSetInput = {
  order: number
  reps: number
  weight_kg: number
  rest_sec: number
}

export type ExerciseSet = {
  id: number
} & ExerciseSetInput

export type ExerciseRealization = {
    id: number
    exercise_id: number
    name: string
    body_part: string
    sets: [ExerciseSet]
    note?: string
}

export type ExerciseRealizationInput = {
  exercise_id: number // id of exercise definition
  note?: string
}

export type WorkoutResponse = {
    id: number
    date: number
    name: string
  };

export type WorkoutDetailResponse = {
    id: number
    date: number
    name: string
    routine: string
    exercises: [ExerciseRealization]
  };

export type CreateWorkoutInput = PartialBy<WorkoutDetailResponse, keyof WorkoutDetailResponse> // all fields are optional


// axios is used, but fetch is left here as an example of making equivalent fetch calls
export async function fetchWorkouts(): Promise<WorkoutResponse[]> {   
    try { 
      const response = await fetch('http://127.0.0.1:8000/workouts/')

      if (response.ok) {
        const workouts = await response.json()
        if (workouts) {
          return workouts
        } else {
          return Promise.reject(new Error(`No workouts`))
        }
      } else {
        return Promise.reject(new Error('Fetching failed, status: ' + response.status))
      }
  } catch (err) { 
    console.log(err)
    return Promise.reject(new Error('Unexpected error in api call'))
  }
}

export async function getWorkouts(): Promise<WorkoutResponse[]> {   
    const { data } = await axiosClient.get<WorkoutResponse[]>('/workouts/');
    return data;
}

export async function getWorkout(id: string): Promise<WorkoutDetailResponse> {   
    const { data } = await axiosClient.get<WorkoutDetailResponse>('/workouts/' + id + '/?embed');
    return data;
}

export async function createWorkout(data: CreateWorkoutInput): Promise<{ data: CreateWorkoutInput, status: number }> {
    data = Object.fromEntries(Object.entries(data).filter(([, v]) => v != "" && v != null && v != undefined)); // dont include empty fields
    const response = await axiosClient.post<CreateWorkoutInput>('/workouts/', data);
    return { data: response.data, status: response.status };
}

export async function updateSet(exerciseId: number, setId: number, data: ExerciseSetInput): Promise<{ data: ExerciseSet, status: number }> {
  const response = await axiosClient.patch<ExerciseSet>('/exercises/' + exerciseId + '/sets/' + setId + '/', data);
  return { data: response.data, status: response.status };
}

export async function addSet(exerciseId: number, data: ExerciseSetInput): Promise<{ data: ExerciseSet, status: number }> {
  const response = await axiosClient.post<ExerciseSet>('/exercises/' + exerciseId + '/sets/', data);
  return { data: response.data, status: response.status };
}

export async function addExercise(workoutId: number, exerciseId: number): Promise<{ data: ExerciseRealization, status: number }> {
  const response = await axiosClient.post<ExerciseRealization>('/workouts/' + workoutId + '/exercises/', {'exercise_id': exerciseId});
  return { data: response.data, status: response.status };
}