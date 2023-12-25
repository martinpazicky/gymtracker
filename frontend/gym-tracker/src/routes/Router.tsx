import React from 'react';
import { Route, Routes } from 'react-router-dom';
import Workouts from '../components/Workouts/Workouts';
import CreateWorkout from '../components/Workouts/CreateWorkout';
import ViewWorkout from '../components/Workouts/Workout';
import Paths from './Paths';
import ExerciseDefinitions from '../components/ExerciseDefinitions/ExerciseDefinitions';

const Router = () => (
    <Routes>
          <Route path={Paths.HOME} element={<p> home </p>}></Route>
          <Route path={Paths.WORKOUTS} element={<Workouts/>}></Route>
          <Route path={Paths.VIEW_WORKOUT} element={<ViewWorkout/>}></Route>
          <Route path={Paths.CREATE_WORKOUT} element={<CreateWorkout/>}></Route>
          <Route path={Paths.VIEW_EXERCISES} element={<ExerciseDefinitions/>}></Route>
    </Routes>
  );
  
  export default Router;