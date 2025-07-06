import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import MechanismService from '../services/mechanismService';
import { Mechanism, PaginatedMechanismResponse, MechanismDownloadCount } from '../types/mechanism';
import { getReliabilityLabel, getReliabilityColorClass } from '../utils/reliabilityUtils';
import { getFileUrl } from '../utils/fileUtils';
import Loading from '../components/common/Loading';
import Pagination from '../components/common/Pagination';

const MechanismListPage: React.FC = () => {
  // 状態管理
  const [mechanisms, setMechanisms] = useState<Mechanism[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [pagination, setPagination] = useState({
    total: 0,
    page: 1,
    limit: 9,
    pages: 0
  });
  const [downloadsCountMap, setDownloadsCountMap] = useState<Record<number, number>>({});

  // メカニズム一覧を取得する関数
  const fetchMechanisms = async (page: number = 1) => {
    try {
      setLoading(true);
      const response: PaginatedMechanismResponse = await MechanismService.getMechanisms(page, pagination.limit);
      setMechanisms(response.items);
      setPagination({
        total: response.total,
        page: response.page,
        limit: response.limit,
        pages: response.pages
      });
      
      // ダウンロード回数を一括取得
      if (response.items.length > 0) {
        const mechanismIds = response.items.map(mechanism => mechanism.id);
        try {
          const downloadsResponse = await MechanismService.getMechanismsDownloads(mechanismIds);
          const downloadsMap: Record<number, number> = {};
          downloadsResponse.items.forEach((item: MechanismDownloadCount) => {
            downloadsMap[item.mechanism_id] = item.total_downloads;
          });
          setDownloadsCountMap(downloadsMap);
        } catch (downloadErr) {
          console.error('ダウンロード回数の取得エラー:', downloadErr);
          // ダウンロード回数の取得に失敗してもメカニズム一覧は表示する
        }
      }
      
      setError(null);
    } catch (err) {
      setError('メカニズム一覧の取得に失敗しました。');
      console.error('メカニズム一覧の取得エラー:', err);
    } finally {
      setLoading(false);
    }
  };

  // ページ変更時の処理
  const handlePageChange = (newPage: number) => {
    fetchMechanisms(newPage);
  };

  // コンポーネントマウント時にメカニズム一覧を取得
  useEffect(() => {
    fetchMechanisms();
  }, []);

  // ローディング中の表示
  if (loading && mechanisms.length === 0) {
    return (
      <div className="min-h-screen bg-gray-50 flex justify-center items-center">
        <Loading />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8 flex justify-between items-center">
          <h1 className="text-3xl font-bold text-gray-900">メカニズム一覧</h1>
          <div>
            <Link
              to="/mechanisms/new"
              className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              新規投稿
            </Link>
          </div>
        </div>
      </header>
      <main>
        <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
          {/* エラーメッセージ */}
          {error && (
            <div className="mb-6 bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
              <span className="block sm:inline">{error}</span>
            </div>
          )}
          
          {/* メカニズム一覧 */}
          {mechanisms.length > 0 ? (
            <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
              {mechanisms.map((mechanism) => (
                <Link
                  to={`/mechanisms/${mechanism.id}`}
                  key={mechanism.id}
                  className="block bg-white overflow-hidden shadow rounded-lg transition-transform duration-300 hover:shadow-lg hover:-translate-y-1 cursor-pointer"
                >
                  <div className="p-5">
                    <div className="flex items-center">
                      <div className="flex-shrink-0 w-full">
                        {mechanism.thumbnail_path ? (
                          <img 
                            src={getFileUrl(mechanism.thumbnail_path)} 
                            alt={mechanism.title} 
                            className="h-48 w-full object-cover rounded-md"
                          />
                        ) : (
                          <div className="h-48 w-full bg-gray-200 rounded-md flex items-center justify-center">
                            <span className="text-gray-400">No Image</span>
                          </div>
                        )}
                      </div>
                    </div>
                    <div className="mt-4">
                      <h3 className="text-lg font-medium text-gray-900">
                        {mechanism.title}
                      </h3>
                      <p className="mt-2 text-sm text-gray-500 line-clamp-2">
                        {mechanism.description}
                      </p>
                      <div className="mt-3 flex flex-wrap gap-2">
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getReliabilityColorClass(mechanism.reliability)}`}>
                          {getReliabilityLabel(mechanism.reliability)}
                        </span>
                        {mechanism.categories.map((category) => (
                          <span
                            key={category}
                            className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
                          >
                            {category}
                          </span>
                        ))}
                      </div>
                      <div className="mt-3 flex items-center justify-between">
                        <div className="flex space-x-2">
                          {mechanism.views_count !== undefined && (
                            <span className="text-sm text-gray-500">
                              閲覧<br />{mechanism.views_count}回
                            </span>
                          )}
                          <span className="text-sm text-gray-500">
                            いいね<br />{mechanism.likes_count}件
                          </span>
                          <span className="text-sm text-gray-500">
                            ダウンロード<br />{downloadsCountMap[mechanism.id] || 0}回
                          </span>
                        </div>
                        <span className="text-xs text-gray-400">
                          {new Date(mechanism.created_at).toLocaleDateString('ja-JP')}
                        </span>
                      </div>
                    </div>
                  </div>
                </Link>
              ))}
            </div>
          ) : !loading && (
            <div className="text-center py-10">
              <p className="text-gray-500">メカニズムがありません。新しいメカニズムを投稿してみましょう。</p>
            </div>
          )}
          
          {/* ページネーション */}
          {pagination.pages > 1 && (
            <div className="mt-8 flex justify-center">
              <Pagination 
                currentPage={pagination.page} 
                totalPages={pagination.pages} 
                onPageChange={handlePageChange} 
              />
            </div>
          )}
        </div>
      </main>
    </div>
  );
};

export default MechanismListPage;
