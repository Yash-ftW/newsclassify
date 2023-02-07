import React from "react";
import { Link } from "react-router-dom";

const About = (props) => {
  return (
    <div id="about">
      <div className="about-image">
        <img src={props.image} alt="" />
      </div>
      <div className="about-text">
        <h2>{props.title}</h2>
        <p>
          Lorem ipsum dolor sit amet consectetur adipisicing elit. Doloribus,
          id?
        </p>
        <Link to={props.path}>
          <button>{props.button}</button>
        </Link>
      </div>
    </div>
  );
};

export default About;
