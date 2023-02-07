import React from "react";
import { Link } from "react-router-dom";
import "./StartScreen.css";
import Navbar from "../components/Navbar";

const StartScreen = () => {
  return (
    <>
      <Navbar />
      <div className="start">
        <div className="start-text">
          <h1>Choose</h1>
        </div>
        <div className="start-screen">
          <Link to="/classify">
            <div className="start-card classify"></div>
          </Link>
          <Link to="/summarize">
            <div className="start-card summarize"></div>
          </Link>
          <Link to="/scrape">
            <div className="start-card scrape"></div>
          </Link>
        </div>
      </div>
    </>
  );
};

export default StartScreen;
