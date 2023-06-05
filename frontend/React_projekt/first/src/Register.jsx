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
    
      // Przygotowanie danych do wysłania
      const requestData = {
        email: data.email,
        username: data.username,
        password1: data.password1,
        password2: data.password2,
        language: data.language
      };
    
      // Wysłanie żądania POST
      fetch('http://127.0.0.1:8000/api/register/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData),
      })
        .then(response => response.json())
        .then(data => {
          console.log('Success:', data);
          setRegistrationSuccess(data.status === "Create new user success");
          setFormData({});
          reset();
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
            {...register("email")}
            />
            <label for="username">username</label>
            <input type="text" id ="username" name = "username" 
            required maxlength="50"
            {...register("username")}

            />
            
                 
            <label for="password">password</label>
            <input type="password" id ="password" name = "password1" 
            required maxlength="50"
              {...register("password1")}

            />   
            
               
            <label for="confirmPassword">confirm password</label>
            <input type="password" id ="confirmPassword" name = "password2" 
            required maxlength="50"
              {...register("password2")}

            />   
            
            <label for="language">language</label>

           

            <button class = "custom-btn">Zarejestruj sie</button>
            <Link to="/login" class="bbutton">Mam już konto!</Link>
        </form>
            
        
        </div>
        
        
    );
}


