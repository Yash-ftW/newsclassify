import React from "react";

import Navbar from "./Navbar";

const Header = () => {
  return (
    <div id="main">
      <Navbar />

      <div className="name">
        <h1>
          <span>Snap News</span>
        </h1>
        <h2 className="name2">
          Stay Informed, In Just A Few Lines -<br />{" "}
          <span className="name2__text">Your Daily News Digest</span>
        </h2>
        <p className="details" style={{ color: "black" }}>
          Welcome to Snap News, where we summarize long news articles and
          provide you with a quick overview of the most important information.
        </p>
        <a href="/classify" className="cv-btn">
          Classify
        </a>
      </div>
    </div>
  );
};

export default Header;
