import React from "react";
import "./Loader.css";

const LoaderEng = () => {
  return (
    <div className="spinnerContainer">
      <div className="spinner"></div>
      <div className="loader">
        <p className="load-p">Scraping</p>
        <div className="words">
          <span className="word">The Kathmandu Post</span>
          <span className="word">BBC</span>
          <span className="word">The Kathmandu Post</span>
          <span className="word">BBC</span>
          <span className="word">The Kathmandu Post</span>
        </div>
      </div>
    </div>
  );
};

export default LoaderEng;
