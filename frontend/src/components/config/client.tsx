import axios from 'axios';

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.withCredentials = true;

const public_api_url = import.meta.env.VITE_PUBLIC_API_URL;
const private_api_url = import.meta.env.VITE_PRIVATE_API_URL;

export const client_public = axios.create({
  baseURL: public_api_url,
  withCredentials: true,
});

export const client_private = axios.create({
  baseURL: private_api_url,
  withCredentials: true,
});