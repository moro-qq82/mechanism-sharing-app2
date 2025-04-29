/**
 * 信頼性レベルを数値から文字列に変換する関数
 * @param level 信頼性レベル（1-5）
 * @returns 信頼性レベルの文字列表現
 */
export const getReliabilityLabel = (level: number): string => {
  switch (level) {
    case 1:
      return '妄想モデル';
    case 2:
      return '実験により一部支持';
    case 3:
      return '社内複数人が支持';
    case 4:
      return '顧客含めて定番認識化';
    case 5:
      return '教科書に記載';
    default:
      return `不明なレベル: ${level}`;
  }
};

/**
 * 信頼性レベルに応じた背景色とテキスト色のクラス名を返す関数
 * @param level 信頼性レベル（1-5）
 * @returns テールウィンドCSSのクラス名
 */
export const getReliabilityColorClass = (level: number): string => {
  switch (level) {
    case 1:
      return 'bg-gray-100 text-gray-800'; // 妄想モデル: グレー
    case 2:
      return 'bg-blue-100 text-blue-800'; // 実験により一部支持: ブルー
    case 3:
      return 'bg-yellow-100 text-yellow-800'; // 社内複数人が支持: イエロー
    case 4:
      return 'bg-green-100 text-green-800'; // 顧客含めて定番認識化: グリーン
    case 5:
      return 'bg-purple-100 text-purple-800'; // 教科書に記載: パープル
    default:
      return 'bg-gray-100 text-gray-800'; // デフォルト: グレー
  }
};
