// 認証関連の型定義

// ユーザー情報の型
export interface User {
  id: number;
  email: string;
  is_admin: boolean;
  created_at: string;
}

// 認証状態の型
export interface AuthState {
  isAuthenticated: boolean;
  user: User | null;
  token: string | null;
  loading: boolean;
  error: string | null;
}

// ログインフォームの型
export interface LoginFormData {
  email: string;
  password: string;
}

// 登録フォームの型
export interface RegisterFormData {
  email: string;
  password: string;
  confirmPassword: string;
}

// APIレスポンスの型
export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}
