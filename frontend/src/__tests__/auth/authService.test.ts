import authService from '../../services/authService';
import { AuthResponse, LoginFormData, RegisterFormData } from '../../types/auth';
import api from '../../services/api';

// apiをモック化
jest.mock('../../services/api', () => ({
  post: jest.fn().mockImplementation(() => Promise.resolve({ data: {} })),
}));

// ローカルストレージのモック
const localStorageMock = {
  getItem: jest.fn(),
  setItem: jest.fn(),
  removeItem: jest.fn(),
  clear: jest.fn(),
};

Object.defineProperty(window, 'localStorage', { value: localStorageMock });

describe('authService', () => {
  // 各テスト前にモックをリセット
  beforeEach(() => {
    jest.clearAllMocks();
    localStorageMock.clear();
  });

  // APIのモックレスポンス
  const mockAuthResponse: AuthResponse = {
    access_token: 'test-token',
    token_type: 'bearer',
    user: {
      id: 1,
      email: 'test@example.com',
      created_at: '2025-04-29T12:00:00',
    },
  };

  // apiのpostメソッドをモック化するヘルパー関数
  const mockApiPost = (data: any) => {
    (api.post as jest.Mock).mockResolvedValueOnce({ data });
    return api.post;
  };

  describe('register', () => {
    it('should register a user successfully', async () => {
      // Arrange
      const registerData: RegisterFormData = {
        email: 'test@example.com',
        password: 'password123',
        confirmPassword: 'password123',
      };
      
      const postMock = mockApiPost(mockAuthResponse);
      
      // Act
      const result = await authService.register(registerData);
      
      // Assert
      expect(postMock).toHaveBeenCalledWith('/api/auth/register', {
        email: 'test@example.com',
        password: 'password123',
      });
      expect(result).toEqual(mockAuthResponse);
    });
  });

  describe('login', () => {
    it('should login a user successfully and store token and user in localStorage', async () => {
      // Arrange
      const loginData: LoginFormData = {
        email: 'test@example.com',
        password: 'password123',
      };
      
      const postMock = mockApiPost(mockAuthResponse);
      
      // Act
      const result = await authService.login(loginData);
      
      // Assert
      expect(postMock).toHaveBeenCalledWith('/api/auth/login', loginData);
      expect(result).toEqual(mockAuthResponse);
      expect(localStorageMock.setItem).toHaveBeenCalledWith('token', 'test-token');
      expect(localStorageMock.setItem).toHaveBeenCalledWith('user', JSON.stringify(mockAuthResponse.user));
    });
  });

  describe('logout', () => {
    it('should remove token and user from localStorage', () => {
      // Arrange
      localStorageMock.setItem('token', 'test-token');
      localStorageMock.setItem('user', JSON.stringify(mockAuthResponse.user));
      
      // Act
      authService.logout();
      
      // Assert
      expect(localStorageMock.removeItem).toHaveBeenCalledWith('token');
      expect(localStorageMock.removeItem).toHaveBeenCalledWith('user');
    });
  });

  describe('getCurrentUser', () => {
    it('should return user from localStorage if exists', () => {
      // Arrange
      localStorageMock.getItem.mockReturnValueOnce(JSON.stringify(mockAuthResponse.user));
      
      // Act
      const result = authService.getCurrentUser();
      
      // Assert
      expect(result).toEqual(mockAuthResponse.user);
      expect(localStorageMock.getItem).toHaveBeenCalledWith('user');
    });

    it('should return null if user does not exist in localStorage', () => {
      // Act
      const result = authService.getCurrentUser();
      
      // Assert
      expect(result).toBeNull();
      expect(localStorageMock.getItem).toHaveBeenCalledWith('user');
    });
  });

  describe('getToken', () => {
    it('should return token from localStorage if exists', () => {
      // Arrange
      localStorageMock.getItem.mockReturnValueOnce('test-token');
      
      // Act
      const result = authService.getToken();
      
      // Assert
      expect(result).toBe('test-token');
      expect(localStorageMock.getItem).toHaveBeenCalledWith('token');
    });

    it('should return null if token does not exist in localStorage', () => {
      // Arrange
      localStorageMock.getItem.mockReturnValueOnce(null);
      
      // Act
      const result = authService.getToken();
      
      // Assert
      expect(result).toBeNull();
      expect(localStorageMock.getItem).toHaveBeenCalledWith('token');
    });
  });

  describe('isAuthenticated', () => {
    it('should return true if token exists in localStorage', () => {
      // Arrange
      localStorageMock.getItem.mockReturnValueOnce('test-token');
      
      // Act
      const result = authService.isAuthenticated();
      
      // Assert
      expect(result).toBe(true);
      expect(localStorageMock.getItem).toHaveBeenCalledWith('token');
    });

    it('should return false if token does not exist in localStorage', () => {
      // Arrange
      localStorageMock.getItem.mockReturnValueOnce(null);
      
      // Act
      const result = authService.isAuthenticated();
      
      // Assert
      expect(result).toBe(false);
      expect(localStorageMock.getItem).toHaveBeenCalledWith('token');
    });
  });
});
