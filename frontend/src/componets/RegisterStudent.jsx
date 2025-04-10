import React,{useState} from "react";
import Header from "./Header";
import { useNavigate } from "react-router-dom";
import { Input } from "./Login";

function RegisterStudent() {
    const [state,setState] = useState({
        class:"",
        first_name:"",
        last_name:"",
        
    })
    const navigate = useNavigate();
    const handleChange = (e) => {
        const { name, value } = e.target;
        setState((prevData) => ({
          ...prevData,
          [name]: value
        }));
      };
    
    function onDone(event){
        event.preventDefault();
        return fetch('http://localhost:5000/api/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(state)
        }).then((response) => {
            if(response.status === 200){
                navigate('/login')
            }
            else{
                alert("Registration failed")
            }
        })
        
    };
    return (
        
        <div className="login-container">
            <div className='login-box'>
            <Header text='Student Registration' />
            <p>Register to a student account</p>
            <form method="POST" onSubmit={onDone}>
                <Input id="class" label="Class" type="text" name="class" placeholder="Enter your class" required={true} onChange={handleChange}/>
                <Input id="first_name" label="First Name" type="text" name="first_name" placeholder="Enter your first name" required={true} onChange={handleChange}/>
                <Input id="last_name" label="Last Name" type="text" name="last_name" placeholder="Enter your last name" required={true} onChange={handleChange}/>
                <button type="submit">Register</button>
            </form>
            </div>
        </div>
    );
}