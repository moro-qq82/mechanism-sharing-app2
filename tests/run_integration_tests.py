import os
import sys
import pytest

def main():
    """
    統合テストを実行するメイン関数
    """
    print("メカニズム共有プラットフォーム 統合テストを実行します...")
    
    # テストディレクトリのパスを取得
    test_dir = os.path.dirname(os.path.abspath(__file__))
    integration_dir = os.path.join(test_dir, "integration")
    
    # 統合テストを実行
    args = [
        "-v",  # 詳細なテスト結果を表示
        integration_dir,  # テストディレクトリ
        "--tb=native",  # トレースバックの形式
    ]
    
    # コマンドライン引数があれば追加
    if len(sys.argv) > 1:
        args.extend(sys.argv[1:])
    
    # pytestを実行
    result = pytest.main(args)
    
    # 結果に応じて終了コードを設定
    sys.exit(result)

if __name__ == "__main__":
    main()
