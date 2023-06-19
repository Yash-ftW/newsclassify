import React from "react";
import "./Loader.css";

const LoaderNep = () => {
  return (
    <div className="spinnerContainer">
      <div className="spinner"></div>
      <div className="loader">
        <p className="load-p">Scraping</p>
        <div className="words">
          <span className="word">Ekantipur</span>
          <span className="word">Setopati</span>
          <span className="word">Ekantipur</span>
          <span className="word">Setopati</span>
          <span className="word">Ekantipur</span>
        </div>
      </div>
    </div>
  );
};

export default LoaderNep;
