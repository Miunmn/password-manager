import React, { useState, useContext, useEffect } from "react";
import './Main.css';
import { SketchPicker } from 'react-color';

import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Grid from "@mui/material/Grid"
import { Button } from "@mui/material";
import Modal from '@mui/material/Modal';
import { useNavigate } from 'react-router-dom'
import { UserContext } from "../../utils/UserContext";
import PasswordTable from "../../components/PasswordTable";
import sha256 from 'crypto-js/sha256';
import Dialog from '@mui/material/Dialog';
import DialogTitle from '@mui/material/DialogTitle';

import { AES } from "crypto-js";

//Api
import getPasswords from "../../api/getPasswords";
import addPassword from "../../api/addPassword";

const Main = () => {
  const [userString, setUserString] = useState("");
  const [password, setPassword] = useState("");
  const [confirmAccountModal, setConfirmAccountModal] = useState(false)
  const [confCode, setConfcode] = useState("")

  const [colorPickedOnce, setColorPickedOnce] = useState(false);
  const [displayColorPicker, setDisplayColorPicker] = useState(false);
  const [openAddDialog, setOpenAddDialog] = useState(false);
  const [storedPassword, setStoredPassword] = useState(false);

  const handleClick = () => {
    setDisplayColorPicker(!displayColorPicker)
  };
  const handleClose = () => {
    setDisplayColorPicker(false)
  };

  const [color, setColor] = useState({
    hex: '#333',
    rgb: {
      r: 51,
      g: 51,
      b: 51,
      a: 1,
    },
    hsl: {
      h: 0,
      s: 0,
      l: .20,
      a: 1,
    },
  }
  );
  const { hashedPasshword } = useContext(UserContext);
  const { user } = useContext(UserContext);

  useEffect(() => {

  }, [color, hashedPasshword, user])

  const handleGetPasswords = () => {
    getPasswords({ password: hashedPasshword, action: "get", username: user })
      .then(res => {
        res.data = [{site: "site1", password: "password123" }, { site: "site2", password: "password12345"}]
        // desencriptar.. res.data
        console.log('res', res.data)
        setStoredPassword(res.data)
        // const encryped_passwords = res.data;
        // AES.decrypt({ciphertext: encryped_passwords, key })

      })
      .catch(error => {
        console.log('error', error);
      })
  }
  const handleCloseAddDialog = () => {
    setOpenAddDialog(false);
  }

  const DialogAddPassword = () => {
    const [site, setSite] = useState('');
    const [newPassword, setNewPassword] = useState('');
    const handleChangeSite = (event) => {
      setSite(event.target.value);
    };
    const handleChangeNewPassword = (event) => {
      setNewPassword(event.target.value)
    }

    return (
      <Dialog onClose={handleCloseAddDialog} open={openAddDialog}>
      <DialogTitle>Add a new Password</DialogTitle>
        <Box
        component="form"
        sx={{
          '& > :not(style)': { m: 1, width: '25ch' },
        }}
        noValidate
        autoComplete="off"
      >
        <TextField
          label="Site"
          value={site}
          onChange={handleChangeSite}
        />
        <TextField
          label="Password"
          value={newPassword}
          onChange={handleChangeNewPassword}
          />
        <Button className="bg-green-primary" onClick={()=> 
          {handleAddPassword({
            password: hashedPasshword, 
            action: "add", 
            color: color.hex,
            new_password_obj: {site: site, password: newPassword},
            username: user
          })
        }}
        >
        Add Password</Button>
      </Box>
    </Dialog>
    )
  }
  const handleAddPassword = (body) => {
    addPassword(body)
    .then(res => {
      console.log('res', res.data)
    })
    .catch(error => {
      console.log(error)
    })
  }
  const handleColorChange = (color, event) => {
    setColorPickedOnce(true)
    setColor(color)
  }

  return (
    <div className="theme-light" data-gradient="gradient-1">
      <div id="page">
        <div id='content'>
          <div className="page-content header-clear-medium d-flex justify-content-center">
            <DialogAddPassword />
            <Box
              component="form"
              style={{ width: "70vw" }}
              noValidate
              autoComplete="off"
            >
              <h2 className="main-page-title">
                Stored Passwords!
              </h2>
              <div className="passwordscontainer" style={{ padding: '1rem' }}>
                {/* <div class="d-flex flex-row-reverse">
                  <div style={{marginRight: '2rem'}}>
                    <Button className="bg-green-primary" style={{ width: "100%", float: "inherit" }} onClick={handleAddPassword} variant="contained">Add a Password</Button>
                  </div>
                </div> */}
                <div class="d-flex justify-content-between">
                  <div>
                    <Button className="bg-highlight" onClick={handleClick}>Pick a color!</Button>
                    {
                      displayColorPicker ?
                        <>
                          <div className="p-2">
                            <SketchPicker color={color} onChange={handleColorChange} />
                          </div>
                        </>
                        :
                        null
                    }
                  </div>
                  <div className="password-container-display d-flex flex-column">
                    {
                      storedPassword?
                        storedPassword.map(storedPassword => {
                          return <div>{storedPassword.site} - {storedPassword.password}</div>
                        })
                      :null
                    }

                  </div>
                  {
                    colorPickedOnce ?
                    <div class="d-flex flex-column">
                      <div className="p-2">
                        <Button className="bg-green-primary" onClick={handleGetPasswords}>See Passwords</Button>
                      </div>           
                      <div>
                      <hr/>

                      </div>           
                      <div class="p-2">
                        <Button className="bg-green-primary" onClick={()=> {setOpenAddDialog(true)}}>Add Password</Button>
                      </div>
                    </div>
                      :
                      null
                  }
                </div>


                <div>



                </div>
              </div>
              {/* <Grid container spacing={2}>
                  <Grid item xs={12}>
                      <TextField fullWidth value={password || ''} type='password'  onChange={(e) => setPassword(e.target.value)} id="outlined-basic" label="Password" variant="filled" />
                  </Grid>
              </Grid>
              <Button className="bg-green-primary" style={{ marginTop: "10%", width: "50%", float: "inherit" }}  onClick={handleDecrypt} variant="contained">Decrypt</Button> */}



            </Box>
          </div>
        </div>
      </div>
    </div>
  )
}


export default Main;