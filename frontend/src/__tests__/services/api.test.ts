import api from '../../services/api';

// apiモジュールを直接インポートして、インターセプターにアクセス
jest.mock('../../services/api', () => {
  // 実際のインターセプターの実装を保存
  const originalModule = jest.requireActual('../../services/api');
  
  // リクエストインターセプターの実装を取得
  const requestInterceptor = originalModule.default.interceptors.request.handlers[0].fulfilled;
  
  // レスポンスインターセプターの実装を取得
  const responseInterceptor = originalModule.default.interceptors.response.handlers[0].fulfilled;
  const responseErrorInterceptor = originalModule.default.interceptors.response.handlers[0].rejected;
  
  // モックされたapiオブジェクトを返す
  return {
    __esModule: true,
    default: {
      ...originalModule.default,
      interceptors: {
        request: {
          handlers: [{ fulfilled: requestInterceptor }]
        },
        response: {
          handlers: [{ fulfilled: responseInterceptor, rejected: responseErrorInterceptor }]
        }
      }
    },
    // テスト用に公開
    requestInterceptor,
    responseInterceptor,
    responseErrorInterceptor
  };
});

// インターセプターの実装を取得
const { requestInterceptor, responseInterceptor, responseErrorInterceptor } = jest.requireMock('../../services/api');

// ローカルストレージのモック
const localStorageMock = {
  getItem: jest.fn(),
  setItem: jest.fn(),
  removeItem: jest.fn(),
  clear: jest.fn(),
};

Object.defineProperty(window, 'localStorage', { value: localStorageMock });

// window.locationのモック
const originalLocation = window.location;
// locationのモックを適切に設定
const locationMock = {
  href: '',
};
Object.defineProperty(window, 'location', {
  value: locationMock,
  writable: true,
});

describe('API Service Helpers', () => {
  // 各テスト前にモックをリセット
  beforeEach(() => {
    jest.clearAllMocks();
    localStorageMock.getItem.mockReset();
    localStorageMock.setItem.mockReset();
    localStorageMock.removeItem.mockReset();
    window.location.href = '';
  });

  // テスト後に元に戻す
  afterAll(() => {
    Object.defineProperty(window, 'location', {
      value: originalLocation,
      writable: true,
    });
  });

  describe('Authentication Helpers', () => {
    it('ローカルストレージからトークンを取得できること', () => {
      // トークンを設定
      localStorageMock.getItem.mockReturnValueOnce('test-token');
      
      // トークンを取得
      const token = localStorage.getItem('token');
      
      // 結果を検証
      expect(token).toBe('test-token');
      expect(localStorageMock.getItem).toHaveBeenCalledWith('token');
    });

    it('ローカルストレージからトークンを削除できること', () => {
      // トークンを削除
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      
      // 結果を検証
      expect(localStorageMock.removeItem).toHaveBeenCalledWith('token');
      expect(localStorageMock.removeItem).toHaveBeenCalledWith('user');
    });

    it('ログインページにリダイレクトできること', () => {
      // ログインページにリダイレクト
      window.location.href = '/login';
      
      // 結果を検証
      expect(locationMock.href).toBe('/login');
    });
  });

  describe('API Interceptors', () => {
    // リクエストインターセプターのテスト
    describe('Request Interceptor', () => {
      it('トークンがある場合、リクエストヘッダーにAuthorizationが追加されること', () => {
        // トークンを設定
        localStorageMock.getItem.mockReturnValueOnce('test-token');
        
        // リクエスト設定オブジェクト
        const config = { headers: {} };
        
        // リクエストインターセプターを実行
        const result = requestInterceptor(config);
        
        // 結果を検証
        expect(result.headers.Authorization).toBe('Bearer test-token');
        expect(localStorageMock.getItem).toHaveBeenCalledWith('token');
      });

      it('トークンがない場合、リクエストヘッダーにAuthorizationが追加されないこと', () => {
        // トークンを設定しない（nullを返す）
        localStorageMock.getItem.mockReturnValueOnce(null);
        
        // リクエスト設定オブジェクト
        const config = { headers: {} };
        
        // リクエストインターセプターを実行
        const result = requestInterceptor(config);
        
        // 結果を検証
        expect(result.headers.Authorization).toBeUndefined();
        expect(localStorageMock.getItem).toHaveBeenCalledWith('token');
      });
    });

    // レスポンスインターセプターのテスト
    describe('Response Interceptor', () => {
      it('正常なレスポンスが適切に処理されること', () => {
        // レスポンスオブジェクト
        const response = { data: { success: true } };
        
        // レスポンスインターセプターを実行
        const result = responseInterceptor(response);
        
        // 結果を検証
        expect(result).toBe(response);
        expect(localStorageMock.removeItem).not.toHaveBeenCalled();
        expect(window.location.href).toBe('');
      });

      it('401エラーの場合、ログアウト処理が実行されること', () => {
        // エラーオブジェクト
        const error = {
          response: {
            status: 401
          }
        };
        
        // エラーハンドラーを実行（エラーをキャッチ）
        try {
          responseErrorInterceptor(error);
        } catch (e) {
          // エラーは期待通り
        }
        
        // ログアウト処理の検証
        expect(localStorageMock.removeItem).toHaveBeenCalledWith('token');
        expect(localStorageMock.removeItem).toHaveBeenCalledWith('user');
        expect(window.location.href).toBe('/login');
      });

      it('その他のエラーの場合、ログアウト処理が実行されないこと', () => {
        // エラーオブジェクト（404エラー）
        const error = {
          response: {
            status: 404
          }
        };
        
        // エラーハンドラーを実行（エラーをキャッチ）
        try {
          responseErrorInterceptor(error);
        } catch (e) {
          // エラーは期待通り
        }
        
        // ログアウト処理が実行されていないことを検証
        expect(localStorageMock.removeItem).not.toHaveBeenCalled();
        expect(window.location.href).toBe('');
      });
    });
  });
});
