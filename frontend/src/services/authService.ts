import api from './api';
import { AuthResponse, LoginFormData, RegisterFormData } from '../types/auth';

/**
 * 認証関連のAPIサービス
 */
const authService = {
  /**
   * ユーザー登録
   * @param userData 登録するユーザー情報
   * @returns 登録結果
   */
  register: async (userData: RegisterFormData) => {
    const { confirmPassword, ...registerData } = userData;
    const response = await api.post<AuthResponse>('/api/auth/register', registerData);
    return response.data;
  },

  /**
   * ログイン
   * @param credentials ログイン情報
   * @returns ログイン結果
   */
  login: async (credentials: LoginFormData) => {
    const response = await api.post<AuthResponse>('/api/auth/login', credentials);
    
    // トークンとユーザー情報をローカルストレージに保存
    if (response.data.access_token) {
      localStorage.setItem('token', response.data.access_token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
    }
    
    return response.data;
  },

  /**
   * ログアウト
   */
  logout: () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  },

  /**
   * 現在のユーザー情報を取得
   * @returns ユーザー情報
   */
  getCurrentUser: () => {
    const userStr = localStorage.getItem('user');
    if (userStr) {
      return JSON.parse(userStr);
    }
    return null;
  },

  /**
   * 認証トークンを取得
   * @returns 認証トークン
   */
  getToken: () => {
    return localStorage.getItem('token');
  },

  /**
   * ユーザーが認証済みかどうかを確認
   * @returns 認証済みかどうか
   */
  isAuthenticated: () => {
    return !!localStorage.getItem('token');
  }
};

export default authService;
