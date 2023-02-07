import React, { useEffect, useState } from "react";
import Navbar from "../components/Navbar";
import "./ClassifyScreen.css";

function Classify() {
  const [text, setText] = useState(0);
  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);

  const handleClick = () => {
    if (text === 0) {
      setText(1);
    } else {
      setText(0);
    }
  };
  return (
    <>
      <Navbar />
      <div className="classify-screen">
        <h1>Classify</h1>
        <textarea rows={30} cols={100} id="tex"></textarea>
        <button type="button" className="classify-btn" onClick={handleClick}>
          Classify
        </button>
        <p className={text === 0 ? `classify-hidden` : `classify-active`}>
          The News Is Classified as : News
        </p>
      </div>
    </>
  );
}
export default Classify;
