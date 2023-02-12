import React, { useEffect, useState } from "react";
import Navbar from "../components/Navbar";
import "./ClassifyScreen.css";
import axios from "axios";
import Loader from "../components/Loader";

const Form = () => {
  const [field1Value, setField1Value] = useState("");
  const [field2Value, setField2Value] = useState("");
  const [text, setText] = useState(0);

  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);
  const [resp, setResp] = useState({});

  const handleField1Change = (event) => {
    setField1Value(event.target.value);
  };

  const handleField2Change = (event) => {
    setField2Value(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    axios
      .post("http://localhost:5000/api/form", {
        field1: field1Value,
        field2: field2Value,
      })
      .then((response) => {
        console.log(response.data);
        setResp(response.data);
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
              />
            </label>
            <br />
            <label>
              <input
                type="text"
                value={field2Value}
                onChange={handleField2Change}
              />
            </label>
            <br />
            <button type="submit" className="classify-btn">
              Submit
            </button>
          </form>
          <p>The News Is Classified as : {resp.prediction}</p>
        </div>
      </div>
    </>
  );
};

export default Form;
