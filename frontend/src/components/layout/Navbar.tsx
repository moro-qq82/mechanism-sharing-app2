import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { Button } from '../ui/button';
import { ParticleBackground } from '../ui/particle-background';
import { cn } from '../../lib/utils';

const Navbar: React.FC = () => {
  const { isAuthenticated, user, logout } = useAuth();
  const navigate = useNavigate();
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  return (
    <nav className="relative bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-600 shadow-lg overflow-hidden">
      <ParticleBackground className="opacity-70" />
      
      <div className="relative z-20 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* ロゴ・ブランド */}
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <Link 
                to="/" 
                className="text-white font-bold text-xl hover:text-blue-200 transition-colors duration-200"
              >
                🔧 メカニズム共有アプリ
              </Link>
            </div>
            
            {/* デスクトップナビゲーション */}
            <div className="hidden md:block ml-10">
              <div className="flex items-baseline space-x-4">
                <Link
                  to="/"
                  className="text-white hover:text-blue-200 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200"
                >
                  ホーム
                </Link>
                {isAuthenticated && (
                  <Link
                    to="/mechanisms/new"
                    className="text-white hover:text-blue-200 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200"
                  >
                    新規投稿
                  </Link>
                )}
              </div>
            </div>
          </div>

          {/* デスクトップユーザーメニュー */}
          <div className="hidden md:block">
            <div className="ml-4 flex items-center md:ml-6">
              {isAuthenticated ? (
                <div className="flex items-center space-x-4">
                  <span className="text-white text-sm font-medium">
                    {user?.email}
                  </span>
                  <Button
                    onClick={handleLogout}
                    variant="outline"
                    size="sm"
                    className="text-white border-white/30 bg-transparent hover:bg-white/20 hover:text-white hover:border-white/50"
                  >
                    ログアウト
                  </Button>
                </div>
              ) : (
                <div className="flex space-x-3">
                  <Button
                    asChild
                    variant="ghost"
                    size="sm"
                    className="text-white hover:bg-white/10 hover:text-white"
                  >
                    <Link to="/login">ログイン</Link>
                  </Button>
                  <Button
                    asChild
                    variant="outline"
                    size="sm"
                    className="text-white border-white/30 bg-transparent hover:bg-white/20 hover:text-white hover:border-white/50"
                  >
                    <Link to="/register">登録</Link>
                  </Button>
                </div>
              )}
            </div>
          </div>

          {/* モバイルメニューボタン */}
          <div className="md:hidden">
            <Button
              onClick={toggleMenu}
              variant="ghost"
              size="icon"
              className="text-white hover:bg-white/10"
            >
              <span className="sr-only">メニューを開く</span>
              <svg
                className={cn("h-6 w-6 transition-transform duration-200", {
                  "rotate-90": isMenuOpen
                })}
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M4 6h16M4 12h16M4 18h16"
                />
              </svg>
            </Button>
          </div>
        </div>
      </div>

      {/* モバイルメニュー */}
      <div className={cn(
        "md:hidden transition-all duration-300 ease-in-out overflow-hidden",
        {
          "max-h-96 opacity-100": isMenuOpen,
          "max-h-0 opacity-0": !isMenuOpen
        }
      )}>
        <div className="relative z-20 bg-black/20 backdrop-blur-sm">
          <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
            <Link
              to="/"
              className="text-white hover:bg-white/10 block px-3 py-2 rounded-md text-base font-medium transition-colors duration-200"
              onClick={() => setIsMenuOpen(false)}
            >
              ホーム
            </Link>
            {isAuthenticated && (
              <Link
                to="/mechanisms/new"
                className="text-white hover:bg-white/10 block px-3 py-2 rounded-md text-base font-medium transition-colors duration-200"
                onClick={() => setIsMenuOpen(false)}
              >
                新規投稿
              </Link>
            )}
          </div>
          
          <div className="pt-4 pb-3 border-t border-white/20">
            {isAuthenticated ? (
              <div className="px-5">
                <div className="flex items-center mb-3">
                  <div className="h-10 w-10 rounded-full bg-white/20 flex items-center justify-center">
                    <span className="text-white font-bold text-lg">
                      {user?.email.charAt(0).toUpperCase()}
                    </span>
                  </div>
                  <div className="ml-3">
                    <div className="text-base font-medium text-white">
                      {user?.email}
                    </div>
                  </div>
                </div>
                <Button
                  onClick={() => {
                    handleLogout();
                    setIsMenuOpen(false);
                  }}
                  variant="outline"
                  size="sm"
                  className="w-full text-white border-white/30 bg-transparent hover:bg-white/20 hover:text-white hover:border-white/50"
                >
                  ログアウト
                </Button>
              </div>
            ) : (
              <div className="px-5 space-y-2">
                <Button
                  asChild
                  variant="ghost"
                  size="sm"
                  className="w-full text-white hover:bg-white/10 hover:text-white"
                >
                  <Link to="/login" onClick={() => setIsMenuOpen(false)}>
                    ログイン
                  </Link>
                </Button>
                <Button
                  asChild
                  variant="outline"
                  size="sm"
                  className="w-full text-white border-white/30 bg-transparent hover:bg-white/20 hover:text-white hover:border-white/50"
                >
                  <Link to="/register" onClick={() => setIsMenuOpen(false)}>
                    登録
                  </Link>
                </Button>
              </div>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
