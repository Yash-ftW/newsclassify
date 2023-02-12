import React, { useState } from "react";
import axios from "axios";

const Test = () => {
  const [news, setNews] = useState("");
  const [summ, setSumm] = useState(1);
  const handleSubmit = (e) => {
    e.preventDefault();
    const bodyData = JSON.stringify({
      news,
      summarization_count: summ,
    });
    const reqOpt = {
      method: "POST",
      headers: { "Content-type": "application/json" },
      body: bodyData,
    };
    fetch("http://localhost:5000/classifcation", reqOpt)
      .then((res) => res.json())
      .then((resJ) => console.log(resJ));
    // axios.get("/data").then((res) => {
    //   console.log(res.data);
    // });
    // axios.post("http://localhost:5000/classifcation", {}).then((res) => {
    //   console.log(res.data);
    // });
    // // window.location.replace("http://localhost:5000/classifcation");
  };
  return (
    <form method="POST" onSubmit={handleSubmit}>
      <textarea
        id="textid"
        name="news"
        rows="20"
        cols="75"
        onChange={(e) => setNews(e.target.value)}
      />

      <input
        type="text"
        id="summarization_count"
        name="summarization_count"
        onChange={(e) => setSumm(e.target.value)}
      />

      <input type="submit" value="Summarize and Classify" />
    </form>
  );
};

export default Test;
