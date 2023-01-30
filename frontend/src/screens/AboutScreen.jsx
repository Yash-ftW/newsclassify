import React, { useEffect } from "react";

function AboutScreen() {
  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);

  return <div className="h-screen">AboutScreen</div>;
}

export default AboutScreen;
