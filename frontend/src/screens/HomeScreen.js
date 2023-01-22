import React from "react";
import { Container } from "react-bootstrap";

import Img1 from "../images/report.jpeg";
import Img2 from "../images/analysis.jpg";
import Img3 from "../images/recommend.jpg";

function HomeScreen() {
  return (
    <>
      <div className="banner">
        <h1>SIRUS</h1>
        <h3>Student Evaluation System</h3>
      </div>
      <section className="feat">
        <h2>Features</h2>
        <div className="line"></div>
        <div className="features">
          <div className="feature feature-1">
            <h5>Report Prediction</h5>
            <img src={Img1} alt="Feature1" />
          </div>
          <div className="feature feature-2">
            <h5>Student Analysis</h5> <img src={Img2} alt="Feature2" />
          </div>
          <div className="feature feature-3">
            <h5>Recommendation</h5> <img src={Img3} alt="Feature3" />
          </div>
        </div>
      </section>
      {/* <div className="features">
        <div className="feature feature-1">
          <h2>Report Prediction</h2>
        </div>
        <div className="feature feature-2">
          <img src={Img1} alt="Feature1" />
        </div>
        <div className="feature feature-3">
          <h2>Student Evalutaion</h2>
        </div>
        <div className="feature feature-4">
          <img src={Img2} alt="Feature2" />
        </div>
      </div> */}
    </>
  );
}

export default HomeScreen;
