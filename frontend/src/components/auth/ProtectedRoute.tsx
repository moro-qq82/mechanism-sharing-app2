import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';

interface ProtectedRouteProps {
  redirectPath?: string;
}

/**
 * 認証が必要なルートを保護するコンポーネント
 * 認証されていない場合は指定されたパスにリダイレクトする
 */
const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ 
  redirectPath = '/login'
}) => {
  const { isAuthenticated, loading } = useAuth();

  // 認証状態の読み込み中は何も表示しない
  if (loading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div data-testid="loading-spinner" className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
      </div>
    );
  }

  // 認証されていない場合はリダイレクト
  if (!isAuthenticated) {
    return <Navigate to={redirectPath} replace />;
  }

  // 認証されている場合は子コンポーネントを表示
  return <Outlet />;
};

export default ProtectedRoute;
