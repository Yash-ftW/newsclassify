import React, { useEffect, useState } from "react";
import Navbar from "../components/Navbar";
import "./ClassifyScreen.css";
import axios from "axios";
import Loader from "../components/Loader";

function Classify() {
  const [text, setText] = useState(0);
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);
  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);

  const handleClick = async () => {
    setLoading(true);
    if (text === 0) {
      setText(1);
    } else {
      setText(0);
    }
    await axios.get("/data").then((res) => {
      setResult(res.data.Hello);
      setLoading(false);
    });
    window.scrollTo(100, 100);
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
        {loading ? (
          <Loader />
        ) : (
          <p className={text === 0 ? `classify-hidden` : `classify-active`}>
            The News Is Classified as : {result}
          </p>
        )}
      </div>
    </>
  );
}
export default Classify;
