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

ReactDOM.render(
  <React.StrictMode>
    <Router>
      <Routes>
        <Route exact path="/" element={<Programs />} />
        <Route exact path="overview" element={<Overview />} />
        <Route exact path="workshop" element={<Workshop />} />
        <Route exact path="rental-assistance" element={<RentalAssistance />} />
        <Route exact path="scholarship" element={<Scholarship />} />
        <Route exact path="home-delivery" element={<HomeDelivery />} />
        <Route exact path="drive-thru" element={<DriveThru />} />
        <Route exact path="onboarding" element={<Onboarding />} />
        <Route exact path="educational-activity" element={<EducationalActivity />} />
      </Routes>
    </Router>
  </React.StrictMode>
  ,
  document.getElementById('root')
);


const chartTypes = {
  "active-users": ("line", "data"),
  "age-groups": ("bar", "data"),
  "client-frequency": ("bar", "data"),
  "most-popular-categories": ("bar", "data")
}

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
