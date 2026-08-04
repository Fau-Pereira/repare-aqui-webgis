import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Mapa from './pages/Mapa';
import Dashboard from './pages/Dashboard';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/login" replace />} />
        <Route path="/login" element={<Login />} />
        <Route path="/mapa" element={<Mapa />} />
        <Route path="/painel" element={<Dashboard />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;