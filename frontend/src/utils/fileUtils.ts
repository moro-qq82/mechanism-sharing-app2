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
  
  // パスが "uploads/" で始まる場合は、その部分を除去
  const normalizedPath = path.startsWith('uploads/') 
    ? path.substring(8) // "uploads/".length
    : path;
  
  return `${API_BASE_URL}/uploads/${normalizedPath}`;
};
