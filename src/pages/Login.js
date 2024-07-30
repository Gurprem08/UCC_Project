// src/pages/LoginRegisterPage.js
import React, { useState } from 'react';
import { getAuth, createUserWithEmailAndPassword, signInWithEmailAndPassword } from 'firebase/auth';
import { Form } from 'react-bootstrap';

const LoginRegisterPage = () => {
  
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isRegistering, setIsRegistering] = useState(false);
  const [error, setError] = useState(null);
  const [isChecked , setIsChecked] = useState(false)
  const [name, setName] = useState('')

  const auth = getAuth();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError(null);
    try {
      await signInWithEmailAndPassword(auth, email, password);
    } catch (error) {
      setError(error.message);
    }
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    setError(null);
    try {
      await createUserWithEmailAndPassword(auth, email, password);
    } catch (error) {
      setError(error.message);
    }
  };


  return (
    <div style={{margin:'80px'}}>
      
    <div className="login-register-page">
      <h2>{isRegistering ? 'REGISTER' : 'SIGN IN'}</h2>
      <form onSubmit={isRegistering ? handleRegister : handleLogin}>

    {isRegistering  && (
      <>
      <div >
    <label style={{ fontWeight: 'bold' }} >Name:</label>
    <input
      type="text"
      id="name"
      value={name}
      onChange={(e) => setName(e.target.value)}
      placeholder="Enter your Name"
      style={{marginLeft:'auto', marginRight:'auto', width:'450px', height:'50px', }}
      required
      />
  </div>
  <div >
    <label style={{ fontWeight: 'bold' }} htmlFor="phone">Phone Number:</label>
    <input
      type="tel"
      id="phone"
      placeholder="Please Enter Phone Number"
      style={{marginLeft:'auto', marginRight:'auto', width:'450px', height:'50px', }}
      required
      />
      </div>
      </>
      )}
  

        <div >
          <label style={{fontWeight:'bold'}} >Email:</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder='Enter your Email'
            style={{marginLeft:'auto', marginRight:'auto', width:'450px', height:'50px', }}
            required
            
      
          />
        </div>
        <div>
          <label style={{fontWeight:'bold'}}>Password:</label>
          <input
            type="password"
            value={password}
            placeholder='Enter your password'
            onChange={(e) => setPassword(e.target.value)}
            required
            style={{marginLeft:'auto', marginRight:'auto', width:'450px', height:'50px', }}
          />
        </div>
        <Form.Group controlId="consentCheckbox" className="mt-6 checkbox-container">
        <Form.Check
        type="checkbox"
      
       
        checked={isChecked}
        onChange={() => { setIsChecked(prevState => !prevState) }}

      />
      <Form.Label style={{ color: "black" , marginBottom:"20px", marginLeft:'auto', marginRight:'auto'}}> This data is protected under India's Data Protection Act 2023.</Form.Label>

      </Form.Group>
        {error && <p className="error">{error}</p>}
        {isChecked ? (

          <button type="submit">{isRegistering ? 'Continue' : 'Continue'}</button>
        ):null}
      </form>
      <button style = {{fontSize:'20px'}}onClick={() => setIsRegistering(!isRegistering)}>
        {isRegistering ? 'Already have an account? Login' : "Don't have an account? Register"}
      </button>
    </div>
  </div>
  );
};

export default LoginRegisterPage;
