/**
 * ファイル関連のユーティリティ関数
 */

// APIのベースURL
const API_BASE_URL = 'http://localhost:8000';

/**
 * ファイルパスをフルURLに変換する関数
 * @param path ファイルパス
 * @returns フルURL
 */
export const getFileUrl = (path: string): string => {
  if (!path) return '';
  
  return `${API_BASE_URL}/${path}`;
}

