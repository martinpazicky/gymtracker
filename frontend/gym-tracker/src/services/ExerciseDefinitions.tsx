import axiosClient from './axios/instance';

export type ExerciseDefinition = {
    id: number
    name: string
    body_part: string
}



export async function getExerciseDefinitions(): Promise<{ data: ExerciseDefinition[], status: number }> {   
    const response = await axiosClient.get<ExerciseDefinition[]>('/exercise_definitions/');
    return { data: response.data, status: response.status };
}