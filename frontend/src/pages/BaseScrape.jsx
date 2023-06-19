import React, { useState } from "react";
import "./Scraper.css";

import { MdOutlineKeyboardArrowLeft } from "react-icons/md";
import { useNavigate } from "react-router-dom";

import Switch from "@mui/joy/Switch";
import ScrapeEnglish from "./ScrapeEnglish";
import ScrapeNepali from "./ScrapeNepali";

import wall from "../images/wall.png";

const ScrapedEnglish = () => {
  const [dark, setDark] = useState(false);
  const navigate = useNavigate();

  const handleClick = () => {
    navigate(-1);
  };

  return (
    <>
      <div className="scraper-wrapper">
        <div className={`back ${!dark ? "eng-wall" : "nep-wall"}`}></div>
        <div className="top">
          <div className="top__back">
            <MdOutlineKeyboardArrowLeft
              className="arrows"
              onClick={handleClick}
            />
          </div>
          <div className="top__title">
            <h2>{!dark ? "English" : "Nepali"} News</h2>
          </div>
          <div className="top__alter">
            <Switch
              variant="outlined"
              color={dark ? "danger" : "primary"}
              slotProps={{ input: { "aria-label": "dark mode" } }}
              startDecorator={"English"}
              endDecorator={"Nepali"}
              checked={dark}
              onChange={(event) => setDark(event.target.checked)}
            />
          </div>
        </div>
        {/* <div className="mid">
          <div className="mid__left">
            <div className="mid__left__top">
              <HiArrowLongUp className="arrows" onClick={handleClick} />
            </div>
            <div className="mid__left__mid">
              <h3>Category</h3>
            </div>
            <div className="mid__left__bottom">
              <HiArrowLongDown className="arrows" onClick={handleClick} />
            </div>
          </div>
          <div className="mid__right">
            <div className="mid__right__box">
              <div className="news-category">Category</div>
              <div className="news-title">
                <h2>Title</h2>
              </div>
              <div className="news-date">Date</div>
              <div className="news-desc">
                Lorem ipsum dolor, sit amet consectetur adipisicing elit.
                Tenetur reprehenderit illum necessitatibus, debitis numquam
                cumque ab quia magnam doloribus dolorem cupiditate aspernatur
                aperiam ea, dicta quasi unde dolorum blanditiis? Temporibus
                fugiat in debitis aut accusamus dolorem excepturi voluptas iusto
                voluptatem? Voluptatem vitae tempore iste repellat consequuntur
                ducimus laborum nobis quasi sed itaque? Animi voluptate
                reiciendis omnis? Atque provident ipsum iste. Lorem ipsum dolor
                sit amet consectetur adipisicing elit. Optio alias asperiores,
                amet, cumque tenetur ullam rerum porro repellat facere, labore
                ipsam fuga itaque. Dolor alias amet obcaecati repudiandae aut
                laudantium commodi ea quis? Fugiat consectetur tenetur
                cupiditate provident inventore soluta commodi, distinctio
                repellat numquam laborum magnam incidunt eaque! Aperiam qui
                tenetur deleniti nobis iusto harum sint voluptas doloribus
                aliquid. Commodi tenetur accusantium sit porro corporis saepe
                asperiores error. Veritatis esse necessitatibus accusantium est
                assumenda, ratione voluptatibus officiis voluptas eveniet earum
                numquam tempore similique ipsam nihil eaque, eum, fugit totam
                porro? Lorem ipsum dolor sit amet consectetur adipisicing elit.
                Nesciunt, reiciendis a tempora blanditiis eos similique
                asperiores praesentium nulla magnam minus necessitatibus et
                assumenda velit commodi culpa itaque quidem aliquam. Vitae
                quaerat atque porro nesciunt ad ex, vero et commodi voluptate
                officia maiores cum quod molestiae aliquam, aspernatur quia,
                expedita ducimus! Dolore neque nostrum provident at incidunt
                nulla tempore quam quod voluptatem quasi cupiditate totam saepe
                aliquam officiis aperiam natus, explicabo adipisci possimus
                magni obcaecati asperiores? Facilis facere odio nisi omnis
                culpa, delectus, voluptatem magnam expedita cum minus dolorem ut
                possimus illum! Quos ab cumque numquam.
              </div>
              <div className="news-source">Source</div>
            </div>
            <div className="bottom">
              <div className="bottom__left">
                <HiArrowLongLeft className="arrows" onClick={handleClick} />
              </div>
              <div className="bottom__mid">
                <h3>News</h3>
              </div>
              <div className="bottom__right">
                <HiArrowLongRight className="arrows" onClick={handleClick} />
              </div>
            </div>
          </div>
        </div> */}
        {!dark ? <ScrapeEnglish /> : <ScrapeNepali />}
      </div>
    </>
  );
};

export default ScrapedEnglish;
