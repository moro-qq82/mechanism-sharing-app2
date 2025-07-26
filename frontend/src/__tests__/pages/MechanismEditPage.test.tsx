import React from 'react';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import MechanismEditPage from '../../pages/MechanismEditPage';
import MechanismService from '../../services/mechanismService';
import { MechanismDetail } from '../../types/mechanism';

// MechanismServiceのモック
jest.mock('../../services/mechanismService');

// モックデータ
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

// テスト用のコンポーネントラッパー
const renderWithRouter = (mechanismId: string = '1') => {
  return render(
    <MemoryRouter initialEntries={[`/mechanisms/${mechanismId}/edit`]}>
      <Routes>
        <Route path="/mechanisms/:id/edit" element={<MechanismEditPage />} />
        <Route path="/mechanisms/:id" element={<div>Detail Page</div>} />
        <Route path="/" element={<div>Home Page</div>} />
      </Routes>
    </MemoryRouter>
  );
};

describe('MechanismEditPage', () => {
  const mockGetMechanismById = jest.fn();
  const mockUpdateMechanism = jest.fn();

  beforeEach(() => {
    // モック関数のリセット
    jest.clearAllMocks();
    
    // MechanismServiceのモック設定
    (MechanismService.getMechanismById as jest.Mock) = mockGetMechanismById;
    (MechanismService.updateMechanism as jest.Mock) = mockUpdateMechanism;
    
    // デフォルトのモック戻り値設定
    mockGetMechanismById.mockResolvedValue(mockMechanismDetail);
    mockUpdateMechanism.mockResolvedValue(mockMechanismDetail);
  });

  test('メカニズムの読み込みとフォーム表示', async () => {
    renderWithRouter();

    // ローディング中の表示確認
    expect(screen.getByText('メカニズムを読み込み中...')).toBeInTheDocument();

    // データ読み込み完了後の表示確認
    await waitFor(() => {
      expect(screen.getByDisplayValue('テストメカニズム')).toBeInTheDocument();
    });

    expect(screen.getByDisplayValue('これはテスト用のメカニズム詳細です。')).toBeInTheDocument();
    expect(screen.getByDisplayValue('テスト, 機械')).toBeInTheDocument();
    
    // セレクトボックスの値確認
    const reliabilitySelect = screen.getByRole('combobox', { name: /信頼性レベル/ });
    expect(reliabilitySelect).toHaveValue('3');

    // APIが正しく呼び出されることを確認
    expect(mockGetMechanismById).toHaveBeenCalledWith(1);
  });

  test('フォーム入力の変更', async () => {
    renderWithRouter();

    await waitFor(() => {
      expect(screen.getByDisplayValue('テストメカニズム')).toBeInTheDocument();
    });

    // タイトルの変更
    const titleInput = screen.getByDisplayValue('テストメカニズム');
    fireEvent.change(titleInput, { target: { value: '更新されたタイトル' } });
    expect(titleInput).toHaveValue('更新されたタイトル');

    // 説明の変更
    const descriptionInput = screen.getByDisplayValue('これはテスト用のメカニズム詳細です。');
    fireEvent.change(descriptionInput, { target: { value: '更新された説明' } });
    expect(descriptionInput).toHaveValue('更新された説明');

    // カテゴリーの変更
    const categoriesInput = screen.getByDisplayValue('テスト, 機械');
    fireEvent.change(categoriesInput, { target: { value: '新カテゴリー' } });
    expect(categoriesInput).toHaveValue('新カテゴリー');
  });

  test('フォーム送信の成功', async () => {
    renderWithRouter();

    await waitFor(() => {
      expect(screen.getByDisplayValue('テストメカニズム')).toBeInTheDocument();
    });

    // フォームデータの変更
    const titleInput = screen.getByDisplayValue('テストメカニズム');
    fireEvent.change(titleInput, { target: { value: '更新されたタイトル' } });

    // 送信ボタンをクリック
    const submitButton = screen.getByRole('button', { name: '更新する' });
    fireEvent.click(submitButton);

    // API呼び出しの確認
    await waitFor(() => {
      expect(mockUpdateMechanism).toHaveBeenCalledWith(1, {
        title: '更新されたタイトル',
        description: 'これはテスト用のメカニズム詳細です。',
        reliability: 3,
        categories: ['テスト', '機械']
      });
    });
  });

  test('バリデーションエラーの表示', async () => {
    renderWithRouter();

    await waitFor(() => {
      expect(screen.getByDisplayValue('テストメカニズム')).toBeInTheDocument();
    });

    // 必須フィールドをクリア
    const titleInput = screen.getByDisplayValue('テストメカニズム');
    fireEvent.change(titleInput, { target: { value: '' } });

    const descriptionInput = screen.getByDisplayValue('これはテスト用のメカニズム詳細です。');
    fireEvent.change(descriptionInput, { target: { value: '' } });

    // 送信ボタンをクリック
    const submitButton = screen.getByRole('button', { name: '更新する' });
    fireEvent.click(submitButton);

    // エラーメッセージの確認
    await waitFor(() => {
      expect(screen.getAllByText('タイトルは必須です')).toHaveLength(2); // フィールドエラーとサマリーエラー
      expect(screen.getAllByText('説明は必須です')).toHaveLength(2); // フィールドエラーとサマリーエラー
    });

    // API呼び出しがされないことを確認
    expect(mockUpdateMechanism).not.toHaveBeenCalled();
  });

  test('更新処理のエラーハンドリング', async () => {
    // console.errorをモック
    const consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation();
    
    // 更新処理でエラーを発生させる
    mockUpdateMechanism.mockRejectedValue(new Error('Update failed'));

    renderWithRouter();

    await waitFor(() => {
      expect(screen.getByDisplayValue('テストメカニズム')).toBeInTheDocument();
    });

    // 送信ボタンをクリック
    const submitButton = screen.getByRole('button', { name: '更新する' });
    fireEvent.click(submitButton);

    // エラーメッセージの確認
    await waitFor(() => {
      expect(screen.getByText('メカニズムの更新に失敗しました。編集権限がない可能性があります。')).toBeInTheDocument();
    });
    
    // console.errorが呼ばれたことを確認
    expect(consoleErrorSpy).toHaveBeenCalled();
    
    // スパイをリストア
    consoleErrorSpy.mockRestore();
  });

  test('キャンセルボタンの動作', async () => {
    renderWithRouter();

    await waitFor(() => {
      expect(screen.getByDisplayValue('テストメカニズム')).toBeInTheDocument();
    });

    // キャンセルボタンが存在することを確認
    const cancelButtons = screen.getAllByText('キャンセル');
    expect(cancelButtons.length).toBeGreaterThan(0);
  });

  test('メカニズム読み込みエラーの処理', async () => {
    // console.errorをモック
    const consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation();
    
    // 読み込み処理でエラーを発生させる
    mockGetMechanismById.mockRejectedValue(new Error('Failed to load'));

    renderWithRouter();

    // エラーメッセージの確認
    await waitFor(() => {
      expect(screen.getByText('メカニズムの読み込みに失敗しました。')).toBeInTheDocument();
    });
    
    // console.errorが呼ばれたことを確認
    expect(consoleErrorSpy).toHaveBeenCalled();
    
    // スパイをリストア
    consoleErrorSpy.mockRestore();
  });

  test('存在しないメカニズムIDの処理', async () => {
    // console.errorをモック（メカニズムが見つからない場合のエラーログを抑制）
    const consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation();
    
    // 存在しないメカニズムの場合はnullを返す
    mockGetMechanismById.mockResolvedValue(null);

    renderWithRouter('999');

    await waitFor(() => {
      expect(screen.getByText('メカニズムが見つかりません。')).toBeInTheDocument();
    });

    expect(screen.getByText('ホームに戻る')).toBeInTheDocument();
    
    // スパイをリストア
    consoleErrorSpy.mockRestore();
  });
});