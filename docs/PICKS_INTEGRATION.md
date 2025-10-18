# TERASS Picks 統合ガイド

## 概要

TERASS Picksは、複数の不動産ポータルサイトを統合検索し、顧客に最適な物件を提案するためのシステムです。このドキュメントでは、TERASS Picksの機能、使用方法、および報酬計算との連携について説明します。

---

## 1. TERASS Picks とは

### 1.1 定義
TERASS Picksは、以下の主要不動産ポータルサイトを統合検索するシステムです：
- **SUUMO**（スーモ）
- **at HOME**（アットホーム）
- **REINS**（レインズ：東日本・中部・西日本・近畿）

### 1.2 目的
- 複数ポータルの効率的な検索
- 顧客ニーズに最適な物件の発見
- 自己発見案件としての報酬率向上（75-90%）
- エージェントの営業効率化

---

## 2. 主要機能

### 2.1 統合検索機能

#### 検索パラメータ
```python
search_params = {
    "area": "埼玉県",           # 地域
    "price_min": 2000,          # 最低価格（万円）
    "price_max": 3500,          # 最高価格（万円）
    "property_type": "マンション",  # 物件タイプ
    "rooms": "3LDK以上",        # 間取り
    "age": "築10年以内"         # 築年数
}
```

#### 対応ポータル
1. **SUUMO**
   - 最大の物件掲載数
   - 詳細な条件検索
   - 写真・動画コンテンツ充実

2. **at HOME**
   - 不動産業者向け情報が豊富
   - 正確な物件情報
   - 更新頻度が高い

3. **REINS（レインズ）**
   - 不動産業者専用データベース
   - 最新の売買情報
   - 地域別に4つのREINS
     - 東日本REINS
     - 中部REINS
     - 西日本REINS
     - 近畿REINS

### 2.2 リアクション機能

顧客の反応を記録し、提案の精度を向上させます。

#### リアクションタイプ
- 👍 興味あり
- ❤️ お気に入り
- 📋 詳細確認希望
- 👀 内見希望
- ❌ 対象外

#### リアクションの活用
```python
# リアクションデータの分析
customer_preferences = {
    "liked_properties": [...],      # お気に入り物件
    "viewed_properties": [...],     # 閲覧した物件
    "preferred_area": "埼玉県南部",  # 好みエリア
    "preferred_price": 3000,        # 希望価格帯
}
```

### 2.3 Terass Offer との比較

#### Terass Offer との違い
| 項目 | TERASS Picks | Terass Offer |
|------|--------------|--------------|
| 報酬率 | 75-90% | 55% |
| 案件分類 | 自己発見 | 特別案件 |
| 物件ソース | 一般ポータル | TERASS独自 |
| 検索範囲 | 全国・全ポータル | TERASS提携物件 |

#### 使い分けガイド
1. **TERASS Picks を優先すべきケース**
   - 顧客の希望条件が明確
   - 幅広い選択肢を提示したい
   - 報酬率を最大化したい

2. **Terass Offer を活用すべきケース**
   - TERASS独自の特別物件がある
   - 迅速な成約が必要
   - 確実性を重視する場合

---

## 3. 使用方法

### 3.1 基本的な検索フロー

```
1. 顧客ヒアリング
   ↓
2. TERASS Picks で検索
   ↓
3. 候補物件の抽出（複数ポータル統合）
   ↓
4. 顧客に提案
   ↓
5. リアクション記録
   ↓
6. 追加検索・提案調整
   ↓
7. 内見・契約サポート
```

### 3.2 CLIでの使用例

```bash
# TERASS Picks 検索の開始
python src/cli/main.py start

# メニューから選択
> 3. 🏠 物件提案
> 1. TERASS Picks活用

# 検索条件の入力
> 地域: 埼玉県
> 予算: 2000-3500万円
> 間取り: 3LDK以上
```

### 3.3 Python APIでの使用例

```python
from src.engine.picks_integration import TERassPicksSearch

# 検索インスタンスの作成
picks = TERassPicksSearch()

# 検索実行
results = picks.search(
    area="埼玉県",
    price_range=(2000, 3500),
    property_type="マンション",
    rooms="3LDK以上"
)

# 結果の取得
for property in results:
    print(f"物件名: {property['name']}")
    print(f"価格: {property['price']}万円")
    print(f"所在地: {property['location']}")
    print(f"ポータル: {property['source']}")
```

---

## 4. 報酬計算との連携

### 4.1 自己発見案件としての扱い

TERASS Picksで発見した物件は**自己発見案件**として扱われます。

#### 報酬率
- **通常**: 75%
- **ボーナスステージ**: 90%（年度累計2,000万円達成後）

### 4.2 報酬計算例

```python
# 例: TERASS Picksで発見した物件の成約
仲介手数料 = 3,000,000円（税抜）
年度累計 = 18,000,000円

# ボーナスステージ未達成
報酬 = 3,000,000 × 0.75 = 2,250,000円

# ボーナスステージ達成後（年度累計20,000,000円以上）
報酬 = 3,000,000 × 0.90 = 2,700,000円
```

### 4.3 ボーナスステージへの貢献

TERASS Picksを活用することで：
- 高い報酬率（75-90%）を獲得
- 年度累計2,000万円の早期達成
- ボーナスステージへの移行促進

---

## 5. 最適化のためのベストプラクティス

### 5.1 効率的な検索

#### 検索条件の設定
1. **広すぎる条件を避ける**
   - ❌ 悪い例: 「東京都、予算500-10,000万円」
   - ✅ 良い例: 「世田谷区、予算3,000-4,000万円、3LDK」

2. **顧客ニーズの明確化**
   - 通勤先・通学先
   - ライフスタイル
   - 優先条件（価格 vs 立地 vs 広さ）

3. **段階的な条件緩和**
   - 第1段階: 全条件で検索
   - 第2段階: 優先度の低い条件を緩和
   - 第3段階: 隣接エリアも含める

### 5.2 顧客対応

#### 提案のポイント
1. **複数の選択肢を提示**（3-5件程度）
2. **各物件の特徴を明確に説明**
3. **顧客の反応を記録**
4. **フォローアップの実施**

#### コミュニケーション
```
例: 顧客への提案メッセージ

「○○様

ご希望条件に基づき、TERASS Picksで物件を検索いたしました。
以下の3件が特におすすめです：

1. [物件A] - 駅近、新築、予算内
2. [物件B] - 広めのリビング、学校近い
3. [物件C] - コストパフォーマンス良好

それぞれの詳細をお送りしますので、
ご興味のある物件をお知らせください。

内見のご希望もお気軽にどうぞ。」
```

### 5.3 リアクションデータの活用

```python
# 顧客の好みパターンを分析
def analyze_customer_preferences(reactions):
    """
    顧客のリアクションから好みを分析
    """
    liked_properties = filter_liked(reactions)
    
    # 共通パターンの抽出
    common_features = extract_common_features(liked_properties)
    
    return {
        "preferred_area": common_features['area'],
        "preferred_price": common_features['price_range'],
        "preferred_type": common_features['property_type'],
        "must_have": common_features['features']
    }
```

---

## 6. トラブルシューティング

### 6.1 よくある問題

#### 問題1: 検索結果が0件
**原因**
- 検索条件が厳しすぎる
- 対象エリアに該当物件がない

**解決策**
```python
# 段階的に条件を緩和
1. 価格範囲を10%拡大
2. 築年数条件を緩和
3. 隣接エリアを含める
```

#### 問題2: 検索に時間がかかる
**原因**
- 複数ポータルの同時検索による負荷
- ネットワーク遅延

**解決策**
- ポータルを絞り込んで検索
- キャッシュ機能の活用

#### 問題3: 物件情報が古い
**原因**
- ポータルの更新タイミング
- キャッシュデータの使用

**解決策**
- 最新情報の再取得
- ポータル直接確認

---

## 7. 統合APIリファレンス

### 7.1 主要クラスとメソッド

```python
class TERassPicksSearch:
    """TERASS Picks 統合検索クラス"""
    
    def search(self, **criteria):
        """
        物件検索
        
        Parameters:
            area (str): 検索エリア
            price_range (tuple): 価格範囲 (最小, 最大)
            property_type (str): 物件タイプ
            rooms (str): 間取り
            
        Returns:
            list: 検索結果の物件リスト
        """
        pass
    
    def add_reaction(self, property_id, reaction_type):
        """
        物件へのリアクション記録
        
        Parameters:
            property_id (str): 物件ID
            reaction_type (str): リアクションタイプ
        """
        pass
    
    def get_recommendations(self, customer_id):
        """
        顧客向けおすすめ物件の取得
        
        Parameters:
            customer_id (str): 顧客ID
            
        Returns:
            list: おすすめ物件リスト
        """
        pass
```

---

## 8. まとめ

TERASS Picksは、エージェントの営業活動を強力に支援するツールです。

### 活用のポイント
1. **自己発見案件として高報酬率（75-90%）**
2. **複数ポータルの統合検索で効率化**
3. **顧客のリアクションを活用した提案精度向上**
4. **Terass Offerとの適切な使い分け**

### 推奨アクション
- 毎日の物件検索でTERASS Picksを活用
- 顧客のフィードバックを記録
- 報酬シミュレーションで目標管理
- ボーナスステージの早期達成を目指す

---

## 9. 関連ドキュメント

- [TERASS-ADVISER_SPEC.md](./TERASS-ADVISER_SPEC.md) - システム全体仕様
- [LOAN_CHECKER.md](./LOAN_CHECKER.md) - 住宅ローン提案システム
- [報酬計算エンジン](../src/engine/reward_calculator.py) - 報酬計算実装

---

## 10. 更新履歴

- **2025年10月18日**: 初版リリース
- **対応バージョン**: TERASS-ADVISER v1.0.0

---

TERASS Picksを最大限に活用して、効率的な営業活動と高い報酬率を実現しましょう！
