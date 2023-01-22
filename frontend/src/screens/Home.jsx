import React, { useEffect } from "react";
import Cards from "../components/Cards";
import HeroSection from "../components/HeroSection";

function Home() {
  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);

  return (
    <>
      <HeroSection />
      <Cards />
    </>
  );
}

export default Home;
