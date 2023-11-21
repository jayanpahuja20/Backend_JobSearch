// UserDashboard.js
import React from 'react';

const UserDashboard = ({ name, email, location, experience }) => {
  return (
    <>
      <head>
        <meta charSet="UTF-8" />
        <title>User Dashboard</title>
        <link
          href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css"
          rel="stylesheet"
          integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN"
          crossOrigin="anonymous"
        />
        <style>
          {`
            body {
              background-color: #363636;
              display: block;
              justify-content: center;
              margin-top: 60px;
              height: 100vh;
            }
            h3, h1 {
              color: white;
              justify-content: center;
              align-items: center;
              display: flex;
            }
            p {
              color: lightgray;
              width: 70%;
              margin: 0 auto;
              text-align: justify;
            }
            .button-container {
              display: flex;
              justify-content: center;
              align-items: center;
              margin-top: 20px;
            }
            .button-container form {
              margin-right: 10px;
            }
          `}
        </style>
      </head>
      <body>
        <script
          src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"
          integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL"
          crossOrigin="anonymous"
        ></script>
        <h1> USER DASHBOARD</h1>
        <h3> NAME: {name}</h3>
        <h3> EMAIL: {email}</h3>
        <h3> LOCATION: {location}</h3>
        <h3> EXPERIENCE: {experience}</h3>
      </body>
    </>
  );
};

export default UserDashboard;
