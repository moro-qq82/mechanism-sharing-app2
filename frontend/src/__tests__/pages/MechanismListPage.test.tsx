import React from 'react';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import MechanismListPage from '../../pages/MechanismListPage';
import MechanismService from '../../services/mechanismService';
import { PaginatedMechanismResponse, MechanismViewsResponse } from '../../types/mechanism';

// MechanismServiceのモック
jest.mock('../../services/mechanismService');

// モックデータ
const mockMechanisms: PaginatedMechanismResponse = {
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
      views_count: 10,
      created_at: '2025-04-25T14:30:00Z'
    },
    {
      id: 2,
      title: 'テストメカニズム2',
      description: 'これは別のテスト用メカニズムです。',
      reliability: 4,
      thumbnail_path: null,
      user: {
        id: 2,
        email: 'user2@example.com',
        created_at: '2025-04-02T00:00:00Z'
      },
      categories: ['電子'],
      likes_count: 3,
      views_count: 5,
      created_at: '2025-04-24T10:15:00Z'
    }
  ],
  total: 10,
  page: 1,
  limit: 9,
  pages: 2
};

// テスト用のコンポーネントラッパー
const renderWithRouter = (component: React.ReactNode) => {
  return render(
    <BrowserRouter>
      {component}
    </BrowserRouter>
  );
};

describe('MechanismListPage', () => {
  beforeEach(() => {
    // モックのリセット
    jest.clearAllMocks();
    
    // getMechanismsのモック実装
    (MechanismService.getMechanisms as jest.Mock).mockResolvedValue(mockMechanisms);
    
    // getMechanismsViewsのモック実装
    (MechanismService.getMechanismsViews as jest.Mock).mockResolvedValue({
      items: [
        { mechanism_id: 1, total_views: 10 },
        { mechanism_id: 2, total_views: 5 }
      ]
    });
  });

  test('ローディング状態が表示されること', async () => {
    renderWithRouter(<MechanismListPage />);
    
    // ローディングコンポーネントが表示されることを確認
    expect(screen.getByRole('status')).toBeInTheDocument();
    
    // データが読み込まれるのを待つ
    await waitFor(() => {
      expect(screen.queryByRole('status')).not.toBeInTheDocument();
    });
  });

  test('メカニズム一覧が正しく表示されること', async () => {
    renderWithRouter(<MechanismListPage />);
    
    // データが読み込まれるのを待つ
    await waitFor(() => {
      expect(MechanismService.getMechanisms).toHaveBeenCalledTimes(1);
    });
    
    // ローディングが終わるのを待つ
    await waitFor(() => {
      expect(screen.queryByRole('status')).not.toBeInTheDocument();
    });
    
    // メカニズムのタイトルが表示されることを確認
    expect(screen.getByText('テストメカニズム1')).toBeInTheDocument();
    expect(screen.getByText('テストメカニズム2')).toBeInTheDocument();
    
    // 説明文が表示されることを確認
    expect(screen.getByText('これはテスト用のメカニズムです。')).toBeInTheDocument();
    expect(screen.getByText('これは別のテスト用メカニズムです。')).toBeInTheDocument();
    
    // 信頼性レベルが表示されることを確認
    expect(screen.getByText('社内複数人が支持')).toBeInTheDocument();
    expect(screen.getByText('顧客含めて定番認識化')).toBeInTheDocument();
    
    // カテゴリーが表示されることを確認
    expect(screen.getByText('テスト')).toBeInTheDocument();
    expect(screen.getByText('機械')).toBeInTheDocument();
    expect(screen.getByText('電子')).toBeInTheDocument();
    
    // いいね数が表示されることを確認
    expect(screen.getByText('いいね 5件')).toBeInTheDocument();
    expect(screen.getByText('いいね 3件')).toBeInTheDocument();
    
    // 閲覧回数が表示されることを確認
    expect(screen.getByText('閲覧 10回')).toBeInTheDocument();
    expect(screen.getByText('閲覧 5回')).toBeInTheDocument();
  });

  test('ページネーションが機能すること', async () => {
    renderWithRouter(<MechanismListPage />);
    
    // データが読み込まれるのを待つ
    await waitFor(() => {
      expect(MechanismService.getMechanisms).toHaveBeenCalledTimes(1);
    });
    
    // ローディングが終わるのを待つ
    await waitFor(() => {
      expect(screen.queryByRole('status')).not.toBeInTheDocument();
    });
    
    // ページネーションが表示されることを確認
    const nextPageButton = screen.getByLabelText('次のページへ');
    expect(nextPageButton).toBeInTheDocument();
    
    // 次のページボタンをクリック
    fireEvent.click(nextPageButton);
    
    // 2ページ目のデータを取得するためのAPIが呼ばれることを確認
    await waitFor(() => {
      expect(MechanismService.getMechanisms).toHaveBeenCalledTimes(2);
    });
    expect(MechanismService.getMechanisms).toHaveBeenLastCalledWith(2, 9);
  });

  test('APIエラー時にエラーメッセージが表示されること', async () => {
    // エラーを返すようにモックを設定
    (MechanismService.getMechanisms as jest.Mock).mockRejectedValue(new Error('API error'));
    
    renderWithRouter(<MechanismListPage />);
    
    // エラーメッセージが表示されるのを待つ
    await waitFor(() => {
      expect(screen.getByText('メカニズム一覧の取得に失敗しました。')).toBeInTheDocument();
    });
  });

  test('一部のデータ取得に失敗しても一覧が表示されること', async () => {
    // 最初のリクエストは成功、2回目のリクエスト（ページネーションなど）は失敗するように設定
    (MechanismService.getMechanisms as jest.Mock)
      .mockResolvedValueOnce(mockMechanisms)
      .mockRejectedValueOnce(new Error('API error'));
    
    // コンソールエラーをスパイ
    const consoleSpy = jest.spyOn(console, 'error').mockImplementation();
    
    renderWithRouter(<MechanismListPage />);
    
    // データが読み込まれるのを待つ
    await waitFor(() => {
      expect(MechanismService.getMechanisms).toHaveBeenCalledTimes(1);
    });
    
    // ローディングが終わるのを待つ
    await waitFor(() => {
      expect(screen.queryByRole('status')).not.toBeInTheDocument();
    });
    
    // メカニズムのタイトルが表示されることを確認
    expect(screen.getByText('テストメカニズム1')).toBeInTheDocument();
    expect(screen.getByText('テストメカニズム2')).toBeInTheDocument();
    
    // ページネーションが表示されることを確認
    const nextPageButton = screen.getByLabelText('次のページへ');
    expect(nextPageButton).toBeInTheDocument();
    
    // 次のページボタンをクリック
    fireEvent.click(nextPageButton);
    
    // エラーがコンソールに出力されることを確認
    await waitFor(() => {
      expect(consoleSpy).toHaveBeenCalled();
    });
    
    // エラーメッセージが表示されることを確認
    expect(screen.getByText('メカニズム一覧の取得に失敗しました。')).toBeInTheDocument();
    
    // スパイをリストア
    consoleSpy.mockRestore();
  });

  test('メカニズムがない場合に適切なメッセージが表示されること', async () => {
    // 空の結果を返すようにモックを設定
    (MechanismService.getMechanisms as jest.Mock).mockResolvedValue({
      items: [],
      total: 0,
      page: 1,
      limit: 9,
      pages: 0
    });
    
    renderWithRouter(<MechanismListPage />);
    
    // メッセージが表示されるのを待つ
    await waitFor(() => {
      expect(screen.getByText('メカニズムがありません。新しいメカニズムを投稿してみましょう。')).toBeInTheDocument();
    });
  });
});
