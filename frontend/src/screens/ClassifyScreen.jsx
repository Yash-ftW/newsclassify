import React, { useEffect } from "react";
import "./ClassifyScreen.css";

function Classify() {
  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);
  return (
    <div className="flex justify-start items-center flex-col h-screen news">
      <div className="w-75 p-2 mt-5 flex justify-center items-center flex-col">
        <h1 className="text-4xl p-4 text-white">Classify</h1>
        <div>
          <textarea placeholder="Enter Some News" className="news-text" />
        </div>
        <button type="button" className="btn-5 m-3">
          Submit
        </button>
      </div>
      <div className="text-2xl">
        The Above News is Classified as : <br />
        <span className="neon flex justify-center items-center">{`<News>`}</span>
      </div>
    </div>
  );
}
export default Classify;
