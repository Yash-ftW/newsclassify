import React, { useEffect, useState } from "react";
import Navbar from "../components/Navbar";
import "./ClassifyScreen.css";
import axios from "axios";
import Loader from "../components/Loader";

const Form = () => {
  const [field1Value, setField1Value] = useState("");
  const [field2Value, setField2Value] = useState("");

  const [result, setResult] = useState(false);
  const [loading, setLoading] = useState(false);
  const [resp, setResp] = useState({});

  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);

  const handleField1Change = (event) => {
    setField1Value(event.target.value);
  };

  const handleField2Change = (event) => {
    setField2Value(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    setLoading(true);
    axios
      .post("http://localhost:5000/api/form", {
        field1: field1Value,
        field2: field2Value,
      })
      .then((response) => {
        console.log(response.data);
        setLoading(false);
        setResp(response.data);
        setResult(true);
      })
      .catch((err) => {
        console.log(err);
      });
  };

  return (
    <>
      <Navbar />
      <div className="wrapper">
        <div className="classify-screen">
          <form onSubmit={handleSubmit}>
            <label>
              <textarea
                type="text"
                value={field1Value}
                onChange={handleField1Change}
                rows={30}
                cols={100}
                required
              />
            </label>
            <br />
            <label>
              <input
                type="number"
                value={field2Value}
                onChange={handleField2Change}
                placeholder="Summarized Sentence Count"
                required
              />
            </label>
            <br />
            <button type="submit" className="classify-btn">
              Submit
            </button>
          </form>
          {loading ? (
            <Loader />
          ) : (
            <div className={!result ? `classify-hidden` : `classify-active`}>
              <div>
                <p>The News Is Classified as : {resp.prediction}</p>
                <p>Summary:{resp.summarized}</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </>
  );
};

export default Form;
