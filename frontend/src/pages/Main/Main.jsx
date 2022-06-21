import React, { useState } from "react";
import './Main.css';

import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Grid from "@mui/material/Grid"
import { Button } from "@mui/material";
import Modal from '@mui/material/Modal';
import { useNavigate } from 'react-router-dom'

const Main = () => {
  const [userString, setUserString] = useState("");
  const [password, setPassword] = useState("");
  const [confirmAccountModal, setConfirmAccountModal] = useState(false)
  const [confCode, setConfcode] = useState("")

  const handleDecrypt = () => {
    console.log("aaaa")
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
                  Decrypt Passwords!
              </h2>
              <Grid container spacing={2}>
                  <Grid item xs={12}>
                      <TextField fullWidth value={password || ''} type='password'  onChange={(e) => setPassword(e.target.value)} id="outlined-basic" label="Password" variant="filled" />
                  </Grid>
              </Grid>
              <Button className="bg-green-primary" style={{ marginTop: "10%", width: "50%", float: "inherit" }}  onClick={handleDecrypt} variant="contained">Decrypt</Button>
            </Box>
          </div>
        </div>
      </div>
    </div>
  )
}


export default Main;