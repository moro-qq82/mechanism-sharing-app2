import React, { useState, useEffect, useRef } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getReliabilityLabel, getReliabilityColorClass } from '../utils/reliabilityUtils';
import MechanismService from '../services/mechanismService';
import { MechanismDetail } from '../types/mechanism';
import Loading from '../components/common/Loading';
import { useAuth } from '../contexts/AuthContext';
import { getFileUrl } from '../utils/fileUtils';

const MechanismDetailPage: React.FC = () => {
  // URLからメカニズムIDを取得
  const { id } = useParams<{ id: string }>();
  const mechanismId = parseInt(id || '0', 10);
  
  // 認証コンテキスト
    const { isAuthenticated, user } = useAuth();
  
  // 状態管理
  const [mechanism, setMechanism] = useState<MechanismDetail | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [isLiked, setIsLiked] = useState<boolean>(false);
  const [likesCount, setLikesCount] = useState<number>(0);
  const [viewsCount, setViewsCount] = useState<{ total: number; user?: number }>({ total: 0 });
  const [downloadsCount, setDownloadsCount] = useState<{ total: number; user?: number }>({ total: 0 });

  // React.StrictModeによる重複実行を防ぐためのref
  const viewRecordedRef = useRef<boolean>(false);

  // メカニズム詳細を取得する関数
  const fetchMechanismDetail = async () => {
    try {
      setLoading(true);
      const data = await MechanismService.getMechanismById(mechanismId);
      setMechanism(data);
      setLikesCount(data.likes_count);
      setError(null);
      
      // 詳細取得後に閲覧履歴を記録（重複防止）
      if (!viewRecordedRef.current) {
        try {
          await MechanismService.recordMechanismView(mechanismId);
          viewRecordedRef.current = true; // 記録済みフラグを設定
          fetchMechanismViews();
        } catch (err) {
          console.error(`閲覧履歴の記録エラー:`, err);
        }
      } else {
        // 既に記録済みの場合は閲覧回数のみ取得
        fetchMechanismViews();
      }
      
      // ダウンロード回数を取得
      fetchMechanismDownloads();
    } catch (err) {
      setError('メカニズム詳細の取得に失敗しました。');
      console.error(`メカニズム詳細の取得エラー:`, err);
    } finally {
      setLoading(false);
    }
  };

  // 閲覧回数を取得する関数
  const fetchMechanismViews = async () => {
    try {
      const viewsData = await MechanismService.getMechanismViews(mechanismId);
      setViewsCount({
        total: viewsData.total_views,
        user: viewsData.user_views
      });
    } catch (err) {
      console.error(`閲覧回数の取得エラー:`, err);
    }
  };

  // ダウンロード回数を取得する関数
  const fetchMechanismDownloads = async () => {
    try {
      const downloadsData = await MechanismService.getMechanismDownloads(mechanismId);
      setDownloadsCount({
        total: downloadsData.total_downloads,
        user: downloadsData.user_downloads
      });
    } catch (err) {
      console.error(`ダウンロード回数の取得エラー:`, err);
    }
  };

  // ダウンロードボタンのクリックハンドラ
  const handleDownload = async (e: React.MouseEvent<HTMLAnchorElement>) => {
    e.preventDefault(); // デフォルトのaタグ動作を防ぐ
    
    try {
      // 専用のダウンロードエンドポイントを使用（履歴記録はサーバー側で実行）
      const downloadUrl = `${process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000'}/api/mechanisms/${mechanismId}/download`;
      
      // 新しいwindowでダウンロードURLを開く
      window.open(downloadUrl, '_blank');
      
      // ダウンロード後に回数を更新（少し遅延を入れる）
      setTimeout(() => {
        fetchMechanismDownloads();
      }, 1000);
      
    } catch (err) {
      console.error(`ダウンロードエラー:`, err);
      alert('ファイルのダウンロードに失敗しました。');
    }
  };

  // いいね処理
  const handleLike = async () => {
    if (!isAuthenticated) {
      // 未認証の場合はログインページへリダイレクト
      // テスト環境ではwindow.location.hrefの変更がエラーになるため、try-catchで囲む
      try {
        window.location.href = '/login';
      } catch (err) {
        console.error('リダイレクトエラー:', err);
      }
      return;
    }

    try {
      if (isLiked) {
        await MechanismService.unlikeMechanism(mechanismId);
        setIsLiked(false);
        setLikesCount(prev => prev - 1);
      } else {
        await MechanismService.likeMechanism(mechanismId);
        setIsLiked(true);
        setLikesCount(prev => prev + 1);
      }
    } catch (err) {
      console.error('いいね処理エラー:', err);
    }
  };

  // コンポーネントマウント時にメカニズム詳細を取得
  useEffect(() => {
    if (mechanismId) {
      fetchMechanismDetail();
    }
  }, [mechanismId]);

  // ローディング中の表示
  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex justify-center items-center">
        <Loading text="メカニズム詳細を読み込み中..." />
      </div>
    );
  }

  // エラー時の表示
  if (error || !mechanism) {
    return (
      <div className="min-h-screen bg-gray-50">
        <header className="bg-white shadow">
          <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center">
              <h1 className="text-3xl font-bold text-gray-900">エラー</h1>
              <Link
                to="/"
                className="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              >
                一覧に戻る
              </Link>
            </div>
          </div>
        </header>
        <main>
          <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
              <span className="block sm:inline">{error}</span>
            </div>
          </div>
        </main>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center">
            <h1 className="text-3xl font-bold text-gray-900">{mechanism.title}</h1>
            <Link
              to="/"
              className="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              一覧に戻る
            </Link>
          </div>
        </div>
      </header>
      <main>
        <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
          <div className="bg-white shadow overflow-hidden sm:rounded-lg">
            <div className="px-4 py-5 sm:px-6">
              <div className="flex justify-between">
                <div>
                  <h3 className="text-lg leading-6 font-medium text-gray-900">メカニズム情報</h3>
                  <p className="mt-1 max-w-2xl text-sm text-gray-500">
                    投稿者: {mechanism.user.email}
                  </p>
                </div>
                <div className="flex items-center">
                  <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${getReliabilityColorClass(mechanism.reliability)} mr-2`}>
                    信頼性: {getReliabilityLabel(mechanism.reliability)}
                  </span>
                  <button 
                    onClick={handleLike}
                    className={`inline-flex items-center px-3 py-1 border border-transparent text-sm font-medium rounded-md text-white ${isLiked ? 'bg-pink-700' : 'bg-pink-600 hover:bg-pink-700'} focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-pink-500`}
                  >
                    いいね {likesCount}
                  </button>
                </div>
              </div>
            </div>
            <div className="border-t border-gray-200">
              <dl>
                <div className="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                  <dt className="text-sm font-medium text-gray-500">カテゴリー</dt>
                  <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                    <div className="flex flex-wrap">
                      {mechanism.categories.map((category) => (
                        <span
                          key={category}
                          className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800 mr-2 mb-2"
                        >
                          {category}
                        </span>
                      ))}
                    </div>
                  </dd>
                </div>
                <div className="bg-white px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                  <dt className="text-sm font-medium text-gray-500">説明</dt>
                  <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                    {mechanism.description}
                  </dd>
                </div>
                <div className="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                  <dt className="text-sm font-medium text-gray-500">ファイル</dt>
                  <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                    <div className="border border-gray-200 rounded-md p-4 bg-white">
                      <div className="h-64 flex items-center justify-center bg-gray-100 rounded">
                        {mechanism.file_path && mechanism.file_path.match(/\.(jpeg|jpg|gif|png)$/i) ? (
                          <img 
                            src={getFileUrl(mechanism.file_path)} 
                            alt="メカニズムファイル" 
                            className="max-h-full max-w-full object-contain"
                          />
                        ) : (
                          <p className="text-gray-500">ファイルプレビュー（画像以外のファイル）</p>
                        )}
                      </div>
                      <div className="mt-4 flex space-x-2">
                        <a
                          href={getFileUrl(mechanism.file_path)}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                        >
                          ファイルを表示
                        </a>
                        <a
                          href="#"
                          onClick={handleDownload}
                          className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
                        >
                          ダウンロード
                        </a>
                      </div>
                    </div>
                  </dd>
                </div>
                <div className="bg-white px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                  <dt className="text-sm font-medium text-gray-500">投稿日時</dt>
                  <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                    {new Date(mechanism.created_at).toLocaleString('ja-JP')}
                  </dd>
                </div>
                <div className="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                  <dt className="text-sm font-medium text-gray-500">更新日時</dt>
                  <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                    {new Date(mechanism.updated_at).toLocaleString('ja-JP')}
                  </dd>
                </div>
                <div className="bg-white px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                  <dt className="text-sm font-medium text-gray-500">閲覧回数</dt>
                  <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                    <div className="flex flex-col">
                      <span>総閲覧回数: {viewsCount.total}</span>
                      {viewsCount.user !== undefined && (
                        <span className="text-gray-600 text-xs mt-1">
                          あなたの閲覧回数: {viewsCount.user}
                        </span>
                      )}
                    </div>
                  </dd>
                </div>
                <div className="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                  <dt className="text-sm font-medium text-gray-500">ダウンロード回数</dt>
                  <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                    <div className="flex flex-col">
                      <span>総ダウンロード回数: {downloadsCount.total}</span>
                      {downloadsCount.user !== undefined && (
                        <span className="text-gray-600 text-xs mt-1">
                          あなたのダウンロード回数: {downloadsCount.user}
                        </span>
                      )}
                    </div>
                  </dd>
                </div>
              </dl>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default MechanismDetailPage;
