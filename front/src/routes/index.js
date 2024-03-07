import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import WelcomePage from '../components/WelcomePage';
import JokesCardSwiper from '../components/JokesCardSwiper.js';
import JokometianView from '../components/JokometianView';
import Instructions from '../components/Instructions';
import Root from '../components/Root';

const AppRoutes = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Root />}  >
          {/* Nested routes */}
          <Route index path="/" element={<WelcomePage />} />
          <Route path="/welcome" element={<WelcomePage/>} />
          <Route path="/swipe" element={<JokesCardSwiper/>} />
          <Route path="/instructions" element={<Instructions/>} />
          <Route path="/jokometian/:id" element={<JokometianView/>} />
        </Route>
      </Routes>
    </Router>
  );
};

export default AppRoutes;
