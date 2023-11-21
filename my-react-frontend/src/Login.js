import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';

function Login() {
  return (
    <div className="login-body">
      <h1 style={{ marginTop: '60px', marginBottom: '20px', color: 'white' }}>JOB SEARCH</h1>
      <div className="container">
        <form action="/dashboard" method="GET">
          <h1 className="h3 mb-3 fw-normal" style={{ color: 'white' }}>Please sign in</h1>
          <div className="form-floating">
            <input type="text" className="form-control" id="name" name="name" placeholder="first_name last_name" required />
            <label htmlFor="name">Full Name</label>
          </div>
          <div className="form-floating">
            <input type="email" className="form-control" id="email" name="email" placeholder="name@example.com" required />
            <label htmlFor="email">Email address</label>
          </div>
          <div className="form-floating">
            <input type="password" className="form-control" id="floatingPassword" name="password" placeholder="Password" required />
            <label htmlFor="floatingPassword">Password</label>
          </div>
          <button type="submit" className="btn btn-primary w-100 py-2">Sign in</button>
        </form>
      </div>
    </div>
  );
}

export default Login;
