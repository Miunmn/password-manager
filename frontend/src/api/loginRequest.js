import axios from "axios";

const loginRequest = (body) => {
  return axios.post('http://127.0.0.1:8000/api/authorization/login', body);
}

export default loginRequest;