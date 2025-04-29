import React from 'react';
import { render, screen } from '@testing-library/react';
import { MemoryRouter, Routes, Route } from 'react-router-dom';
import ProtectedRoute from '../../components/auth/ProtectedRoute';
import { useAuth } from '../../contexts/AuthContext';

// useAuthをモック化
jest.mock('../../contexts/AuthContext', () => ({
  useAuth: jest.fn(),
}));

// テスト用のコンポーネント
const TestComponent = () => <div>Protected Content</div>;

// テスト用のルーティング設定
const TestRoutes = () => (
  <MemoryRouter initialEntries={['/']}>
    <Routes>
      <Route element={<ProtectedRoute />}>
        <Route path="/" element={<TestComponent />} />
      </Route>
      <Route path="/login" element={<div>Login Page</div>} />
    </Routes>
  </MemoryRouter>
);

describe('ProtectedRoute', () => {
  // 各テスト前にモックをリセット
  beforeEach(() => {
    jest.clearAllMocks();
    
    // window.locationのモック
    Object.defineProperty(window, 'location', {
      writable: true,
      value: { href: '/' },
    });
  });

  it('should render loading spinner when loading is true', () => {
    // Arrange
    (useAuth as jest.Mock).mockReturnValue({
      isAuthenticated: false,
      loading: true,
    });
    
    // Act
    render(<TestRoutes />);
    
    // Assert
    expect(screen.queryByText('Protected Content')).not.toBeInTheDocument();
    expect(screen.queryByText('Login Page')).not.toBeInTheDocument();
    
    // ローディングスピナーの要素を確認
    const spinner = screen.getByTestId('loading-spinner');
    expect(spinner).toBeInTheDocument();
  });

  it('should redirect to login page when user is not authenticated', () => {
    // Arrange
    (useAuth as jest.Mock).mockReturnValue({
      isAuthenticated: false,
      loading: false,
    });
    
    // Act
    render(<TestRoutes />);
    
    // Assert
    expect(screen.queryByText('Protected Content')).not.toBeInTheDocument();
    expect(screen.getByText('Login Page')).toBeInTheDocument();
  });

  it('should render protected content when user is authenticated', () => {
    // Arrange
    (useAuth as jest.Mock).mockReturnValue({
      isAuthenticated: true,
      loading: false,
    });
    
    // Act
    render(<TestRoutes />);
    
    // Assert
    expect(screen.getByText('Protected Content')).toBeInTheDocument();
    expect(screen.queryByText('Login Page')).not.toBeInTheDocument();
  });

  it('should redirect to custom path when redirectPath prop is provided', () => {
    // Arrange
    (useAuth as jest.Mock).mockReturnValue({
      isAuthenticated: false,
      loading: false,
    });
    
    // カスタムリダイレクトパスを持つテスト用のルーティング設定
    const CustomRedirectRoutes = () => (
      <MemoryRouter initialEntries={['/']}>
        <Routes>
          <Route element={<ProtectedRoute redirectPath="/custom-login" />}>
            <Route path="/" element={<TestComponent />} />
          </Route>
          <Route path="/custom-login" element={<div>Custom Login Page</div>} />
        </Routes>
      </MemoryRouter>
    );
    
    // Act
    render(<CustomRedirectRoutes />);
    
    // Assert
    expect(screen.queryByText('Protected Content')).not.toBeInTheDocument();
    expect(screen.getByText('Custom Login Page')).toBeInTheDocument();
  });
});
