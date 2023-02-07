import React from "react";
import Navbar from "./Navbar";

const Header = () => {
  return (
    <div id="main">
      <Navbar />
      <div className="name">
        <h1>
          <span>Newsify : Your News Classifier </span>
        </h1>
        <p className="details">
          Lorem ipsum dolor, sit amet consectetur adipisicing elit. Iure
          voluptate consequuntur et. Cupiditate inventore asperiores magni
          fugiat perferendis, quaerat repellendus porro minus eos labore illum
          quae! Delectus a eius earum!
        </p>
        <a href="/" className="cv-btn">
          Classify
        </a>
      </div>
    </div>
  );
};

export default Header;
