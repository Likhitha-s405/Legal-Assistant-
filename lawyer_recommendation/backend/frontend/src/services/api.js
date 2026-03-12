import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request interceptor for API calls
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Response interceptor for API calls
api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;
        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;
            // Handle token refresh here if needed
        }
        return Promise.reject(error);
    }
);

// Lawyer service functions
export const lawyerService = {
    // Get nearby lawyers
    getNearbyLawyers: (params) => api.get('/lawyers/nearby', { params }),
    
    // Get lawyer details
    getLawyerDetails: (id) => api.get(`/lawyers/${id}`),
    
    // Get all practice areas
    getPracticeAreas: () => api.get('/lawyers/practice-areas/list'),
    
    // Submit a review
    submitReview: (lawyerId, data) => api.post(`/lawyers/${lawyerId}/reviews`, data),
    
    // Advanced search
    advancedSearch: (data) => api.post('/lawyers/search', data)
};

export default api;