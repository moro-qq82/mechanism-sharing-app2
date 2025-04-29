import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import LoginForm from '../../components/auth/LoginForm';
import { useAuth } from '../../contexts/AuthContext';

// useAuthをモック化
jest.mock('../../contexts/AuthContext', () => ({
  useAuth: jest.fn(),
}));

describe('LoginForm', () => {
  // モックのログイン関数
  const mockLogin = jest.fn();
  
  // 各テスト前にモックをリセット
  beforeEach(() => {
    jest.clearAllMocks();
    
    // useAuthのモック実装
    (useAuth as jest.Mock).mockReturnValue({
      login: mockLogin,
      error: null,
      loading: false,
    });
  });

  it('should render login form correctly', () => {
    // Arrange & Act
    render(
      <BrowserRouter>
        <LoginForm />
      </BrowserRouter>
    );
    
    // Assert
    expect(screen.getByPlaceholderText('メールアドレス')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('パスワード')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /ログイン/i })).toBeInTheDocument();
  });

  it('should update form values on input change', () => {
    // Arrange
    render(
      <BrowserRouter>
        <LoginForm />
      </BrowserRouter>
    );
    
    const emailInput = screen.getByPlaceholderText('メールアドレス');
    const passwordInput = screen.getByPlaceholderText('パスワード');
    
    // Act
    fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
    fireEvent.change(passwordInput, { target: { value: 'password123' } });
    
    // Assert
    expect(emailInput).toHaveValue('test@example.com');
    expect(passwordInput).toHaveValue('password123');
  });

  it('should call login function with form data on submit', async () => {
    // Arrange
    render(
      <BrowserRouter>
        <LoginForm />
      </BrowserRouter>
    );
    
    const emailInput = screen.getByPlaceholderText('メールアドレス');
    const passwordInput = screen.getByPlaceholderText('パスワード');
    const submitButton = screen.getByRole('button', { name: /ログイン/i });
    
    // Act
    fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
    fireEvent.change(passwordInput, { target: { value: 'password123' } });
    fireEvent.click(submitButton);
    
    // Assert
    await waitFor(() => {
      expect(mockLogin).toHaveBeenCalledWith({
        email: 'test@example.com',
        password: 'password123',
      });
    });
  });

  it('should display loading state when loading is true', () => {
    // Arrange
    (useAuth as jest.Mock).mockReturnValue({
      login: mockLogin,
      error: null,
      loading: true,
    });
    
    // Act
    render(
      <BrowserRouter>
        <LoginForm />
      </BrowserRouter>
    );
    
    // Assert
    const submitButton = screen.getByRole('button', { name: /ログイン中/i });
    expect(submitButton).toBeDisabled();
    expect(submitButton).toHaveTextContent('ログイン中...');
  });

  it('should display error message when error exists', () => {
    // Arrange
    const errorMessage = 'ログインに失敗しました';
    (useAuth as jest.Mock).mockReturnValue({
      login: mockLogin,
      error: errorMessage,
      loading: false,
    });
    
    // Act
    render(
      <BrowserRouter>
        <LoginForm />
      </BrowserRouter>
    );
    
    // Assert
    expect(screen.getByText(errorMessage)).toBeInTheDocument();
  });
});
