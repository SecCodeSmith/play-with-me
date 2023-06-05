import React, {useState} from "react"
import { Link} from "react-router-dom";
import {useForm} from "react-hook-form"


export default function Register(){
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
            console.log(csrfToken)
            // Wysłanie żądania POST z tokenem CSRF w nagłówku
            fetch('http://127.0.0.1:8000/api/register/', { // do zmiany 
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
          {registrationSuccess && <p>Rejestracja zakończona sukcesem!</p>} {/* Wyświetlanie komunikatu o sukcesie */}
        <form className ="register-form" onSubmit={handleSubmit(handlePost)}>
        
            <h1 className="purples">Play with me!</h1>
            
            <label htmlFor="login">email</label>
            <input type="email" placeholder="email@gmail.com" 
            id ="email" name = "email"required maxlength="50"
            
            />
            <label for="username">username</label>
            <input type="text" id ="username" name = "username" 
            required maxlength="50"
            />
            
                 
            <label for="password">password</label>
            <input type="password" id ="password" name = "password1" 
            required maxlength="50"
            
            />   
            
               
            <label for="confirmPassword">confirm password</label>
            <input type="password" id ="confirmPassword" name = "password2" 
            required maxlength="50"
            
            />   
            
            <label for="language">language</label>
            <input type="text" id ="language" name = "language" 
            required maxlength="50"
            defaultValue="English"/>
           

            <button class = "custom-btn">Zarejestruj sie</button>
            <Link to="/login" class="bbutton">Mam już konto!</Link>
        </form>
            
        
        </div>
        
        
    );
}


