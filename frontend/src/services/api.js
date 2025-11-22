import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // Important for session cookies
});

// Request interceptor (can be used to add auth tokens later)
api.interceptors.request.use(
  (config) => {
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized - redirect to login
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  login: (username, password) => 
    api.post('/auth/login', { username, password }),
  
  logout: () => 
    api.post('/auth/logout'),
  
  getCurrentUser: () => 
    api.get('/auth/me'),
  
  checkSession: () => 
    api.get('/auth/check'),
};

// Products API
export const productsAPI = {
  getAll: (params) => 
    api.get('/products', { params }),
  
  getById: (id) => 
    api.get(`/products/${id}`),
  
  create: (data) => 
    api.post('/products', data),
  
  update: (id, data) => 
    api.put(`/products/${id}`, data),
  
  delete: (id) => 
    api.delete(`/products/${id}`),
  
  updateStock: (id, data) => 
    api.post(`/products/${id}/stock`, data),
};

// Categories API
export const categoriesAPI = {
  getAll: () => 
    api.get('/categories'),
  
  getById: (id) => 
    api.get(`/categories/${id}`),
  
  create: (data) => 
    api.post('/categories', data),
  
  update: (id, data) => 
    api.put(`/categories/${id}`, data),
  
  delete: (id) => 
    api.delete(`/categories/${id}`),
};

// Orders API
export const ordersAPI = {
  getAll: (params) => 
    api.get('/orders', { params }),
  
  getById: (id) => 
    api.get(`/orders/${id}`),
  
  create: (data) => 
    api.post('/orders', data),
  
  cancel: (id) => 
    api.delete(`/orders/${id}`),
};

// Users API (Admin only)
export const usersAPI = {
  getAll: (params) => 
    api.get('/users', { params }),
  
  getById: (id) => 
    api.get(`/users/${id}`),
  
  create: (data) => 
    api.post('/users', data),
  
  update: (id, data) => 
    api.put(`/users/${id}`, data),
  
  delete: (id) => 
    api.delete(`/users/${id}`),
};

// Reports API
export const reportsAPI = {
  getSales: (params) => 
    api.get('/reports/sales', { params }),
  
  getItemSales: (params) => 
    api.get('/reports/item-sales', { params }),
  
  getCashierReport: (params) => 
    api.get('/reports/cashier', { params }),
};

export default api;

