// import logo from './logo.svg';
// import './App.css';

// function App() {
//   return (
//     <div className="App">
//       <header className="App-header">
//         <img src={logo} className="App-logo" alt="logo" />
//         <p>
//           Edit <code>src/App.js</code> and save to reload.
//         </p>
//         <a
//           className="App-link"
//           href="https://reactjs.org"
//           target="_blank"
//           rel="noopener noreferrer"
//         >
//           Learn React
//         </a>
//       </header>
//     </div>
//   );
// }


import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css'; 
import './App.css';

function App() {
    return (
        <div className="App">
            <h1 style={{ color: 'white', justifyContent: 'center', alignItems: 'center', display: 'flex' }}>JOB SEARCH</h1>
            <p style={{ color: 'lightgray', width: '70%', margin: '0 auto', textAlign: 'justify' }}>
                The job market is dynamic and ever-evolving, with job seekers and employers alike needing access to accurate and up-to-date information on job openings.
                In this context, our portal aims to provide a seamless and efficient platform for job seekers to explore opportunities and for employers to connect with potential candidates.
                In light of the prevailing economic trends and the ongoing recession, the job market has become more competitive than ever.
                Job seekers are grappling with the challenge of identifying suitable employment opportunities that align with their skills and interests.
            </p>
            <div className="button-container">
                <form action="/login" method="get">
                    <button className="btn btn-primary rounded-pill px-3" type="submit">LOGIN</button>
                </form>
                {/* Uncomment the following lines if you want to include the SIGN UP button */}
                {/* <form action="/signup" method="get">
                    <button className="btn btn-primary rounded-pill px-3" type="submit">SIGN UP</button>
                </form> */}
            </div>
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" crossOrigin="anonymous"></script>
        </div>
    );
}

export default App;
