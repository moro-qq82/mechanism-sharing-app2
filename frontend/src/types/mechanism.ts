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
  views_count?: number;  // 閲覧回数（オプション）
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

// メカニズム閲覧回数の型
export interface MechanismViewCount {
  mechanism_id: number;
  total_views: number;
  user_views?: number;
}

// 複数メカニズムの閲覧回数レスポンスの型
export interface MechanismViewsResponse {
  items: MechanismViewCount[];
}
