import MechanismService from '../../services/mechanismService';
import api from '../../services/api';
import { MechanismDetail, MechanismFormData, PaginatedMechanismResponse, MechanismViewCount, MechanismViewsResponse } from '../../types/mechanism';

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
      expect(api.get).toHaveBeenCalledWith('/api/mechanisms?page=1&limit=10');
      expect(result).toEqual(mockPaginatedResponse);
    });

    it('ページネーションパラメータを指定して取得できること', async () => {
      // Arrange
      (api.get as jest.Mock).mockResolvedValueOnce({ data: mockPaginatedResponse });
      
      // Act
      const result = await MechanismService.getMechanisms(2, 20);
      
      // Assert
      expect(api.get).toHaveBeenCalledWith('/api/mechanisms?page=2&limit=20');
      expect(result).toEqual(mockPaginatedResponse);
    });

    it('エラー時に例外をスローすること', async () => {
      // Arrange
      const error = new Error('API error');
      (api.get as jest.Mock).mockRejectedValueOnce(error);
      
      // Act & Assert
      await expect(MechanismService.getMechanisms()).rejects.toThrow(error);
      expect(api.get).toHaveBeenCalledWith('/api/mechanisms?page=1&limit=10');
    });
  });

  describe('getMechanismById', () => {
    it('正常にメカニズム詳細を取得できること', async () => {
      // Arrange
      (api.get as jest.Mock).mockResolvedValueOnce({ data: mockMechanismDetail });
      
      // Act
      const result = await MechanismService.getMechanismById(1);
      
      // Assert
      expect(api.get).toHaveBeenCalledWith('/api/mechanisms/1');
      expect(result).toEqual(mockMechanismDetail);
    });

    it('エラー時に例外をスローすること', async () => {
      // Arrange
      const error = new Error('API error');
      (api.get as jest.Mock).mockRejectedValueOnce(error);
      
      // Act & Assert
      await expect(MechanismService.getMechanismById(1)).rejects.toThrow(error);
      expect(api.get).toHaveBeenCalledWith('/api/mechanisms/1');
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
      expect(api.post).toHaveBeenCalledWith('/api/mechanisms', expect.any(FormData), {
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
      expect(api.post).toHaveBeenCalledWith('/api/mechanisms', expect.any(FormData), {
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
      expect(api.post).toHaveBeenCalledWith('/api/likes', { mechanism_id: 1 });
      expect(result).toEqual(mockLikeResponse);
    });

    it('エラー時に例外をスローすること', async () => {
      // Arrange
      const error = new Error('API error');
      (api.post as jest.Mock).mockRejectedValueOnce(error);
      
      // Act & Assert
      await expect(MechanismService.likeMechanism(1)).rejects.toThrow(error);
      expect(api.post).toHaveBeenCalledWith('/api/likes', { mechanism_id: 1 });
    });
  });

  describe('unlikeMechanism', () => {
    it('正常にいいねを取り消せること', async () => {
      // Arrange
      (api.delete as jest.Mock).mockResolvedValueOnce({});
      
      // Act
      await MechanismService.unlikeMechanism(1);
      
      // Assert
      expect(api.delete).toHaveBeenCalledWith('/api/likes/1');
    });

    it('エラー時に例外をスローすること', async () => {
      // Arrange
      const error = new Error('API error');
      (api.delete as jest.Mock).mockRejectedValueOnce(error);
      
      // Act & Assert
      await expect(MechanismService.unlikeMechanism(1)).rejects.toThrow(error);
      expect(api.delete).toHaveBeenCalledWith('/api/likes/1');
    });
  });

  describe('recordMechanismView', () => {
    it('正常に閲覧履歴を記録できること', async () => {
      // Arrange
      const mockViewResponse = { mechanism_id: 1, user_id: 1, view_count: 1 };
      (api.post as jest.Mock).mockResolvedValueOnce({ data: mockViewResponse });
      
      // Act
      const result = await MechanismService.recordMechanismView(1);
      
      // Assert
      expect(api.post).toHaveBeenCalledWith('/api/mechanisms/1/view');
      expect(result).toEqual(mockViewResponse);
    });

    it('エラー時に例外をスローすること', async () => {
      // Arrange
      const error = new Error('API error');
      (api.post as jest.Mock).mockRejectedValueOnce(error);
      
      // Act & Assert
      await expect(MechanismService.recordMechanismView(1)).rejects.toThrow(error);
      expect(api.post).toHaveBeenCalledWith('/api/mechanisms/1/view');
    });
  });

  describe('getMechanismViews', () => {
    it('正常に閲覧回数を取得できること', async () => {
      // Arrange
      const mockViewCountResponse: MechanismViewCount = {
        mechanism_id: 1,
        total_views: 10,
        user_views: 3
      };
      (api.get as jest.Mock).mockResolvedValueOnce({ data: mockViewCountResponse });
      
      // Act
      const result = await MechanismService.getMechanismViews(1);
      
      // Assert
      expect(api.get).toHaveBeenCalledWith('/api/mechanisms/1/views');
      expect(result).toEqual(mockViewCountResponse);
    });

    it('エラー時に例外をスローすること', async () => {
      // Arrange
      const error = new Error('API error');
      (api.get as jest.Mock).mockRejectedValueOnce(error);
      
      // Act & Assert
      await expect(MechanismService.getMechanismViews(1)).rejects.toThrow(error);
      expect(api.get).toHaveBeenCalledWith('/api/mechanisms/1/views');
    });
  });

  describe('getMechanismsViews', () => {
    it('正常に複数メカニズムの閲覧回数を一括取得できること', async () => {
      // Arrange
      const mockViewsResponse: MechanismViewsResponse = {
        items: [
          { mechanism_id: 1, total_views: 10, user_views: 3 },
          { mechanism_id: 2, total_views: 5, user_views: 1 }
        ]
      };
      (api.post as jest.Mock).mockResolvedValueOnce({ data: mockViewsResponse });
      
      // Act
      const result = await MechanismService.getMechanismsViews([1, 2]);
      
      // Assert
      expect(api.post).toHaveBeenCalledWith('/api/mechanisms/views/batch', [1, 2]);
      expect(result).toEqual(mockViewsResponse);
    });

    it('エラー時に例外をスローすること', async () => {
      // Arrange
      const error = new Error('API error');
      (api.post as jest.Mock).mockRejectedValueOnce(error);
      
      // Act & Assert
      await expect(MechanismService.getMechanismsViews([1, 2])).rejects.toThrow(error);
      expect(api.post).toHaveBeenCalledWith('/api/mechanisms/views/batch', [1, 2]);
    });
  });
});
