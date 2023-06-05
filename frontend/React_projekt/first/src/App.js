import logo from './logo.svg';
import './App.css';
import { ChakraProvider } from '@chakra-ui/react'


import  Register  from './Register';
import  Login  from './Login';

import { Topbar } from './Topbar';
import Home from './Home.jsx'
import React,{ useState } from 'react';
import { BrowserRouter, Routes,Route } from 'react-router-dom';


function App() {
  const[currentForm,setCurrentForm] =useState('login')
  const [isLoggedIn, setLoggedIn] = useState(false);



  //return <Home/> // css sie lekko wypiepsza ale dziala


  return (
    <div className="container">
      
      <BrowserRouter>
        <Routes>
          
          <Route index element={<Login/>}/>
          <Route path="/login" element={<Login/>}/>
          <Route path="/home" element={<Home/>}/>
          <Route path="/register" element={<Register/>}/>
          

      </Routes>
      </BrowserRouter>
    </div>

  );
  
  
}




export default App;
