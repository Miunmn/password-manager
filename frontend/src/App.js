import './App.css';
import { Routes, Route} from "react-router-dom";

//Pages
import Login from './pages/Login/Login';

function App() {

  return (
    <div className='App'>
        <Routes>
            <Route exact path='/' element={<Login />}/>           
        </Routes>
    </div>
  );
}

export default App;
