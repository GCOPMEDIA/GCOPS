import React ,{useState}from "react";
import { Input } from "./Login";
import Header from "./Header";

function Subject(props){
    return <div className="subject">
        <Input id="subject" label="Subject Title" type="text" name="subject" placeholder="Enter the subject title" required={true} onChange={props.change}/>
        <span><Input id="exams" label="Examination Score" type="text" name="exams_score" placeholder="Enter the exam score" required={true} onChange={props.change} /></span>
        <span><Input id= "class_score" label="Class Score" type="text" name="class_score" placeholder="Enter the class score" required={true} onChange={props.change} />  </span>  
    </div>
}


function Grade(){
    const [state,setState] = useState({
        username:"",
        password:""
    })
    const handleChange = (e) => {
        const { name, value } = e.target;
        setState((prevData) => ({
          ...prevData,
          [name]: value
        }));
      };

    function onDone(event){
        const { name, value } = event.target;
        
        event.preventDefault();
        return fetch('http://localhost:5000/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(state)
        })
        
    };
    return (
        <div className="login-container">
            <div className='login-box'>
            <Header text='Student Results' />
            <p>Provide the </p>
            <form method="POST" onSubmit={onDone}>
            <Subject change={handleChange}/>
            <Subject change={handleChange}/>
            <Subject change={handleChange}/>           
            <Subject change={handleChange}/>
            <Subject change={handleChange}/>            
            <Subject change={handleChange}/>
            <Subject change={handleChange}/>
            <Subject change={handleChange}/>
            <Subject change={handleChange}/>            
            <button type="submit">submit Results</button>
            </form>
            </div>
        </div>
    )
}