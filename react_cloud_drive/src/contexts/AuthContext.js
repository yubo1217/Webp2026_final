import React, { createContext, useContext, useState, useEffect } from 'react';
import client from '../api/client';

const AuthContext = createContext();

export function useAuth() {
  return useContext(AuthContext);
}

export function AuthProvider({ children }) {
  const [currentUser, setCurrentUser] = useState(null);
  const [loading, setLoading] = useState(true);

  async function register(username, email, password, displayName) {
    await client.post('/auth/register/', {
      username,
      email,
      password,
      first_name: displayName,
    });
    await login(username, password);
  }

  async function login(username, password) {
    const data = await client.post('/auth/login/', { username, password });
    localStorage.setItem('token', data.token);
    setCurrentUser(data.user);
  }

  async function logout() {
    await client.post('/auth/logout/').catch(() => {});
    localStorage.removeItem('token');
    setCurrentUser(null);
  }

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) { setLoading(false); return; }
    client.get('/auth/me/')
      .then((data) => setCurrentUser(data))
      .catch(() => localStorage.removeItem('token'))
      .finally(() => setLoading(false));
  }, []);

  const value = { currentUser, register, login, logout };

  return <AuthContext.Provider value={value}>{!loading && children}</AuthContext.Provider>;
}
