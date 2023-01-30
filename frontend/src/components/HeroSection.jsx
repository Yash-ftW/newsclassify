import React from "react";
import Button from "./Button";

import "./HeroSection.css";

import Vid1 from "../videos/video-1.mp4";

function HeroSection() {
  return (
    <div className="hero-container">
      <video src={Vid1} autoPlay loop muted />
      <h1>ClassifyMe</h1>
      <p>Classify or Scrape The News</p>
      <div className="hero-btns">
        <Button
          className="btns"
          buttonStyle="btn--outline"
          buttonSize="btn--large"
          path="classify"
        >
          Classify <i class="fa-solid fa-right-to-bracket"></i>
        </Button>
        <Button
          className="btns"
          buttonStyle="btn--primary"
          buttonSize="btn--large"
          path="/about"
        >
          Scrape <i class="fa-solid fa-circle-info"></i>
        </Button>
      </div>
    </div>
  );
}

export default HeroSection;
