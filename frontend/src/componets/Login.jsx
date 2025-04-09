import React,{ useState } from 'react';
import Header from './Header';

function Input(props) {
    return (
        <div className="input-group">
            <label htmlFor={props.id}>{props.label}</label>
            <input id={props.id} type={props.type} name={props.name} placeholder={props.placeholder} required={props.required} />
        </div>
    );

}

function Login() {
    return (
        <div className="login-container">
            <div className='login-box'>
            <Header text='Stuff Login'/>
            <form method="POST" action="/login">
                <Input id="username" label="Username" type="text" name="username" placeholder="Enter your username" required={true} />
                <Input id="password" label="Password" type="password" name="password" placeholder="Enter your password" required={true} />
                <button type="submit">Login</button>
            </form>
            </div>
        </div>
    );
}
export default Login;