import React, { ReactNode } from 'react';
import Navbar from './Navbar';

interface LayoutProps {
  children: ReactNode;
}

/**
 * アプリケーションの共通レイアウトコンポーネント
 * ナビゲーションバーとコンテンツエリアを含む
 */
const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div className="flex flex-col min-h-screen">
      <Navbar />
      <main className="flex-grow container mx-auto px-4 py-8">
        {children}
      </main>
      <footer className="bg-gray-100 py-4">
        <div className="container mx-auto px-4 text-center text-gray-600">
          <p>© 2025 メカニズム共有アプリ</p>
        </div>
      </footer>
    </div>
  );
};

export default Layout;
