import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';

// ページコンポーネントのインポート
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import MechanismListPage from './pages/MechanismListPage';
import MechanismDetailPage from './pages/MechanismDetailPage';
import MechanismNewPage from './pages/MechanismNewPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/" element={<MechanismListPage />} />
        <Route path="/mechanisms/:id" element={<MechanismDetailPage />} />
        <Route path="/mechanisms/new" element={<MechanismNewPage />} />
      </Routes>
    </Router>
  );
}

export default App;
