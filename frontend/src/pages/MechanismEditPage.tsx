import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import Input from '../components/common/Input';
import TextArea from '../components/common/TextArea';
import Select from '../components/common/Select';
import Button from '../components/common/Button';
import { MechanismDetail, MechanismUpdateData } from '../types/mechanism';
import MechanismService from '../services/mechanismService';

const MechanismEditPage: React.FC = () => {
  const navigate = useNavigate();
  const { id } = useParams<{ id: string }>();
  const mechanismId = parseInt(id || '0', 10);
  
  const [isLoading, setIsLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [formErrors, setFormErrors] = useState<Record<string, string>>({});
  const [mechanism, setMechanism] = useState<MechanismDetail | null>(null);
  
  // フォームの状態
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    reliability: 1,
    categories: ''
  });
  
  // メカニズムデータの読み込み
  useEffect(() => {
    const loadMechanism = async () => {
      try {
        setIsLoading(true);
        const data = await MechanismService.getMechanismById(mechanismId);
        if (data) {
          setMechanism(data);
          setFormData({
            title: data.title,
            description: data.description,
            reliability: data.reliability,
            categories: data.categories.join(', ')
          });
        } else {
          setError('メカニズムが見つかりません。');
        }
      } catch (err) {
        console.error('メカニズムの読み込みに失敗しました', err);
        setError('メカニズムの読み込みに失敗しました。');
      } finally {
        setIsLoading(false);
      }
    };

    if (mechanismId) {
      loadMechanism();
    }
  }, [mechanismId]);
  
  // 入力変更ハンドラー
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'reliability' ? parseInt(value, 10) : value
    }));
    
    // エラーをクリア
    if (formErrors[name]) {
      setFormErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };
  
  // フォームのバリデーション
  const validateForm = (): boolean => {
    const errors: Record<string, string> = {};
    
    if (!formData.title.trim()) {
      errors.title = 'タイトルは必須です';
    }
    
    if (!formData.description.trim()) {
      errors.description = '説明は必須です';
    }
    
    setFormErrors(errors);
    return Object.keys(errors).length === 0;
  };
  
  // フォーム送信ハンドラー
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // バリデーション
    if (!validateForm()) {
      return;
    }
    
    setIsSubmitting(true);
    setError(null);
    
    try {
      const updateData: MechanismUpdateData = {
        title: formData.title,
        description: formData.description,
        reliability: formData.reliability,
        categories: formData.categories.split(',').map(cat => cat.trim()).filter(cat => cat)
      };
      
      await MechanismService.updateMechanism(mechanismId, updateData);
      // 成功したら詳細ページにリダイレクト
      navigate(`/mechanisms/${mechanismId}`);
    } catch (err) {
      console.error('メカニズムの更新に失敗しました', err);
      setError('メカニズムの更新に失敗しました。編集権限がない可能性があります。');
    } finally {
      setIsSubmitting(false);
    }
  };
  
  // 信頼性レベルのオプション
  const reliabilityOptions = [
    { value: '1', label: '1 - 妄想モデル: 理論的な仮説段階' },
    { value: '2', label: '2 - 実験により一部支持: 一部の実験データで支持' },
    { value: '3', label: '3 - 社内複数人が支持: 組織内で複数の専門家が支持' },
    { value: '4', label: '4 - 顧客含めて定番認識化: 業界で広く認知' },
    { value: '5', label: '5 - 教科書に記載: 学術的に確立' }
  ];
  
  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="spinner-border animate-spin inline-block w-8 h-8 border-4 rounded-full" role="status">
            <span className="sr-only">読み込み中...</span>
          </div>
          <p className="mt-2 text-gray-600">メカニズムを読み込み中...</p>
        </div>
      </div>
    );
  }
  
  if (!mechanism) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-600">メカニズムが見つかりません。</p>
          <Button
            variant="outline"
            onClick={() => navigate('/')}
            className="mt-4"
          >
            ホームに戻る
          </Button>
        </div>
      </div>
    );
  }
  
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center">
            <h1 className="text-3xl font-bold text-gray-900">メカニズム編集</h1>
            <Button
              variant="outline"
              onClick={() => navigate(`/mechanisms/${mechanismId}`)}
            >
              キャンセル
            </Button>
          </div>
        </div>
      </header>
      <main>
        <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
          <div className="bg-white shadow overflow-hidden sm:rounded-lg">
            <div className="px-4 py-5 sm:p-6">
              <form className="space-y-8 divide-y divide-gray-200" onSubmit={handleSubmit}>
                <div className="space-y-8 divide-y divide-gray-200">
                  <div>
                    <div>
                      <h3 className="text-lg leading-6 font-medium text-gray-900">メカニズム情報</h3>
                      <p className="mt-1 text-sm text-gray-500">
                        メカニズムに関する基本情報を編集してください。
                      </p>
                    </div>

                    <div className="mt-6 grid grid-cols-1 gap-y-6 gap-x-4 sm:grid-cols-6">
                      <div className="sm:col-span-6">
                        <Input
                          id="title"
                          name="title"
                          label="タイトル"
                          value={formData.title}
                          onChange={handleInputChange}
                          placeholder="メカニズムのタイトルを入力"
                          fullWidth
                          error={formErrors.title}
                        />
                      </div>

                      <div className="sm:col-span-6">
                        <TextArea
                          id="description"
                          name="description"
                          label="説明"
                          value={formData.description}
                          onChange={handleInputChange}
                          rows={5}
                          placeholder="メカニズムの詳細な説明を入力"
                          fullWidth
                          error={formErrors.description}
                          helperText="メカニズムの動作原理や特徴について詳しく説明してください。"
                        />
                      </div>

                      <div className="sm:col-span-3">
                        <Select
                          id="reliability"
                          name="reliability"
                          label="信頼性レベル"
                          value={formData.reliability.toString()}
                          onChange={handleInputChange}
                          options={reliabilityOptions}
                          fullWidth
                        />
                      </div>

                      <div className="sm:col-span-6">
                        <Input
                          id="categories"
                          name="categories"
                          label="カテゴリー"
                          value={formData.categories}
                          onChange={handleInputChange}
                          placeholder="カテゴリーをカンマ区切りで入力（例: 機械,電子）"
                          fullWidth
                          helperText="複数のカテゴリーはカンマで区切ってください。"
                        />
                      </div>
                    </div>
                  </div>
                  
                  {/* ファイル情報の表示（編集不可） */}
                  <div className="pt-8">
                    <div>
                      <h3 className="text-lg leading-6 font-medium text-gray-900">ファイル情報</h3>
                      <p className="mt-1 text-sm text-gray-500">
                        ファイルの編集はサポートされていません。新しいファイルをアップロードする場合は、新しいメカニズムとして投稿してください。
                      </p>
                    </div>
                    <div className="mt-6 bg-gray-50 p-4 rounded-md">
                      <p className="text-sm text-gray-700">
                        <strong>現在のファイル:</strong> {mechanism.file_path}
                      </p>
                      {mechanism.thumbnail_path && (
                        <p className="text-sm text-gray-700 mt-2">
                          <strong>サムネイル:</strong> {mechanism.thumbnail_path}
                        </p>
                      )}
                    </div>
                  </div>
                </div>

                <div className="pt-5">
                  <div className="flex flex-col">
                    <div className="flex justify-end">
                      <Button
                        type="button"
                        variant="outline"
                        onClick={() => navigate(`/mechanisms/${mechanismId}`)}
                        className="mr-3"
                      >
                        キャンセル
                      </Button>
                      <Button
                        type="submit"
                        isLoading={isSubmitting}
                        disabled={isSubmitting}
                      >
                        更新する
                      </Button>
                    </div>
                    
                    {/* エラーメッセージを更新ボタンの下に表示 */}
                    {(error || Object.keys(formErrors).length > 0) && (
                      <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-md">
                        {error && <p className="text-red-600 mb-2">{error}</p>}
                        {Object.keys(formErrors).length > 0 && (
                          <div>
                            <p className="text-red-600 font-medium">必須項目が記入されていません：</p>
                            <ul className="list-disc pl-5 mt-1">
                              {Object.entries(formErrors).map(([field, message]) => (
                                <li key={field} className="text-red-600">{message}</li>
                              ))}
                            </ul>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                </div>
              </form>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default MechanismEditPage;