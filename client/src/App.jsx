import React from "react";
import { BrowserRouter, Routes, Route, useLocation } from "react-router-dom";

import PDF from "./pages/pdf";
import NavBar from "./components/navbar";
import YouTube from "./pages/youtube";
import ChatBot from "./pages/chatbot";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Home from "./pages/home";


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
        <Route exact path="/login" element={<Login />} />
        <Route exact path="/signup" element={<Register />} />
        <Route exact path="/home" element={<Home/> } />
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