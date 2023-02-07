import React, { useState } from "react";
import logo from "../images/Logoer.png";

const Navbar = () => {
  const [nav, setNav] = useState(false);
  const [clickNav, setClickNav] = useState(0);

  const changeBackground = () => {
    if (window.scrollY >= 50) {
      setNav(true);
    } else {
      setNav(false);
    }

    // if (window.scrollY >= 200) {
    //   setClickNav(1);
    // } else if (window.scrollY >= 300) {
    //   setClickNav(2);
    // } else {
    //   setClickNav(0);
    // }
  };
  window.addEventListener("scroll", changeBackground);

  return (
    <nav className={nav ? `nav active` : `nav`}>
      <a href="/#" className="logo" onClick={() => setClickNav(0)}>
        <img src={logo} alt="" />
      </a>
      <input type="checkbox" className="menu-btn" id="menu-btn" />
      <label className="menu-icon" htmlFor="menu-btn">
        <span className="nav-icon"></span>
      </label>
      <ul className="menu">
        <li>
          <a
            href="/#"
            className={clickNav === 0 ? `active` : ``}
            onClick={() => {
              setClickNav(0);
            }}
          >
            Home
          </a>
        </li>
        <li>
          <a
            href="#features"
            className={clickNav === 1 ? `active` : ``}
            onClick={() => setClickNav(1)}
          >
            Features
          </a>
        </li>
        <li>
          <a
            href="#about"
            className={clickNav === 2 ? `active` : ``}
            onClick={() => setClickNav(2)}
          >
            About
          </a>
        </li>
        <li>
          <a
            href="/start"
            className={clickNav === 3 ? `active` : ``}
            onClick={() => setClickNav(3)}
          >
            Get Started
          </a>
        </li>
        {/* <li>
          <a href="/">Download</a>
        </li> */}
      </ul>
    </nav>
  );
};

export default Navbar;
