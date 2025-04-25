import React from 'react';

const MechanismListPage: React.FC = () => {
  // 仮のメカニズムデータ
  const mechanisms = [
    {
      id: 1,
      title: 'サンプルメカニズム1',
      description: 'これはサンプルメカニズムの説明です。',
      reliability: 3,
      thumbnailPath: '/placeholder.jpg',
      categories: ['機械', '電子'],
      likesCount: 5,
      createdAt: '2025-04-25T14:30:00Z',
    },
    {
      id: 2,
      title: 'サンプルメカニズム2',
      description: 'これは別のサンプルメカニズムの説明です。',
      reliability: 4,
      thumbnailPath: '/placeholder.jpg',
      categories: ['機械'],
      likesCount: 3,
      createdAt: '2025-04-24T10:15:00Z',
    },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8 flex justify-between items-center">
          <h1 className="text-3xl font-bold text-gray-900">メカニズム一覧</h1>
          <div>
            <a
              href="/mechanisms/new"
              className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              新規投稿
            </a>
          </div>
        </div>
      </header>
      <main>
        <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {mechanisms.map((mechanism) => (
              <div
                key={mechanism.id}
                className="bg-white overflow-hidden shadow rounded-lg"
              >
                <div className="p-5">
                  <div className="flex items-center">
                    <div className="flex-shrink-0">
                      <div className="h-48 w-full bg-gray-200 rounded-md"></div>
                    </div>
                  </div>
                  <div className="mt-4">
                    <h3 className="text-lg font-medium text-gray-900">
                      <a href={`/mechanisms/${mechanism.id}`} className="hover:underline">
                        {mechanism.title}
                      </a>
                    </h3>
                    <p className="mt-2 text-sm text-gray-500 line-clamp-2">
                      {mechanism.description}
                    </p>
                    <div className="mt-3 flex items-center">
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800 mr-2">
                        信頼性: {mechanism.reliability}
                      </span>
                      {mechanism.categories.map((category) => (
                        <span
                          key={category}
                          className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800 mr-2"
                        >
                          {category}
                        </span>
                      ))}
                    </div>
                    <div className="mt-3 flex items-center text-sm text-gray-500">
                      <span>いいね {mechanism.likesCount}件</span>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </main>
    </div>
  );
};

export default MechanismListPage;
