import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";

import "./index.css";

import Footer from "./components/Footer";
import Navbar from "./components/Navbar";
import HomeScreen from "./screens/Home";
import TodoScreen from "./screens/TodoScreen";
import FeaturesScreen from "./screens/FeaturesScreen";
import Login from "./screens/Login";
import AboutScreen from "./screens/AboutScreen";

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<HomeScreen />} exact />
        <Route path="/login" element={<Login />} />
        <Route path="/todo" element={<TodoScreen />} />
        <Route path="/features" element={<FeaturesScreen />} />
        <Route path="/about" element={<AboutScreen />} />
      </Routes>
      <Footer />
    </Router>
  );
}

export default App;
