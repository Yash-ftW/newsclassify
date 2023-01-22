import React, { useEffect, useState } from "react";
import { Offcanvas } from "react-bootstrap";
import { Link } from "react-router-dom";

function OffCanva() {
  const [show, setShow] = useState(false);
  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const onScroll = () => {
      if (window.scrollY > 50) {
        setScrolled(true);
      } else {
        setScrolled(false);
      }
    };
    window.addEventListener("scroll", onScroll);

    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  return (
    <>
      <button
        className={`off-btn ${scrolled ? "scrolled" : ""}`}
        onClick={handleShow}
      >
        <i className="fa-solid fa-bars"></i>
      </button>
      <Offcanvas show={show} onHide={handleClose}>
        <Offcanvas.Header closeButton>
          <Offcanvas.Title>
            <h1>Menu</h1>
          </Offcanvas.Title>
        </Offcanvas.Header>
        <Offcanvas.Body>
          <ul class="list-group">
            <Link to="/" className="link-no">
              <li class="list-group-item d-flex justify-content-between align-items-center">
                Graph
              </li>
            </Link>
            <Link to="/" className="link-no">
              <li class="list-group-item d-flex justify-content-between align-items-center">
                Schedule
              </li>
            </Link>
            <Link to="/" className="link-no">
              <li className="list-group-item d-flex justify-content-between align-items-center">
                Calendar
              </li>
            </Link>
            <Link to="/" className="link-no">
              <li class="list-group-item d-flex justify-content-between align-items-center">
                Recommendations
              </li>
            </Link>
            <Link to="/todo" className="link-no">
              <li class="list-group-item d-flex justify-content-between align-items-center">
                To-Do List
              </li>
            </Link>
          </ul>
        </Offcanvas.Body>
      </Offcanvas>
    </>
  );
}

export default OffCanva;
