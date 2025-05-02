import MechanismService from '../../services/mechanismService';
import api from '../../services/api';
import { MechanismDetail, MechanismFormData, PaginatedMechanismResponse } from '../../types/mechanism';

// apiをモック化
jest.mock('../../services/api', () => ({
  get: jest.fn(),
  post: jest.fn(),
  delete: jest.fn(),
}));

describe('MechanismService', () => {
  // 各テスト前にモックをリセット
  beforeEach(() => {
    jest.clearAllMocks();
  });

  // モックデータ
  const mockPaginatedResponse: PaginatedMechanismResponse = {
    items: [
      {
        id: 1,
        title: 'テストメカニズム1',
        description: 'これはテスト用のメカニズムです。',
        reliability: 3,
        thumbnail_path: '/test-thumbnail.jpg',
        user: {
          id: 1,
          email: 'test@example.com',
          created_at: '2025-04-01T00:00:00Z'
        },
        categories: ['テスト', '機械'],
        likes_count: 5,
        created_at: '2025-04-25T14:30:00Z'
      }
    ],
    total: 10,
    page: 1,
    limit: 10,
    pages: 1
  };

  const mockMechanismDetail: MechanismDetail = {
    id: 1,
    title: 'テストメカニズム',
    description: 'これはテスト用のメカニズム詳細です。',
    reliability: 3,
    thumbnail_path: '/test-thumbnail.jpg',
    file_path: '/test-file.pdf',
    user: {
      id: 1,
      email: 'test@example.com',
      created_at: '2025-04-01T00:00:00Z'
    },
    categories: ['テスト', '機械'],
    likes_count: 5,
    created_at: '2025-04-25T14:30:00Z',
    updated_at: '2025-04-25T15:30:00Z'
  };

  describe('getMechanisms', () => {
    it('正常にメカニズム一覧を取得できること', async () => {
      // Arrange
      (api.get as jest.Mock).mockResolvedValueOnce({ data: mockPaginatedResponse });
      
      // Act
      const result = await MechanismService.getMechanisms();
      
      // Assert
      expect(api.get).toHaveBeenCalledWith('/mechanisms?page=1&limit=10');
      expect(result).toEqual(mockPaginatedResponse);
    });

    it('ページネーションパラメータを指定して取得できること', async () => {
      // Arrange
      (api.get as jest.Mock).mockResolvedValueOnce({ data: mockPaginatedResponse });
      
      // Act
      const result = await MechanismService.getMechanisms(2, 20);
      
      // Assert
      expect(api.get).toHaveBeenCalledWith('/mechanisms?page=2&limit=20');
      expect(result).toEqual(mockPaginatedResponse);
    });

    it('エラー時に例外をスローすること', async () => {
      // Arrange
      const error = new Error('API error');
      (api.get as jest.Mock).mockRejectedValueOnce(error);
      
      // Act & Assert
      await expect(MechanismService.getMechanisms()).rejects.toThrow(error);
      expect(api.get).toHaveBeenCalledWith('/mechanisms?page=1&limit=10');
    });
  });

  describe('getMechanismById', () => {
    it('正常にメカニズム詳細を取得できること', async () => {
      // Arrange
      (api.get as jest.Mock).mockResolvedValueOnce({ data: mockMechanismDetail });
      
      // Act
      const result = await MechanismService.getMechanismById(1);
      
      // Assert
      expect(api.get).toHaveBeenCalledWith('/mechanisms/1');
      expect(result).toEqual(mockMechanismDetail);
    });

    it('エラー時に例外をスローすること', async () => {
      // Arrange
      const error = new Error('API error');
      (api.get as jest.Mock).mockRejectedValueOnce(error);
      
      // Act & Assert
      await expect(MechanismService.getMechanismById(1)).rejects.toThrow(error);
      expect(api.get).toHaveBeenCalledWith('/mechanisms/1');
    });
  });

  describe('createMechanism', () => {
    it('正常にメカニズムを作成できること', async () => {
      // Arrange
      (api.post as jest.Mock).mockResolvedValueOnce({ data: mockMechanismDetail });
      
      const file = new File(['test'], 'test.pdf', { type: 'application/pdf' });
      const thumbnail = new File(['test'], 'thumbnail.jpg', { type: 'image/jpeg' });
      
      const formData: MechanismFormData = {
        title: 'テストメカニズム',
        description: 'これはテスト用のメカニズムです。',
        reliability: 3,
        categories: 'テスト,機械',
        file: file,
        thumbnail: thumbnail
      };
      
      // Act
      const result = await MechanismService.createMechanism(formData);
      
      // Assert
      expect(api.post).toHaveBeenCalledWith('/mechanisms', expect.any(FormData), {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      expect(result).toEqual(mockMechanismDetail);
      
      // FormDataの内容を検証
      const calledFormData = (api.post as jest.Mock).mock.calls[0][1];
      expect(calledFormData).toBeInstanceOf(FormData);
    });

    it('エラー時に例外をスローすること', async () => {
      // Arrange
      const error = new Error('API error');
      (api.post as jest.Mock).mockRejectedValueOnce(error);
      
      const formData: MechanismFormData = {
        title: 'テストメカニズム',
        description: 'これはテスト用のメカニズムです。',
        reliability: 3,
        categories: 'テスト,機械',
        file: new File(['test'], 'test.pdf', { type: 'application/pdf' }),
        thumbnail: null
      };
      
      // Act & Assert
      await expect(MechanismService.createMechanism(formData)).rejects.toThrow(error);
      expect(api.post).toHaveBeenCalledWith('/mechanisms', expect.any(FormData), {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
    });
  });

  describe('likeMechanism', () => {
    it('正常にいいねを付けられること', async () => {
      // Arrange
      const mockLikeResponse = { mechanism_id: 1, user_id: 1 };
      (api.post as jest.Mock).mockResolvedValueOnce({ data: mockLikeResponse });
      
      // Act
      const result = await MechanismService.likeMechanism(1);
      
      // Assert
      expect(api.post).toHaveBeenCalledWith('/likes', { mechanism_id: 1 });
      expect(result).toEqual(mockLikeResponse);
    });

    it('エラー時に例外をスローすること', async () => {
      // Arrange
      const error = new Error('API error');
      (api.post as jest.Mock).mockRejectedValueOnce(error);
      
      // Act & Assert
      await expect(MechanismService.likeMechanism(1)).rejects.toThrow(error);
      expect(api.post).toHaveBeenCalledWith('/likes', { mechanism_id: 1 });
    });
  });

  describe('unlikeMechanism', () => {
    it('正常にいいねを取り消せること', async () => {
      // Arrange
      (api.delete as jest.Mock).mockResolvedValueOnce({});
      
      // Act
      await MechanismService.unlikeMechanism(1);
      
      // Assert
      expect(api.delete).toHaveBeenCalledWith('/likes/1');
    });

    it('エラー時に例外をスローすること', async () => {
      // Arrange
      const error = new Error('API error');
      (api.delete as jest.Mock).mockRejectedValueOnce(error);
      
      // Act & Assert
      await expect(MechanismService.unlikeMechanism(1)).rejects.toThrow(error);
      expect(api.delete).toHaveBeenCalledWith('/likes/1');
    });
  });
});
