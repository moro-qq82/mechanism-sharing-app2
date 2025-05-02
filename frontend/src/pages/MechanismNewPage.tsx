import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import Input from '../components/common/Input';
import TextArea from '../components/common/TextArea';
import Select from '../components/common/Select';
import FileUpload from '../components/common/FileUpload';
import Button from '../components/common/Button';
import { MechanismFormData } from '../types/mechanism';
import MechanismService from '../services/mechanismService';

const MechanismNewPage: React.FC = () => {
  const navigate = useNavigate();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [formErrors, setFormErrors] = useState<Record<string, string>>({});
  
  // フォームの状態
  const [formData, setFormData] = useState<MechanismFormData>({
    title: '',
    description: '',
    reliability: 1,
    categories: '',
    file: null,
    thumbnail: null
  });
  
  // ファイル参照
  const fileInputRef = useRef<HTMLInputElement>(null);
  const thumbnailInputRef = useRef<HTMLInputElement>(null);
  
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
  
  // ファイル変更ハンドラー
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, files } = e.target;
    if (files && files.length > 0) {
      setFormData(prev => ({
        ...prev,
        [name]: files[0]
      }));
      
      // エラーをクリア
      if (formErrors[name]) {
        setFormErrors(prev => ({
          ...prev,
          [name]: ''
        }));
      }
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
    
    if (!formData.file) {
      errors.file = 'メカニズムファイルは必須です';
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
      await MechanismService.createMechanism(formData);
      // 成功したらホームページにリダイレクト
      navigate('/');
    } catch (err) {
      console.error('メカニズムの投稿に失敗しました', err);
      setError('メカニズムの投稿に失敗しました。');
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
  
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center">
            <h1 className="text-3xl font-bold text-gray-900">新規メカニズム投稿</h1>
            <Button
              variant="outline"
              onClick={() => navigate('/')}
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
              {error && (
                <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-md">
                  <p className="text-red-600">{error}</p>
                </div>
              )}
              <form className="space-y-8 divide-y divide-gray-200" onSubmit={handleSubmit}>
                <div className="space-y-8 divide-y divide-gray-200">
                  <div>
                    <div>
                      <h3 className="text-lg leading-6 font-medium text-gray-900">メカニズム情報</h3>
                      <p className="mt-1 text-sm text-gray-500">
                        メカニズムに関する基本情報を入力してください。
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

                  <div className="pt-8">
                    <div>
                      <h3 className="text-lg leading-6 font-medium text-gray-900">ファイル</h3>
                      <p className="mt-1 text-sm text-gray-500">メカニズムに関するファイルをアップロードしてください。</p>
                    </div>
                    <div className="mt-6">
                      <div className="sm:col-span-6">
                        <FileUpload
                          ref={fileInputRef}
                          id="file"
                          name="file"
                          label="メカニズムファイル"
                          onChange={handleFileChange}
                          acceptedFileTypes="application/pdf,application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document,application/vnd.ms-powerpoint,application/vnd.openxmlformats-officedocument.presentationml.presentation,application/vnd.ms-excel,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,image/jpeg,image/png,image/gif"
                          buttonText="ファイルを選択"
                          error={formErrors.file}
                          helperText="PDF, DOC, DOCX, PPT, PPTX, XLS, XLSX, JPG, PNG, GIF"
                          fullWidth
                        />
                      </div>

                      <div className="sm:col-span-6 mt-6">
                        <FileUpload
                          ref={thumbnailInputRef}
                          id="thumbnail"
                          name="thumbnail"
                          label="サムネイル画像（オプション）"
                          onChange={handleFileChange}
                          acceptedFileTypes="image/jpeg,image/png,image/gif"
                          buttonText="画像を選択"
                          helperText="JPG, PNG, GIF"
                          fullWidth
                        />
                      </div>
                    </div>
                  </div>
                </div>

                <div className="pt-5">
                  <div className="flex justify-end">
                    <Button
                      type="button"
                      variant="outline"
                      onClick={() => navigate('/')}
                      className="mr-3"
                    >
                      キャンセル
                    </Button>
                    <Button
                      type="submit"
                      isLoading={isSubmitting}
                      disabled={isSubmitting}
                    >
                      投稿する
                    </Button>
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

export default MechanismNewPage;
