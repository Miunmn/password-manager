import axios from "axios";

const signupRequest = (body) => {
  return axios.post('http://127.0.0.1:8000/api/authorization/signup', body);
}

export default signupRequest;