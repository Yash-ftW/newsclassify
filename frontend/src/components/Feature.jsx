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
        <FeatureBox
          image={featureimage}
          title="Classify"
          detail="Bringing Clarity to the News: Automatically Categorize and Organize"
        />
        <FeatureBox
          image={featureimage1}
          title="Summarize"
          detail="Get the gist in a jiffy: Summarize News Stories Effortlessly with Our News Summarizer."
        />
        <FeatureBox
          image={featureimage2}
          title="Scrape"
          detail="Stay Ahead of the Game: Automatically Extract the Latest News with Our News Scraper."
        />
      </div>
    </div>
  );
};

export default Feature;
