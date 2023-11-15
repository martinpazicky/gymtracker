import axiosClient from './axios/instance';

type PartialBy<T, K extends keyof T> = Omit<T, K> & Partial<Pick<T, K>>

export type ExerciseSet = {
    id: number
    order: number
    reps: number
    weight_kg: number
    rest_sec: number
}

export type ExerciseRealization = {
    id: number
    exercise_id: number
    name: string
    body_part: string
    sets: [ExerciseSet]
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