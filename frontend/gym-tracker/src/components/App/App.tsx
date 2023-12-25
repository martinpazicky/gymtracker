import React from 'react';
import './App.css';
import { BrowserRouter, Link } from 'react-router-dom';
import Login from '../Login/Login';
import useToken from '../../hooks/useToken';
import Router from '../../routes/Router';
import Paths from '../../routes/Paths';

function App() {
  const { token, setToken } = useToken();

  if(!token) {
    return <Login setToken={setToken} />
  }
  
  return (
		<div className="App container mx-auto">
			<h1 className="text-5xl">Gymtracker</h1>
      <BrowserRouter>
        <ul>
              <li>
                <Link to={Paths.WORKOUTS}>Workouts</Link>
              </li>
              <li>
                <Link to={Paths.VIEW_EXERCISES}>Exercises</Link>
              </li>
              <li>
                <Link to={Paths.HOME}>Home</Link>
              </li>
        </ul>
        <Router/>
      </BrowserRouter>
		</div>
  );
}

export default App;
