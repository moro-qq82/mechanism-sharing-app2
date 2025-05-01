// メカニズム関連の型定義

import { User } from './auth';

// メカニズム基本情報の型
export interface Mechanism {
  id: number;
  title: string;
  description: string;
  reliability: number;
  thumbnail_path: string | null;
  user: User;
  categories: string[];
  likes_count: number;
  created_at: string;
}

// メカニズム詳細情報の型（基本情報を拡張）
export interface MechanismDetail extends Mechanism {
  file_path: string;
  updated_at: string;
}

// メカニズム一覧レスポンスの型
export interface PaginatedMechanismResponse {
  items: Mechanism[];
  total: number;
  page: number;
  limit: number;
  pages: number;
}

// メカニズム作成フォームの型
export interface MechanismFormData {
  title: string;
  description: string;
  reliability: number;
  categories: string;
  file: File | null;
  thumbnail: File | null;
}
