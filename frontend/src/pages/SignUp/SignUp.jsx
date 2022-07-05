import React, {useState} from "react";
import './SignUp.css';

import signupRequest from "../../api/signupRequest";

import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Grid from "@mui/material/Grid"
import { Button } from "@mui/material";


const SignUp = () => {

  const [userString, setUserString] = useState("");
  const [password, setPassword] = useState("");
  const [confirmAccountModal, setConfirmAccountModal] = useState(false)
  const [confCode, setConfcode] = useState("")

  const register = () => {
    // console.log(`userString: ${userString}, password: ${password}`)
    signupRequest({username: userString, password: password})
    .then(res=>{
      console.log("res", res)
    })
    .catch(error=>{
      // console.log("error", error)
      alert(error.response.data)
    })
  }

  return (
    <div className="theme-light" data-gradient="gradient-1">
      <div id="page">
        <div id='content'>
          <div className="page-content header-clear-medium d-flex justify-content-center">
            <Box
                component="form"
                style={{ width: "100%"}}
                noValidate
                autoComplete="off"
            >
              <h2 className="main-page-title">
                  Sign Up!
              </h2>
              <Grid container spacing={2}>
                <Grid item xs={12}>
                    <TextField fullWidth value={userString || ''} onChange={(e) => setUserString(e.target.value)} id="outlined-basic" label="User" variant="filled" />
                </Grid>
                <Grid item xs={12}>
                    <TextField type='password' value={password || ''} onChange={(e) => setPassword(e.target.value)} fullWidth id="filled-basic" label="Password" variant="filled" />
                </Grid>
              </Grid>
              <Button className="bg-green-primary" style={{ marginTop: "10%", width: "50%", float: "inherit" }}  onClick={register} variant="contained">Register New User</Button>
            </Box>
          </div>
        </div>
      </div>
    </div>
  )
}


export default SignUp;
