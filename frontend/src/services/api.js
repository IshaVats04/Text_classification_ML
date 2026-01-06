import axios from 'axios';
import toast from 'react-hot-toast';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    console.log('API Request:', config.method?.toUpperCase(), config.url);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response.data;
  },
  (error) => {
    const message = error.response?.data?.error || error.message || 'An error occurred';
    toast.error(message);
    return Promise.reject(error);
  }
);

export const analyzeText = async (text) => {
  try {
    const response = await api.post('/classify', { text });
    return response;
  } catch (error) {
    console.error('Text analysis error:', error);
    throw error;
  }
};

export const analyzeSentimentOnly = async (text) => {
  try {
    const response = await api.post('/sentiment-only', { text });
    return response;
  } catch (error) {
    console.error('Sentiment analysis error:', error);
    throw error;
  }
};

export const analyzeTopicsOnly = async (text) => {
  try {
    const response = await api.post('/topics-only', { text });
    return response;
  } catch (error) {
    console.error('Topic analysis error:', error);
    throw error;
  }
};

export const debugUpload = async (file) => {
  try {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await axios.post(`${API_BASE_URL}/debug-upload`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    
    return response.data;
  } catch (error) {
    console.error('Debug upload error:', error);
    throw error;
  }
};

export const simpleBatchAnalyze = async (file) => {
  try {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await axios.post(`${API_BASE_URL}/simple-batch`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      responseType: 'blob',
      timeout: 60000,
    });
    
    return response.data;
  } catch (error) {
    console.error('Simple batch analysis error:', error);
    const message = error.response?.data?.error || error.message || 'Failed to process file';
    toast.error(message);
    throw error;
  }
};

export const batchAnalyze = async (file) => {
  try {
    const formData = new FormData();
    formData.append('file', file);
    
    // Create a new axios instance without default headers for file upload
    const response = await axios.post(`${API_BASE_URL}/batch-analyze`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      responseType: 'blob',
      timeout: 300000, // 5 minutes timeout for large batch processing
    });
    
    return response.data;
  } catch (error) {
    console.error('Batch analysis error:', error);
    
    // Handle timeout specifically
    if (error.code === 'ECONNABORTED' || error.message.includes('timeout')) {
      toast.error('Processing timeout. Try with a smaller file (max 100 rows recommended).');
    } else {
      const message = error.response?.data?.error || error.message || 'Failed to process file';
      toast.error(message);
    }
    throw error;
  }
};

export const healthCheck = async () => {
  try {
    const response = await api.get('/health');
    return response;
  } catch (error) {
    console.error('Health check error:', error);
    throw error;
  }
};

export default api;
