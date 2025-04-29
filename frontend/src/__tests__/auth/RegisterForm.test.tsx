import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import RegisterForm from '../../components/auth/RegisterForm';
import { useAuth } from '../../contexts/AuthContext';

// useAuthをモック化
jest.mock('../../contexts/AuthContext', () => ({
  useAuth: jest.fn(),
}));

describe('RegisterForm', () => {
  // モックの登録関数
  const mockRegister = jest.fn();
  
  // 各テスト前にモックをリセット
  beforeEach(() => {
    jest.clearAllMocks();
    
    // useAuthのモック実装
    (useAuth as jest.Mock).mockReturnValue({
      register: mockRegister,
      error: null,
      loading: false,
    });
  });

  it('should render register form correctly', () => {
    // Arrange & Act
    render(
      <BrowserRouter>
        <RegisterForm />
      </BrowserRouter>
    );
    
    // Assert
    expect(screen.getByPlaceholderText('メールアドレス')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('パスワード')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('パスワード（確認）')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /登録/i })).toBeInTheDocument();
  });

  it('should update form values on input change', () => {
    // Arrange
    render(
      <BrowserRouter>
        <RegisterForm />
      </BrowserRouter>
    );
    
    const emailInput = screen.getByPlaceholderText('メールアドレス');
    const passwordInput = screen.getByPlaceholderText('パスワード');
    const confirmPasswordInput = screen.getByPlaceholderText('パスワード（確認）');
    
    // Act
    fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
    fireEvent.change(passwordInput, { target: { value: 'password123' } });
    fireEvent.change(confirmPasswordInput, { target: { value: 'password123' } });
    
    // Assert
    expect(emailInput).toHaveValue('test@example.com');
    expect(passwordInput).toHaveValue('password123');
    expect(confirmPasswordInput).toHaveValue('password123');
  });

  it('should show error when passwords do not match', () => {
    // Arrange
    render(
      <BrowserRouter>
        <RegisterForm />
      </BrowserRouter>
    );
    
    const emailInput = screen.getByPlaceholderText('メールアドレス');
    const passwordInput = screen.getByPlaceholderText('パスワード');
    const confirmPasswordInput = screen.getByPlaceholderText('パスワード（確認）');
    const submitButton = screen.getByRole('button', { name: /登録/i });
    
    // Act
    fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
    fireEvent.change(passwordInput, { target: { value: 'password123' } });
    fireEvent.change(confirmPasswordInput, { target: { value: 'password456' } });
    fireEvent.click(submitButton);
    
    // Assert
    expect(screen.getByText('パスワードが一致しません')).toBeInTheDocument();
    expect(mockRegister).not.toHaveBeenCalled();
  });

  it('should show error when password is too short', () => {
    // Arrange
    render(
      <BrowserRouter>
        <RegisterForm />
      </BrowserRouter>
    );
    
    const emailInput = screen.getByPlaceholderText('メールアドレス');
    const passwordInput = screen.getByPlaceholderText('パスワード');
    const confirmPasswordInput = screen.getByPlaceholderText('パスワード（確認）');
    const submitButton = screen.getByRole('button', { name: /登録/i });
    
    // Act
    fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
    fireEvent.change(passwordInput, { target: { value: 'pass' } });
    fireEvent.change(confirmPasswordInput, { target: { value: 'pass' } });
    fireEvent.click(submitButton);
    
    // Assert
    expect(screen.getByText('パスワードは8文字以上である必要があります')).toBeInTheDocument();
    expect(mockRegister).not.toHaveBeenCalled();
  });

  it('should call register function with form data on submit when validation passes', async () => {
    // Arrange
    render(
      <BrowserRouter>
        <RegisterForm />
      </BrowserRouter>
    );
    
    const emailInput = screen.getByPlaceholderText('メールアドレス');
    const passwordInput = screen.getByPlaceholderText('パスワード');
    const confirmPasswordInput = screen.getByPlaceholderText('パスワード（確認）');
    const submitButton = screen.getByRole('button', { name: /登録/i });
    
    // Act
    fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
    fireEvent.change(passwordInput, { target: { value: 'password123' } });
    fireEvent.change(confirmPasswordInput, { target: { value: 'password123' } });
    fireEvent.click(submitButton);
    
    // Assert
    await waitFor(() => {
      expect(mockRegister).toHaveBeenCalledWith({
        email: 'test@example.com',
        password: 'password123',
        confirmPassword: 'password123',
      });
    });
  });

  it('should display loading state when loading is true', () => {
    // Arrange
    (useAuth as jest.Mock).mockReturnValue({
      register: mockRegister,
      error: null,
      loading: true,
    });
    
    // Act
    render(
      <BrowserRouter>
        <RegisterForm />
      </BrowserRouter>
    );
    
    // Assert
    const submitButton = screen.getByRole('button', { name: /登録中/i });
    expect(submitButton).toBeDisabled();
    expect(submitButton).toHaveTextContent('登録中...');
  });

  it('should display error message when error exists', () => {
    // Arrange
    const errorMessage = '登録に失敗しました';
    (useAuth as jest.Mock).mockReturnValue({
      register: mockRegister,
      error: errorMessage,
      loading: false,
    });
    
    // Act
    render(
      <BrowserRouter>
        <RegisterForm />
      </BrowserRouter>
    );
    
    // Assert
    expect(screen.getByText(errorMessage)).toBeInTheDocument();
  });
});
