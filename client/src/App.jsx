import React from "react";
import { BrowserRouter, Routes, Route, useLocation } from "react-router-dom";

import PDF from "./pdf";
import NavBar from "./navbar";
import YouTube from "./youtube";
import ChatBot from "./chatbot";


const App = () => {
  const location = useLocation();

  const noNavBarPaths = [];



  return (
    <div className="container">
      {!noNavBarPaths.includes(location.pathname) && <NavBar />}
      <Routes>
        <Route exact path="/" element={<PDF />} />
        <Route exact path="/youtube" element={<YouTube />} />
        <Route exact path="/chatbot" element={<ChatBot />} />
      </Routes>
    </div>
  );
};

// eslint-disable-next-line react-refresh/only-export-components
export default () => (
  <BrowserRouter>
    <App />
  </BrowserRouter>
);