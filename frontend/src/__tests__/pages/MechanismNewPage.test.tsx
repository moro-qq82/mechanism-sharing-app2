import React from 'react';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import MechanismNewPage from '../../pages/MechanismNewPage';
import MechanismService from '../../services/mechanismService';
import { AuthProvider, useAuth } from '../../contexts/AuthContext';

// MechanismServiceのモック
jest.mock('../../services/mechanismService');

// 認証コンテキストのモック
jest.mock('../../contexts/AuthContext', () => {
  const originalModule = jest.requireActual('../../contexts/AuthContext');
  return {
    ...originalModule,
    useAuth: jest.fn(),
  };
});

// テスト用のコンポーネントラッパー
const renderWithRouter = () => {
  return render(
    <MemoryRouter initialEntries={['/mechanisms/new']}>
      <AuthProvider>
        <Routes>
          <Route path="/mechanisms/new" element={<MechanismNewPage />} />
          <Route path="/" element={<div>ホームページ</div>} />
        </Routes>
      </AuthProvider>
    </MemoryRouter>
  );
};

describe('MechanismNewPage', () => {
  beforeEach(() => {
    // モックのリセット
    jest.clearAllMocks();
    
    // createMechanismのモック実装
    (MechanismService.createMechanism as jest.Mock).mockResolvedValue({
      id: 1,
      title: 'テストメカニズム',
      description: 'これはテスト用のメカニズムです。',
      reliability: 3,
      thumbnail_path: '/test-thumbnail.jpg',
      file_path: '/test-file.pdf',
      user: {
        id: 1,
        email: 'test@example.com',
        created_at: '2025-04-01T00:00:00Z'
      },
      categories: ['テスト', '機械'],
      likes_count: 0,
      created_at: '2025-05-02T00:00:00Z',
      updated_at: '2025-05-02T00:00:00Z'
    });
    
    // 認証済み状態をモック
    (useAuth as jest.Mock).mockReturnValue({
      isAuthenticated: true,
      user: { id: 1, email: 'test@example.com', created_at: '2025-04-01T00:00:00Z' },
      token: 'test-token',
      loading: false,
      error: null,
      login: jest.fn(),
      register: jest.fn(),
      logout: jest.fn()
    });
  });

  test('フォームが正しく表示されること', () => {
    renderWithRouter();
    
    // タイトルが表示されることを確認
    expect(screen.getByText('新規メカニズム投稿')).toBeInTheDocument();
    
    // フォーム要素が表示されることを確認
    expect(screen.getByLabelText('タイトル')).toBeInTheDocument();
    expect(screen.getByLabelText('説明')).toBeInTheDocument();
    expect(screen.getByLabelText('信頼性レベル')).toBeInTheDocument();
    expect(screen.getByLabelText('カテゴリー')).toBeInTheDocument();
    expect(screen.getByLabelText('メカニズムファイル')).toBeInTheDocument();
    expect(screen.getByLabelText('サムネイル画像（オプション）')).toBeInTheDocument();
    
    // 送信ボタンが表示されることを確認
    expect(screen.getByText('投稿する')).toBeInTheDocument();
  });

  test('フォームに入力して送信できること', async () => {
    renderWithRouter();
    
    // フォームに入力
    fireEvent.change(screen.getByLabelText('タイトル'), {
      target: { value: 'テストメカニズム' }
    });
    
    fireEvent.change(screen.getByLabelText('説明'), {
      target: { value: 'これはテスト用のメカニズムです。' }
    });
    
    fireEvent.change(screen.getByLabelText('信頼性レベル'), {
      target: { value: '3' }
    });
    
    fireEvent.change(screen.getByLabelText('カテゴリー'), {
      target: { value: 'テスト,機械' }
    });
    
    // ファイルアップロード
    const mechanismFileInput = screen.getByLabelText('メカニズムファイル');
    const mechanismFile = new File(['テストファイル'], 'test.pdf', { type: 'application/pdf' });
    Object.defineProperty(mechanismFileInput, 'files', {
      value: [mechanismFile]
    });
    fireEvent.change(mechanismFileInput);
    
    // サムネイルアップロード
    const thumbnailInput = screen.getByLabelText('サムネイル画像（オプション）');
    const thumbnailFile = new File(['テスト画像'], 'thumbnail.jpg', { type: 'image/jpeg' });
    Object.defineProperty(thumbnailInput, 'files', {
      value: [thumbnailFile]
    });
    fireEvent.change(thumbnailInput);
    
    // フォーム送信
    fireEvent.click(screen.getByText('投稿する'));
    
    // APIが呼ばれることを確認
    await waitFor(() => {
      expect(MechanismService.createMechanism).toHaveBeenCalledTimes(1);
    });
    
    // 正しいパラメータでAPIが呼ばれたことを確認
    expect(MechanismService.createMechanism).toHaveBeenCalledWith({
      title: 'テストメカニズム',
      description: 'これはテスト用のメカニズムです。',
      reliability: 3,
      categories: 'テスト,機械',
      file: mechanismFile,
      thumbnail: thumbnailFile
    });
    
    // 送信成功後にホームページにリダイレクトされることを確認
    await waitFor(() => {
      expect(screen.getByText('ホームページ')).toBeInTheDocument();
    });
  });

  test('必須フィールドが空の場合にバリデーションエラーが表示されること', async () => {
    renderWithRouter();
    
    // フォーム送信（入力なし）
    fireEvent.click(screen.getByText('投稿する'));
    
    // 必須項目エラーメッセージのヘッダーが表示されるまで待機
    await waitFor(() => {
      expect(screen.getByText('必須項目が記入されていません：')).toBeInTheDocument();
    });
    
    // 各フィールドのエラーメッセージが表示されることを確認
    expect(screen.getByText('タイトルは必須です')).toBeInTheDocument();
    expect(screen.getByText('説明は必須です')).toBeInTheDocument();
    expect(screen.getByText('メカニズムファイルは必須です')).toBeInTheDocument();
    
    // エラーメッセージが投稿ボタンの下に表示されていることを確認
    const submitButton = screen.getByText('投稿する');
    const errorMessage = screen.getByText('必須項目が記入されていません：');
    expect(submitButton.compareDocumentPosition(errorMessage)).toBe(Node.DOCUMENT_POSITION_FOLLOWING);
    
    // APIが呼ばれないことを確認
    expect(MechanismService.createMechanism).not.toHaveBeenCalled();
  });

  test('APIエラー時にエラーメッセージが表示されること', async () => {
    // エラーを返すようにモックを設定
    (MechanismService.createMechanism as jest.Mock).mockRejectedValue(new Error('API error'));
    
    renderWithRouter();
    
    // フォームに入力
    fireEvent.change(screen.getByLabelText('タイトル'), {
      target: { value: 'テストメカニズム' }
    });
    
    fireEvent.change(screen.getByLabelText('説明'), {
      target: { value: 'これはテスト用のメカニズムです。' }
    });
    
    fireEvent.change(screen.getByLabelText('信頼性レベル'), {
      target: { value: '3' }
    });
    
    fireEvent.change(screen.getByLabelText('カテゴリー'), {
      target: { value: 'テスト,機械' }
    });
    
    // ファイルアップロード
    const mechanismFileInput = screen.getByLabelText('メカニズムファイル');
    const mechanismFile = new File(['テストファイル'], 'test.pdf', { type: 'application/pdf' });
    Object.defineProperty(mechanismFileInput, 'files', {
      value: [mechanismFile]
    });
    fireEvent.change(mechanismFileInput);
    
    // フォーム送信
    fireEvent.click(screen.getByText('投稿する'));
    
    // エラーメッセージが表示されるまで待機
    await waitFor(() => {
      expect(screen.getByText('メカニズムの投稿に失敗しました。')).toBeInTheDocument();
    });
    
    // エラーメッセージが投稿ボタンの下に表示されていることを確認
    const submitButton = screen.getByText('投稿する');
    const errorMessage = screen.getByText('メカニズムの投稿に失敗しました。');
    expect(submitButton.compareDocumentPosition(errorMessage)).toBe(Node.DOCUMENT_POSITION_FOLLOWING);
  });

  test('キャンセルボタンをクリックするとホームページに戻ること', async () => {
    renderWithRouter();
    
    // キャンセルボタンをクリック（フォーム内のキャンセルボタンを特定）
    fireEvent.click(screen.getByText('キャンセル', { selector: 'button[type="button"]' }));
    
    // ホームページにリダイレクトされることを確認
    await waitFor(() => {
      expect(screen.getByText('ホームページ')).toBeInTheDocument();
    });
  });
});
