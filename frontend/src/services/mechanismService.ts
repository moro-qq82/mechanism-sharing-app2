import api from './api';
import { PaginatedMechanismResponse, MechanismDetail, MechanismFormData } from '../types/mechanism';

/**
 * メカニズムサービス
 * メカニズム関連のAPI呼び出しを行うサービス
 */
export const MechanismService = {
  /**
   * メカニズム一覧を取得する
   * @param page ページ番号（デフォルト: 1）
   * @param limit 1ページあたりの件数（デフォルト: 10）
   * @returns メカニズム一覧とページネーション情報
   */
  async getMechanisms(page: number = 1, limit: number = 10): Promise<PaginatedMechanismResponse> {
    try {
      const response = await api.get(`/mechanisms?page=${page}&limit=${limit}`);
      return response.data;
    } catch (error) {
      console.error('メカニズム一覧の取得に失敗しました', error);
      throw error;
    }
  },

  /**
   * 指定されたIDのメカニズム詳細を取得する
   * @param id メカニズムID
   * @returns メカニズム詳細情報
   */
  async getMechanismById(id: number): Promise<MechanismDetail> {
    try {
      const response = await api.get(`/mechanisms/${id}`);
      return response.data;
    } catch (error) {
      console.error(`メカニズム(ID: ${id})の取得に失敗しました`, error);
      throw error;
    }
  },

  /**
   * 新しいメカニズムを作成する
   * @param mechanismData メカニズム作成データ
   * @returns 作成されたメカニズム情報
   */
  async createMechanism(mechanismData: MechanismFormData): Promise<MechanismDetail> {
    try {
      // FormDataオブジェクトを作成
      const formData = new FormData();
      formData.append('title', mechanismData.title);
      formData.append('description', mechanismData.description);
      formData.append('reliability', mechanismData.reliability.toString());
      formData.append('categories', mechanismData.categories);
      
      // ファイルを追加
      if (mechanismData.file) {
        formData.append('file', mechanismData.file);
      }
      
      // サムネイルを追加（オプション）
      if (mechanismData.thumbnail) {
        formData.append('thumbnail', mechanismData.thumbnail);
      }
      
      // multipart/form-dataでリクエスト
      const response = await api.post('/mechanisms', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      
      return response.data;
    } catch (error) {
      console.error('メカニズムの作成に失敗しました', error);
      throw error;
    }
  },

  /**
   * メカニズムにいいねを付ける
   * @param mechanismId メカニズムID
   * @returns いいね情報
   */
  async likeMechanism(mechanismId: number): Promise<{ mechanism_id: number; user_id: number }> {
    try {
      const response = await api.post(`/likes`, { mechanism_id: mechanismId });
      return response.data;
    } catch (error) {
      console.error(`メカニズム(ID: ${mechanismId})へのいいねに失敗しました`, error);
      throw error;
    }
  },

  /**
   * メカニズムのいいねを取り消す
   * @param mechanismId メカニズムID
   */
  async unlikeMechanism(mechanismId: number): Promise<void> {
    try {
      await api.delete(`/likes/${mechanismId}`);
    } catch (error) {
      console.error(`メカニズム(ID: ${mechanismId})のいいね取り消しに失敗しました`, error);
      throw error;
    }
  }
};

export default MechanismService;
