import React, { useEffect } from "react";

function FeaturesScreen() {
  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);
  return <div className="h-screen">FeaturesScreen</div>;
}

export default FeaturesScreen;
