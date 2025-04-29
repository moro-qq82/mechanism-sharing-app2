import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { useNavigate } from 'react-router-dom';
import { AuthState, LoginFormData, RegisterFormData, User } from '../types/auth';
import authService from '../services/authService';

// 初期認証状態
const initialAuthState: AuthState = {
  isAuthenticated: false,
  user: null,
  token: null,
  loading: true,
  error: null,
};

// コンテキストの型定義
interface AuthContextType extends AuthState {
  login: (credentials: LoginFormData) => Promise<void>;
  register: (userData: RegisterFormData) => Promise<void>;
  logout: () => void;
}

// AuthContextの作成
const AuthContext = createContext<AuthContextType | undefined>(undefined);

// AuthProviderの型定義
interface AuthProviderProps {
  children: ReactNode;
}

// AuthProviderコンポーネント
export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [authState, setAuthState] = useState<AuthState>(initialAuthState);
  const navigate = useNavigate();

  // 初期化時に認証状態を確認
  useEffect(() => {
    const initAuth = () => {
      try {
        const token = authService.getToken();
        const user = authService.getCurrentUser();

        if (token && user) {
          setAuthState({
            isAuthenticated: true,
            user,
            token,
            loading: false,
            error: null,
          });
        } else {
          setAuthState({
            ...initialAuthState,
            loading: false,
          });
        }
      } catch (error) {
        setAuthState({
          ...initialAuthState,
          loading: false,
          error: '認証状態の初期化に失敗しました',
        });
      }
    };

    initAuth();
  }, []);

  // ログイン処理
  const login = async (credentials: LoginFormData) => {
    try {
      setAuthState({
        ...authState,
        loading: true,
        error: null,
      });

      const response = await authService.login(credentials);
      
      setAuthState({
        isAuthenticated: true,
        user: response.user,
        token: response.access_token,
        loading: false,
        error: null,
      });

      navigate('/');
    } catch (error) {
      setAuthState({
        ...authState,
        loading: false,
        error: 'ログインに失敗しました。メールアドレスとパスワードを確認してください。',
      });
    }
  };

  // 登録処理
  const register = async (userData: RegisterFormData) => {
    try {
      setAuthState({
        ...authState,
        loading: true,
        error: null,
      });

      // パスワード確認
      if (userData.password !== userData.confirmPassword) {
        setAuthState({
          ...authState,
          loading: false,
          error: 'パスワードが一致しません',
        });
        return;
      }

      await authService.register(userData);
      
      // 登録後、自動的にログイン
      await login({
        email: userData.email,
        password: userData.password,
      });
    } catch (error) {
      setAuthState({
        ...authState,
        loading: false,
        error: '登録に失敗しました。別のメールアドレスを試してください。',
      });
    }
  };

  // ログアウト処理
  const logout = () => {
    authService.logout();
    setAuthState({
      ...initialAuthState,
      loading: false,
    });
    navigate('/login');
  };

  // コンテキスト値
  const contextValue: AuthContextType = {
    ...authState,
    login,
    register,
    logout,
  };

  return (
    <AuthContext.Provider value={contextValue}>
      {children}
    </AuthContext.Provider>
  );
};

// カスタムフック
export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
