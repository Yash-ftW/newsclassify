import React from "react";
import "./Loader.css";

const Loader = () => {
  return (
    <div className="c-load-wrap">
      <div className="c-loader">
        <div className="c-loader-square"></div>
        <div className="c-loader-square"></div>
        <div className="c-loader-square"></div>
        <div className="c-loader-square"></div>
        <div className="c-loader-square"></div>
        <div className="c-loader-square"></div>
        <div className="c-loader-square"></div>
      </div>
    </div>
  );
};

export default Loader;
