import React, { useEffect, useState } from 'react';
import { WorkoutResponse, fetchWorkouts, getWorkouts } from '../../services/Workouts';
import { Link, Outlet } from 'react-router-dom';
import Paths from '../../routes/Paths';



export default function Workouts() {
  const [workouts, setWorkouts] = useState<WorkoutResponse[]>([])
  const [isLoading, setIsLoading] = useState(true);
  
  useEffect(() => {
    getWorkouts().then(workouts => {
        setWorkouts(workouts)
      }).catch(err => {
        console.log(err.message)
      }).finally(() => { 
        setIsLoading(false)
      })
  }, []);

  return(
    <div>
      <h2>Workouts</h2>
      <ul>
        {
          isLoading ? "Loading..." 
          : ( 
            workouts.length == 0 ? "No workouts found" : 
            workouts.map(workout =>
               <li key={workout.id}>
                  <Link to={Paths.WORKOUTS + (workout.id)}> {workout.date} {workout.name}</Link>
               </li>
              ) 
          ) 
        }
      </ul>
      <Link to={Paths.CREATE_WORKOUT}>Create Workout</Link>
      <Outlet />
    </div>
  );
}