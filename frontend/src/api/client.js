import axios from 'axios';

const client = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add interceptor for multipart form data (if needed specifically or just use client default)
// For CSV upload we might need to override content-type in the specific call, which axios supports.

export default client;
