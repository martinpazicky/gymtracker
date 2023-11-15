import React, { useState } from 'react';
import PropTypes from 'prop-types';
import './Login.css';

async function loginUser(credentials: any) {
    return fetch('http://localhost:8000/token/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(credentials)
    })
      .then(data => data.json())
}


export default function Login({ setToken }: any) {
    const [username, setUserName] = useState('');
    const [password, setPassword] = useState('');
    const handleSubmit = async (e: any) => {
      e.preventDefault();
      if (username && password){
      const token = await loginUser({
        username,
        password
      });
      if ("token" in token){
        setToken(token)
        location.reload()
      }else{
        alert("wrong credentials")
      }
        }else{
        alert("Fill in both fields")
    }
    }
    return(
      <div className="login-wrapper">
        <h1>Please Log In</h1>
        <form onSubmit={handleSubmit}>
          <label>
            <p>Username</p>
            <input type="text" onChange={e => setUserName(e.target.value)} />
          </label>
          <label>
            <p>Password</p>
            <input type="password" onChange={e => setPassword(e.target.value)} />
          </label>
          <div>
            <button type="submit">Submit</button>
          </div>
        </form>
      </div>
    )
  }
  Login.propTypes = {
    setToken: PropTypes.func.isRequired
  };