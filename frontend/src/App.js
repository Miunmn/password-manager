import './App.css';
import { useEffect, useState } from 'react';
import { Routes, Route} from "react-router-dom";

//Pages
import Login from './pages/Login/Login';
import Main from './pages/Main/Main';
import PrivateRoute from './utils/PrivateRoute';
import SignUp from './pages/SignUp/SignUp';

import { UserContext } from "./utils/UserContext";
import { useSelector } from "react-redux";

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(false);
  const userState = useSelector(state => state.account.selectedAccount);
  const [hashedPasshword, setHashedPassword] = useState(null);

  useEffect(()=>{
    setUser(userState)
  }, []);

  return (
    <UserContext.Provider value={{ user, setUser, loading, setLoading, hashedPasshword, setHashedPassword }} >
      <div className='App'>
          <Routes>
              <Route path='/' element={<Login />}/> 
              <Route path='/signup' element={<SignUp />} />
              <Route path='/main' element={<PrivateRoute component={Main}/>}/>
          </Routes>
      </div>
    </UserContext.Provider>
  );
}

export default App;