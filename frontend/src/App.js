import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import ClassifyScreen from "./pages/ClassifyScreen";

import HomeScreen from "./pages/HomeScreen";
import ScrapeScreen from "./pages/ScrapeScreen";
import StartScreen from "./pages/StartScreen";
import SummarizeScreen from "./pages/SummarizeScreen";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomeScreen />} exact />
        <Route path="/start" element={<StartScreen />} />
        <Route path="/classify" element={<ClassifyScreen />} />
        <Route path="/summarize" element={<SummarizeScreen />} />
        <Route path="/scrape" element={<ScrapeScreen />} />
      </Routes>
    </Router>
  );
}

export default App;
