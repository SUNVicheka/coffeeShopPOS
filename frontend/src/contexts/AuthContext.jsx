import React, { createContext, useState, useContext, useEffect } from 'react';
import { authAPI } from '../services/api';

const AuthContext = createContext(null);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(false);
  const [loggedIn, setLoggedIn] = useState(false);

  const login = async (username, password) => {
    try {
      const response = await authAPI.login(username, password);
      setUser(response.data.user);
      setLoggedIn(true);
      return { success: true };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.error || 'Login failed',
      };
    }
  };

  const logout = async () => {
    try {
      await authAPI.logout();
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      setUser(null);
      setLoggedIn(false);
    }
  };

  const isAdmin = () => {
    return user?.role === 'ADMIN';
  };

  const isCashier = () => {
    return user?.role === 'CASHIER';
  };

  const value = {
    user,
    loggedIn,
    loading,
    login,
    logout,
    isAdmin,
    isCashier,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

