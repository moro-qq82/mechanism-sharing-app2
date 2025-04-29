import React from 'react';
import { getReliabilityLabel, getReliabilityColorClass } from '../utils/reliabilityUtils';

const MechanismDetailPage: React.FC = () => {
  // 仮のメカニズム詳細データ
  const mechanism = {
    id: 1,
    title: 'サンプルメカニズム',
    description: 'これはサンプルメカニズムの詳細な説明です。メカニズムの動作原理や特徴について詳しく解説しています。このメカニズムは様々な用途に活用できます。',
    reliability: 3,
    filePath: '/files/sample.pdf',
    thumbnailPath: '/placeholder.jpg',
    user: {
      id: 1,
      email: 'user@example.com'
    },
    categories: ['機械', '電子'],
    likesCount: 5,
    createdAt: '2025-04-25T14:30:00Z',
    updatedAt: '2025-04-25T14:30:00Z'
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center">
            <h1 className="text-3xl font-bold text-gray-900">{mechanism.title}</h1>
            <a
              href="/"
              className="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              一覧に戻る
            </a>
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
                  <button className="inline-flex items-center px-3 py-1 border border-transparent text-sm font-medium rounded-md text-white bg-pink-600 hover:bg-pink-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-pink-500">
                    いいね {mechanism.likesCount}
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
                        <p className="text-gray-500">ファイルプレビュー</p>
                      </div>
                      <div className="mt-4">
                        <a
                          href={mechanism.filePath}
                          className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                        >
                          ファイルを表示
                        </a>
                      </div>
                    </div>
                  </dd>
                </div>
                <div className="bg-white px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                  <dt className="text-sm font-medium text-gray-500">投稿日時</dt>
                  <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                    {new Date(mechanism.createdAt).toLocaleString('ja-JP')}
                  </dd>
                </div>
                <div className="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                  <dt className="text-sm font-medium text-gray-500">更新日時</dt>
                  <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                    {new Date(mechanism.updatedAt).toLocaleString('ja-JP')}
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
