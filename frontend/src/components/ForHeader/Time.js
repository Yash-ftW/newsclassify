import React, { useEffect, useState } from "react";

function Time() {
  const [clock, setClock] = useState();

  useEffect(() => {
    setInterval(() => {
      const time = new Date();
      setClock(time.toLocaleTimeString());
    }, 1000);
  }, []);
  return <div className="pe-none">{clock}</div>;
}

export default Time;
