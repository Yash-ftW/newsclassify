import React from "react";
import FeatureBox from "./FeatureBox";
import featureimage from "../images/feature_1.png";
import featureimage1 from "../images/feature_2.png";
import featureimage2 from "../images/feature_3.png";

const Feature = () => {
  return (
    <div id="features">
      <h1 className="feat-title">Features</h1>
      <div className="a-container">
        <FeatureBox image={featureimage} title="Classify" />
        <FeatureBox image={featureimage1} title="Summarize" />
        <FeatureBox image={featureimage2} title="Scrape" />
      </div>
    </div>
  );
};

export default Feature;
