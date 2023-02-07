import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import ClassifyScreen from "./pages/ClassifyScreen";

import HomeScreen from "./pages/HomeScreen";
import StartScreen from "./pages/StartScreen";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomeScreen />} exact />
        <Route path="/start" element={<StartScreen />} />
        <Route path="/classify" element={<ClassifyScreen />} />
      </Routes>
    </Router>
  );
}

export default App;
