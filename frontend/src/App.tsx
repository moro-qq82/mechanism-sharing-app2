import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';

// ページコンポーネントのインポート
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import MechanismListPage from './pages/MechanismListPage';
import MechanismDetailPage from './pages/MechanismDetailPage';
import MechanismNewPage from './pages/MechanismNewPage';

// 認証関連のコンポーネントのインポート
import { AuthProvider } from './contexts/AuthContext';
import ProtectedRoute from './components/auth/ProtectedRoute';
import Layout from './components/layout/Layout';

function App() {
  return (
    <Router>
      <AuthProvider>
        <Routes>
          {/* 認証不要のルート */}
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          
          {/* 認証が必要なルート */}
          <Route element={<ProtectedRoute />}>
            <Route 
              path="/" 
              element={
                <Layout>
                  <MechanismListPage />
                </Layout>
              } 
            />
            <Route 
              path="/mechanisms/:id" 
              element={
                <Layout>
                  <MechanismDetailPage />
                </Layout>
              } 
            />
            <Route 
              path="/mechanisms/new" 
              element={
                <Layout>
                  <MechanismNewPage />
                </Layout>
              } 
            />
          </Route>
        </Routes>
      </AuthProvider>
    </Router>
  );
}

export default App;
