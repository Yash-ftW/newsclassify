import React, { useEffect } from "react";
import axios from "axios";

const Try = () => {
  useEffect(() => {
    axios.get("/data").then((res) => {
      console.log(res.data.Hello);
    });
  }, []);

  return <div>Try</div>;
};

export default Try;
