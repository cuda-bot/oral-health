// src/App.js
import React from "react";
import ImageUpload from "./ImageUpload";
import "./App.css";

function App() {
  return (
    <div className="App">
      <div className="container">
        <div className="logo">
          <i className="fas fa-tooth"></i>
        </div>
        <h1>Oral Health AI</h1>
        <p className="subtitle">Upload a dental image to get instant analysis and detect potential oral health conditions</p>

        <ImageUpload />

        <div className="features">
          <div className="feature">
            <div className="feature-icon">
              <i className="fas fa-bolt"></i>
            </div>
            <div className="feature-title">Fast Analysis</div>
            <div className="feature-desc">Get results in seconds</div>
          </div>
          <div className="feature">
            <div className="feature-icon">
              <i className="fas fa-shield-alt"></i>
            </div>
            <div className="feature-title">Secure</div>
            <div className="feature-desc">Your data is protected</div>
          </div>
          <div className="feature">
            <div className="feature-icon">
              <i className="fas fa-brain"></i>
            </div>
            <div className="feature-title">AI Powered</div>
            <div className="feature-desc">Advanced ML algorithms</div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;

