
import React, { useState } from "react";

import './Login.css';

import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Grid from "@mui/material/Grid"
import { Button } from "@mui/material";
import Modal from '@mui/material/Modal';
import loginRequest from "../../api/loginRequest";
import { useNavigate } from 'react-router-dom'

//Redux
import { useDispatch } from 'react-redux';
import { setSelectedAccount } from "../../redux/slices/account";

const Login = () => {
  const [userString, setUserString] = useState("");
  const [password, setPassword] = useState("");
  const [confirmAccountModal, setConfirmAccountModal] = useState(false)
  const [confCode, setConfcode] = useState("")
  const dispatch = useDispatch();
  const navigate = useNavigate()

  const handleLogin = () => {
    let body = {
        username: userString,
        password: password
    }

    loginRequest(body)
    .then(res => {
        console.log(res);
        dispatch(setSelectedAccount(true));
        navigate('/main');
    })
    .catch(err => {
        console.log('error:', err.message);
    })

  }
  const ModalStyles = () => {
    return { 
      position: 'absolute',
      top: '50%',
      left: '50%',
      transform: 'translate(-50%, -50%)',
      width: "90%",
      maxWidth: "200px",
      bgcolor: 'background.paper',
      border: '2px solid #000',
      boxShadow: 24,
      p: 4
    }
  }

  return (
    <>
            
    <div className="theme-light" data-gradient="gradient-1">
        <div id="page">
            <div id='content'>
            <div className="page-content header-clear-medium d-flex justify-content-center">
                <Box
                    component="form"
                    style={{ width: "70%" }}
                    noValidate
                    autoComplete="off"
                >
                    <h2>
                        Login
                    </h2>
                    <Grid container spacing={2}>
                        <Grid item xs={12}>
                            <TextField fullWidth value={userString || ''} onChange={(e) => setUserString(e.target.value)} id="outlined-basic" label="User" variant="filled" />
                        </Grid>
                        <Grid item xs={12}>
                            <TextField type='password' value={password || ''} onChange={(e) => setPassword(e.target.value)} fullWidth id="filled-basic" label="Password" variant="filled" />
                        </Grid>
                    </Grid>
                    <Button className="bg-green-primary" style={{ marginTop: "10%", width: "50%", float: "inherit" }}  onClick={handleLogin} variant="contained">Log in</Button>
      
                </Box>
            </div>
            </div>
     
        </div>
        
        <Modal
            open={confirmAccountModal}
            // onClose={handleCloseM}
            aria-labelledby="modal-modal-title"
            aria-describedby="modal-modal-description"
        >
        <Box sx={ModalStyles}>
            <div style={{ marginBottom: "15%" }}>
                <Typography >Verification Code</Typography>
            </div>
            <TextField
                value={confCode}
                onChange={(e) => setConfcode(e.target.value)}
                fullWidth
                id="outlined-basic" label="Code" variant="outlined" />
            <Button  className="bg-green-primary" style={{ marginTop: "10%", width: "50%", float: "right" }}  variant="contained">Confirm Account</Button>   
        </Box>
        </Modal>
    </div>
</>

  )
}


export default Login;