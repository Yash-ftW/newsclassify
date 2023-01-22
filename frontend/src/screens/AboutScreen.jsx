import React, { useEffect } from "react";

function AboutScreen() {
  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);

  return <div>AboutScreen</div>;
}

export default AboutScreen;
