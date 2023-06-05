import React, {useState} from "react"
import './index.css'
import {useForm} from "react-hook-form"


import { Link} from "react-router-dom";



export default function Login(){
    const [formData, setFormData] = useState({});
    const{register,handleSubmit,reset}=useForm();
    const [registrationSuccess, setRegistrationSuccess] = useState(false);
  

    function handlePost(data) {
        setFormData(data);
        reset();
      
        // Pobranie tokena CSRF
        fetch('http://127.0.0.1:8000/api/tokenCNF/')
          .then(response => response.json())
          .then(data => {
            const csrfToken = data.csrf_token;
      
            // Wysłanie żądania POST z tokenem CSRF w nagłówku
            fetch('http://127.0.0.1:8000/api/login/', { // do zmiany 
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
              },
              body: JSON.stringify(formData),
            })
              .then(response => response.text())
              .then(data => {
                console.log('Success:', data);
                setRegistrationSuccess(true);
                setFormData({});
                reset();
              })
              .catch(error => {
                console.error('Error:', error);
              });
          })
          .catch(error => {
            console.error('Error:', error);
          });
      }

    return (
        
        <div className="auth-form-container">
         
        <form className ="login-form" onSubmit={handleSubmit(handlePost)} >
            
            <h1 className="purples">Play with me!</h1>
            <label for="login">email</label>
            <input type="login" placeholder="email@gmail.com" 
            id ="email" name = "username"required maxlength="50"/>
            <span id="usernameError" class="error"></span>
           

            
                
            <label for="password">password</label>
            <input type="password" id ="password" name = "password" 
            required maxlength="50" />   
            <span id="usernameError" class="error"></span>
            

            <button class ="custom-btn"  >Zaloguj się </button>
            <Link to="/register" class="bbutton">Nie masz konta? Zarejestruj się</Link>

        </form>
            
        
        
        </div>
        
        
    );

    }
