import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import reportWebVitals from './reportWebVitals';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import {
  Programs,
  Workshop,
  RentalAssistance,
  Scholarship,
  HomeDelivery,
  DriveThru,
  Onboarding,
  EducationalActivity,
  Overview
} from "./pages"

const types = {
  "most-popular-categories": ("bar", "data"),
  "client-frequency": ("bar", "data"),
  "most-active-users": ("line", "data"),
  "age-groups": ("bar", "data"),
  "consistent-client-dropping-off": ("bar", "data") // table?
}

ReactDOM.render(
  <React.StrictMode>
    <Router>
      <Routes>
        <Route exact path="/" element={<Programs />} />
        <Route exact path="overview" element={<Overview chartTypes={types} />} />
        <Route exact path="workshop" element={<Workshop chartTypes={types} />} />
        <Route exact path="rental-assistance" element={<RentalAssistance chartTypes={types} />} />
        <Route exact path="scholarship" element={<Scholarship chartTypes={types} />} />
        <Route exact path="home-delivery" element={<HomeDelivery chartTypes={types} />} />
        <Route exact path="drive-thru" element={<DriveThru chartTypes={types} />} />
        <Route exact path="onboarding" element={<Onboarding chartTypes={types} />} />
        <Route exact path="educational-activity" element={<EducationalActivity chartTypes={types} />} />
      </Routes>
    </Router>
  </React.StrictMode>
  ,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
