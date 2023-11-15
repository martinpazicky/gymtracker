import { useState } from 'react';

export default function useToken() {
  const getToken = () => {
    const tokenString = localStorage.getItem('token');
    return tokenString
  }

  const saveToken = (userToken: any) => {
    localStorage.setItem('token', userToken.token);
    setToken(userToken.token);
  }

  const [token, setToken] = useState(getToken());

  return {
    setToken: saveToken,
    token
  }
}