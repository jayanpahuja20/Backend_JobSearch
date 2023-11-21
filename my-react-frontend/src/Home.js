
import React from 'react';

const home = () => {
  return (
    <>
      <head>
        <meta charSet="UTF-8" />
        <title>Job Search</title>
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
            h1 {
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
        <h1> JOB SEARCH</h1>
        <p>
          The job market is dynamic and ever-evolving, with job seekers and
          employers alike needing access to accurate and up-to-date information
          on job openings. In this context, our portal aims to provide a
          seamless and efficient platform for job seekers to explore
          opportunities and for employers to connect with potential candidates.
          In light of the prevailing economic trends and the ongoing recession,
          the job market has become more competitive than ever. Job seekers are
          grappling with the challenge of identifying suitable employment
          opportunities that align with their skills and interests.
        </p>
        <div className="button-container">
          <form action="/login" method="get">
            <button className="btn btn-primary rounded-pill px-3" type="submit">
              LOGIN
            </button>
          </form>
          {/* Uncomment the following lines if you have a signup route */}
          {/* <form action="/signup" method="get">
            <button className="btn btn-primary rounded-pill px-3" type="submit">
              SIGN UP
            </button>
          </form> */}
        </div>
      </body>
    </>
  );
};

export default home;
