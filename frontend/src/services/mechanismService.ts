import api from './api';
import { PaginatedMechanismResponse, MechanismDetail, MechanismFormData, MechanismUpdateData, MechanismViewCount, MechanismViewsResponse, MechanismDownloadCount, MechanismDownloadsResponse } from '../types/mechanism';

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
      const response = await api.get(`/api/mechanisms?page=${page}&limit=${limit}`);
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
      const response = await api.get(`/api/mechanisms/${id}`);
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
      const response = await api.post('/api/mechanisms', formData, {
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
   * メカニズムを更新する
   * @param id メカニズムID
   * @param updateData 更新データ
   * @returns 更新されたメカニズム情報
   */
  async updateMechanism(id: number, updateData: MechanismUpdateData): Promise<MechanismDetail> {
    try {
      const response = await api.put(`/api/mechanisms/${id}`, updateData);
      return response.data;
    } catch (error) {
      console.error(`メカニズム(ID: ${id})の更新に失敗しました`, error);
      throw error;
    }
  },

  /**
   * メカニズムを削除する
   * @param id メカニズムID
   * @returns 削除の成功/失敗
   */
  async deleteMechanism(id: number): Promise<void> {
    try {
      await api.delete(`/api/mechanisms/${id}`);
    } catch (error) {
      console.error(`メカニズム(ID: ${id})の削除に失敗しました`, error);
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
      const response = await api.post(`/api/likes`, { mechanism_id: mechanismId });
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
      await api.delete(`/api/likes/${mechanismId}`);
    } catch (error) {
      console.error(`メカニズム(ID: ${mechanismId})のいいね取り消しに失敗しました`, error);
      throw error;
    }
  },

  /**
   * メカニズム閲覧履歴を記録する
   * @param mechanismId メカニズムID
   * @returns 記録された閲覧履歴
   */
  async recordMechanismView(mechanismId: number): Promise<any> {
    try {
      const response = await api.post(`/api/mechanisms/${mechanismId}/view`);
      return response.data;
    } catch (error) {
      console.error(`メカニズム(ID: ${mechanismId})の閲覧履歴記録に失敗しました`, error);
      throw error;
    }
  },

  /**
   * メカニズムの閲覧回数を取得する
   * @param mechanismId メカニズムID
   * @returns 閲覧回数情報
   */
  async getMechanismViews(mechanismId: number): Promise<MechanismViewCount> {
    try {
      const response = await api.get(`/api/mechanisms/${mechanismId}/views`);
      return response.data;
    } catch (error) {
      console.error(`メカニズム(ID: ${mechanismId})の閲覧回数取得に失敗しました`, error);
      throw error;
    }
  },

  /**
   * 複数メカニズムの閲覧回数を一括取得する
   * @param mechanismIds メカニズムIDのリスト
   * @returns 閲覧回数情報のリスト
   */
  async getMechanismsViews(mechanismIds: number[]): Promise<MechanismViewsResponse> {
    try {
      const response = await api.post(`/api/mechanisms/views/batch`, mechanismIds);
      return response.data;
    } catch (error) {
      console.error(`複数メカニズムの閲覧回数取得に失敗しました`, error);
      throw error;
    }
  },

  /**
   * メカニズムダウンロード履歴を記録する
   * @param mechanismId メカニズムID
   * @returns 記録されたダウンロード履歴
   */
  async recordMechanismDownload(mechanismId: number): Promise<any> {
    try {
      const response = await api.post(`/api/mechanisms/${mechanismId}/download`);
      return response.data;
    } catch (error) {
      console.error(`メカニズム(ID: ${mechanismId})のダウンロード履歴記録に失敗しました`, error);
      throw error;
    }
  },

  /**
   * メカニズムのダウンロード回数を取得する
   * @param mechanismId メカニズムID
   * @returns ダウンロード回数情報
   */
  async getMechanismDownloads(mechanismId: number): Promise<MechanismDownloadCount> {
    try {
      const response = await api.get(`/api/mechanisms/${mechanismId}/downloads`);
      return response.data;
    } catch (error) {
      console.error(`メカニズム(ID: ${mechanismId})のダウンロード回数取得に失敗しました`, error);
      throw error;
    }
  },

  /**
   * 複数メカニズムのダウンロード回数を一括取得する
   * @param mechanismIds メカニズムIDのリスト
   * @returns ダウンロード回数情報のリスト
   */
  async getMechanismsDownloads(mechanismIds: number[]): Promise<MechanismDownloadsResponse> {
    try {
      const response = await api.post(`/api/mechanisms/downloads/batch`, mechanismIds);
      return response.data;
    } catch (error) {
      console.error(`複数メカニズムのダウンロード回数取得に失敗しました`, error);
      throw error;
    }
  }
};

export default MechanismService;
