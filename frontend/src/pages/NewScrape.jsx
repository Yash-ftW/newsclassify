import React, { useEffect, useState } from "react";
import "./NewScrape.css";
import axios from "axios";
import { Toaster, toast } from "react-hot-toast";
import { useNavigate } from "react-router-dom";
import LoaderEng from "../components/LoaderEng";
import LoaderNep from "../components/LoaderNep";

const NewScrape = () => {
  const [engLoading, setEngLoading] = useState(false);
  const [nepLoading, setNepLoading] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {}, []);

  const engScrape = async () => {
    setEngLoading(true);
    await axios
      .get("/scrapeEnglishNews")
      .then((res) => {
        console.log(res.data);
        setEngLoading(false);
        toast.success("Scraped Successfully");
      })
      .catch((err) => {
        toast.error("Somethin Went Wrong: " + err);
        return;
      });
  };

  const nepScrape = async () => {
    setNepLoading(true);
    await axios
      .get("/scrapeNepaliNews")
      .then((res) => {
        console.log(res.data);
        setNepLoading(false);
        toast.success("Scraped Successfully");
      })
      .catch((err) => {
        toast.error("Somethin Went Wrong: " + err);
        return;
      });
  };

  const handleClick = () => {
    navigate(-1);
  };

  return (
    <>
      <div className="scrape-back" onClick={handleClick}>
        <span className="scrape-arrow"></span>
      </div>
      <div className="new-wrapper">
        <Toaster />
        <div className="scrape-box">
          <h1 className="scrape-head-new">Scrape News</h1>
          {engLoading && <LoaderEng />}
          {nepLoading && <LoaderNep />}
          <div className="btn-wrap-new">
            <button className="new-btn" onClick={engScrape}>
              Scrape English
            </button>
            <button className="new-btn" onClick={nepScrape}>
              Scrape Nepali
            </button>
          </div>
        </div>
      </div>
    </>
  );
};

export default NewScrape;
