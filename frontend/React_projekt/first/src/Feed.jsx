import { Box,Button, HStack, Heading,Textarea } from "@chakra-ui/react";

import "./feed.css"

import {useForm} from "react-hook-form"
import React, { useState } from 'react';


export default function Feed(){
    const [formData, setFormData] = useState({});


    const{register,handleSubmit,reset}=useForm();

    function handlePost(data) {
        setFormData(data);
        reset();
      
        // Pobranie tokena CSRF
        fetch('127.0.0.1:8000/api/tokenCNF/')
          .then(response => response.json())
          .then(data => {
            const csrfToken = data.csrf_token;
      
            // Wysłanie żądania POST z tokenem CSRF w nagłówku
            fetch('URL_BACKEND', { // do zmiany 
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
              },
              body: JSON.stringify(formData),
            })
              .then(response => response.json())
              .then(data => {
                console.log('Success:', data);
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
    <Box id="box"maxW="600px" mx="auto" py="200" >
    <form onSubmit={handleSubmit(handlePost)}>
    <HStack id="stack"justify ="space-between">
        <Heading id="heading"size ="lg">New post</Heading>
        <Button id="button"colorScheme="teal" type="submit">Post</Button>
    </HStack>
    <Textarea id="textarea"resize="none"
      mt="5" width={800} height={100}
       placeholder="Wpisz tekst..."{...register("text",{required:true})} />
    </form>

</Box>
   
    );
        
    
        
}