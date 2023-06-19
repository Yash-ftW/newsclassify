import React, { useState, useEffect } from "react";
import axios from "axios";

import toast, { Toaster } from "react-hot-toast";
import SourceButton from "../components/SourceButton";

const ScrapedNepali = () => {
  const [scraped, setScraped] = useState({
    title: "",
    link: "",
    date: "",
    summary: "",
    category: "BUSINESS",
  });

  useEffect(() => {
    axios.get("http://localhost:5000/api/fetchScrapeNepali").then((response) => {
      console.log(response);
      setScraped({
        title: response.data.title,
        link: response.data.link,
        date: response.data.date,
        summary: response.data.summary,
        category: response.data.category,
      });
    });
  }, []);

  const nextNews = async (event) => {
    const prev = "Previous News";
    const next = "Next News";
    const dest = event.target.innerText === prev ? prev : next;

    if (dest === prev) {
      await axios
        .post("/api/fetchScrapeNepali", { dest, changeCategory: "" })
        .then((response) =>
          setScraped({
            title: response.data.title,
            link: response.data.link,
            date: response.data.date,
            summary: response.data.summary,
            category: response.data.category,
          })
        )
        .catch((error) => {
          toast.error("Something Went Wrong");
        });
    } else {
      await axios
        .post("/api/fetchScrapeNepali", { dest, changeCategory: "" })
        .then((response) =>
          setScraped({
            title: response.data.title,
            link: response.data.link,
            date: response.data.date,
            summary: response.data.summary,
            category: response.data.category,
          })
        )
        .catch((error) => {
          toast.error("Something Went Wrong");
        });
    }
  };

  const handleCatChange = (event) => {
    let next;
    let prev;
    switch (scraped.category?.toUpperCase()) {
      case "BUSINESS":
        prev = "OTHERS";
        next = "ENTERTAINMENT";
        break;

      case "ENTERTAINMENT":
        prev = "BUSINESS";
        next = "POLITICS";
        break;

      case "POLITICS":
        prev = "ENTERTAINMENT";
        next = "SPORT";
        break;

      case "SPORT":
        prev = "POLITICS";
        next = "TECH";
        break;

      case "TECH":
        prev = "SPORT";
        next = "OTHERS";
        break;

      case "OTHERS":
        prev = "TECH";
        next = "BUSINESS";
        break;

      default:
        prev = "BUSINESS";
        next = "BUSINESS";
        break;
    }

    const category =
      event.target.innerText === "Previous Category" ? prev : next;
    axios
      .post("/api/fetchScrapeNepali", {
        changeCategory: category,
      })
      .then((response) => {
        setScraped({
          title: response.data.title,
          link: response.data.link,
          date: response.data.date,
          summary: response.data.summary,
          category: response.data.category,
        });
      })
      .catch((error) => {
        toast.error("No More Category");
      });
  };

  return (
    <>
      <div className="scraped-nepali">
        <Toaster />
        <div className="left">
          <div className="left-arrow-box">
            <button className="cv-btn" onClick={handleCatChange}>
              Previous Category
            </button>
            <button className="cv-btn" onClick={handleCatChange}>
              Next Category
            </button>
          </div>
        </div>
        <div className="right">
          <div className="news-box">
            <div className="news-category">{scraped.category}</div>
            <div className="news-title">
              <h2>{scraped.title}</h2>
            </div>
            <div className="news-date">{scraped.date}</div>
            <div className="news-desc">
              <p>{scraped.summary}</p>
            </div>
            <div className="news-link">
              <SourceButton link={scraped.link} />
            </div>
          </div>
          <div className="bottom-arrow-box">
            <button className="cv-btn" onClick={nextNews}>
              Previous News
            </button>
            <button className="cv-btn" onClick={nextNews}>
              Next News
            </button>
          </div>
        </div>
      </div>
    </>
  );
};

export default ScrapedNepali;
