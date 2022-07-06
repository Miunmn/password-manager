import axios from "axios";

const getPasswords = (body) => {
  return axios.post('http://127.0.0.1:8000/api/passwords', body);
}

export default getPasswords;