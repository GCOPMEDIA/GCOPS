import React,{ useState } from 'react';
import Header from './Header';

function Input(props) {
    return (
        <div className="input-group">
            <label htmlFor={props.id}>{props.label}</label>
            <input id={props.id} type={props.type} name={props.name} placeholder={props.placeholder} required={props.required} onChange={props.onChange}/>
        </div>
    );

}

function Login() {
    
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
            <Header text='Stuff Login' />
            <p>Login to your account</p>
            <form method="POST" onSubmit={onDone}>
                <Input id="username" label="Username" type="text" name="username" placeholder="Enter your username" required={true}  onChange={handleChange} />
                <Input id="password" label="Password" type="password" name="password" placeholder="Enter your password" required={true} onChange={handleChange}/>
                <button type="submit" >Login</button>
            </form>
            </div>
        </div>
    );
}
export default Login;
export { Input };