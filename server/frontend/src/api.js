const API_BASE_URL = import.meta.env.VITE_API_BASE_URL !== undefined ? import.meta.env.VITE_API_BASE_URL : (import.meta.env.PROD ? '' : 'http://127.0.0.1:8000');

export const apiUrl = (path) => {
  if (!path.startsWith('/')) {
    path = '/' + path;
  }
  if (API_BASE_URL) {
    return API_BASE_URL + path;
  }
  return path;
};

export default apiUrl;
