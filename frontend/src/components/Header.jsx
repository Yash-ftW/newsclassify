import React from "react";
import Navbar from "./Navbar";

const Header = () => {
  return (
    <div id="main">
      <Navbar />
      <div className="name">
        <h1>
          <span>
            SNS : <br />
            Short And Simple
          </span>
        </h1>
        <p className="details" style={{ color: "black" }}>
          Welcome to our SNS website, where we summarize long news articles and
          provide you with a quick overview of the most important information.
          In today's fast-paced world, it can be challenging to keep up with the
          latest news and events. With so much information available, it's easy
          to get overwhelmed and miss out on crucial stories.
        </p>
        <a href="/" className="cv-btn">
          Classify
        </a>
      </div>
    </div>
  );
};

export default Header;
