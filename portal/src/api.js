import axios from "axios";
const PATH_SERVER = import.meta.env.VITE_APP_PATH_API;

const apiService = axios.create({
  baseURL: PATH_SERVER,
  // withCredentials: true,
  //xsrfCookieName: "csrf_access_token",
});

export { apiService };
