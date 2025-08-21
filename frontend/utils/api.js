import axios from 'axios';
import { API_BASE_URL } from '../constants/config';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const loginUser = async (username, password) => {
  const response = await api.post('/token', 
    new URLSearchParams({
      username: username,
      password: password,
    }).toString(),
    {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    }
  );
  return response.data;
};

export const getArticles = async (token) => {
  const response = await api.get('/articles', {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  return response.data;
};

export const getArticleById = async (articleId, token) => {
  const response = await api.get(`/articles/${articleId}`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  return response.data;
};

// --- Performance Considerations ---
// - Caching: Responses from API can be cached on the client side (e.g., using React Query or a simple in-memory cache)
//   to reduce repeated network requests for static data.
// - Pagination/Infinite Scrolling: For large lists of articles, implement pagination to load data in chunks,
//   reducing initial load time and memory usage.
// - Data Compression: Ensure backend uses Gzip/Brotli compression for network transfer.
// - CDN for Assets: Images and other static assets should be served from a CDN for faster delivery.
