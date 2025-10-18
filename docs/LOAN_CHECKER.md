# Loan Checker - 住宅ローン最適提案システム

## 概要

Loan Checkerは、107の金融機関に対応した住宅ローン最適提案システムです。顧客の条件に最適な住宅ローンを提案し、エージェントの営業活動を支援します。

---

## 1. システム概要

### 1.1 目的
- 顧客に最適な住宅ローンの提案
- 107行の金融機関データベース対応
- 金利比較とシミュレーション
- 審査通過可能性の判定

### 1.2 対応金融機関
- **都市銀行**: 5行
- **地方銀行**: 64行
- **信用金庫**: 26組織
- **ネット銀行**: 8行
- **その他金融機関**: 4行

合計: **107金融機関**

---

## 2. 金利情報

### 2.1 金利範囲
- **最低金利**: 0.520%（変動金利）
- **最高金利**: 3.242%（固定金利）
- **平均金利**: 約1.2-1.5%

### 2.2 金利タイプ

#### 変動金利
- 金利水準: 0.520% - 1.475%
- 特徴:
  - 金利が低い
  - 市場金利に連動
  - 半年ごとに見直し

#### 固定金利
##### 固定期間選択型
- 10年固定: 1.200% - 2.100%
- 20年固定: 1.800% - 2.800%
- 35年固定: 2.000% - 3.242%

##### 全期間固定型
- フラット35: 1.850% - 2.450%
- 特徴:
  - 返済終了まで金利固定
  - 長期的な返済計画が立てやすい

---

## 3. 主要機能

### 3.1 金利検索

#### 検索パラメータ
```python
loan_search_params = {
    "loan_amount": 30000000,        # 借入金額（円）
    "loan_period": 35,              # 返済期間（年）
    "interest_type": "変動",         # 金利タイプ
    "customer_profile": {
        "age": 35,                  # 年齢
        "annual_income": 6000000,   # 年収（円）
        "employment": "正社員",      # 雇用形態
        "work_years": 5,            # 勤続年数
    }
}
```

#### 検索結果
```python
search_results = [
    {
        "bank_name": "○○銀行",
        "interest_rate": 0.520,
        "interest_type": "変動",
        "monthly_payment": 77000,
        "total_payment": 32340000,
        "total_interest": 2340000,
        "approval_possibility": "高"
    },
    # ... 他の検索結果
]
```

### 3.2 返済シミュレーション

#### 月々の返済額計算
```python
def calculate_monthly_payment(loan_amount, annual_rate, years):
    """
    月々の返済額を計算
    
    Parameters:
        loan_amount (int): 借入金額
        annual_rate (float): 年利率（%）
        years (int): 返済期間（年）
        
    Returns:
        int: 月々の返済額
    """
    monthly_rate = annual_rate / 100 / 12
    months = years * 12
    
    if monthly_rate == 0:
        return loan_amount / months
    
    monthly_payment = loan_amount * (
        monthly_rate * (1 + monthly_rate) ** months
    ) / (
        (1 + monthly_rate) ** months - 1
    )
    
    return int(monthly_payment)
```

#### 総返済額の計算
```python
total_payment = monthly_payment × 返済期間（月数）
total_interest = total_payment - loan_amount
```

### 3.3 審査通過可能性判定

#### 判定基準
1. **返済負担率**
   ```python
   返済負担率 = (年間返済額 / 年収) × 100
   
   # 基準
   - 25%以下: 高い審査通過可能性
   - 25-35%: 普通
   - 35%以上: 審査が厳しい
   ```

2. **勤続年数**
   - 3年以上: 有利
   - 1-3年: 普通
   - 1年未満: 不利

3. **雇用形態**
   - 正社員・公務員: 有利
   - 契約社員: 普通
   - 自営業・フリーランス: 審査基準が異なる

4. **信用情報**
   - クレジットヒストリー
   - 他のローン状況
   - 延滞履歴の有無

---

## 4. 金融機関データベース

### 4.1 主要銀行の金利例

#### 都市銀行
| 銀行名 | 変動金利 | 10年固定 | 35年固定 |
|--------|----------|----------|----------|
| 三菱UFJ銀行 | 0.625% | 1.350% | 2.050% |
| 三井住友銀行 | 0.675% | 1.400% | 2.100% |
| みずほ銀行 | 0.625% | 1.450% | 2.150% |
| りそな銀行 | 0.695% | 1.495% | 2.200% |

#### ネット銀行
| 銀行名 | 変動金利 | 10年固定 | 特徴 |
|--------|----------|----------|------|
| 住信SBIネット銀行 | 0.520% | 1.200% | 業界最低水準 |
| 楽天銀行 | 0.650% | 1.350% | 楽天ポイント付与 |
| auじぶん銀行 | 0.580% | 1.280% | がん保障付き |
| ソニー銀行 | 0.697% | 1.450% | 外貨預金連携 |

#### 地方銀行（抜粋）
| 銀行名 | 変動金利 | 10年固定 | 営業エリア |
|--------|----------|----------|-----------|
| 横浜銀行 | 0.700% | 1.500% | 神奈川県中心 |
| 千葉銀行 | 0.725% | 1.525% | 千葉県中心 |
| 福岡銀行 | 0.750% | 1.550% | 福岡県中心 |
| 静岡銀行 | 0.725% | 1.500% | 静岡県中心 |

### 4.2 データ更新頻度
- **月次更新**: 金利情報
- **四半期更新**: 審査基準情報
- **随時更新**: 新商品情報

---

## 5. 使用方法

### 5.1 CLIでの使用

```bash
# Loan Checker の起動
python src/cli/main.py start

# メニューから選択
> 4. 💳 住宅ローン
> 1. 107銀行検索

# 条件入力
> 借入金額: 3000万円
> 返済期間: 35年
> 金利タイプ: 変動
> 年収: 600万円
> 年齢: 35歳
```

### 5.2 Python APIでの使用

```python
from src.engine.loan_checker import LoanChecker

# Loan Checkerインスタンス作成
checker = LoanChecker()

# 顧客情報の設定
customer = {
    "age": 35,
    "annual_income": 6000000,
    "employment": "正社員",
    "work_years": 5,
}

# 最適ローンの検索
recommendations = checker.search_optimal_loans(
    loan_amount=30000000,
    loan_period=35,
    interest_type="変動",
    customer_profile=customer
)

# 結果の表示
for loan in recommendations:
    print(f"銀行: {loan['bank_name']}")
    print(f"金利: {loan['interest_rate']}%")
    print(f"月々返済額: {loan['monthly_payment']:,}円")
    print(f"審査可能性: {loan['approval_possibility']}")
    print("---")
```

---

## 6. 提案ロジック

### 6.1 最適ローン選定の優先順位

```python
def prioritize_loans(loans, customer_profile):
    """
    顧客に最適なローンを優先順位付け
    
    優先順位:
    1. 審査通過可能性
    2. 総返済額
    3. 月々返済額
    4. 金融機関の信頼性
    """
    scored_loans = []
    
    for loan in loans:
        score = 0
        
        # 審査通過可能性（40点満点）
        if loan['approval_possibility'] == '高':
            score += 40
        elif loan['approval_possibility'] == '中':
            score += 25
        else:
            score += 10
        
        # 金利の低さ（30点満点）
        rate_score = max(0, 30 - (loan['interest_rate'] * 10))
        score += rate_score
        
        # 総返済額の低さ（20点満点）
        # 最低総返済額を基準にスコアリング
        # ...
        
        # 金融機関の信頼性（10点満点）
        # 都市銀行: 10点、地方銀行: 8点、ネット銀行: 6点
        # ...
        
        scored_loans.append((score, loan))
    
    # スコア順にソート
    scored_loans.sort(reverse=True, key=lambda x: x[0])
    
    return [loan for score, loan in scored_loans]
```

### 6.2 顧客別提案パターン

#### パターン1: 若年・高収入
- **特徴**: 年齢30代、年収800万円以上
- **推奨**: 変動金利で低金利追求
- **理由**: 長期的な収入増加が見込める

#### パターン2: 中年・安定収入
- **特徴**: 年齢40代、年収600万円前後
- **推奨**: 10-20年固定金利
- **理由**: リスクとコストのバランス重視

#### パターン3: シニア層
- **特徴**: 年齢50代以上
- **推奨**: 短期固定または変動金利
- **理由**: 定年後の返済を考慮

#### パターン4: 自営業・フリーランス
- **特徴**: 収入変動あり
- **推奨**: フラット35など全期間固定
- **理由**: 安定した返済計画が重要

---

## 7. 実装例

### 7.1 基本クラス構造

```python
class LoanChecker:
    """住宅ローン最適提案システム"""
    
    def __init__(self):
        self.banks_data = self.load_banks_data()
    
    def load_banks_data(self):
        """
        107金融機関のデータをロード
        """
        # データベースまたはJSONファイルから読み込み
        pass
    
    def search_optimal_loans(self, loan_amount, loan_period, 
                            interest_type, customer_profile):
        """
        最適なローンを検索
        """
        # 検索ロジック実装
        pass
    
    def calculate_payment(self, loan_amount, interest_rate, years):
        """
        返済額を計算
        """
        # 計算ロジック実装
        pass
    
    def assess_approval_possibility(self, loan, customer_profile):
        """
        審査通過可能性を判定
        """
        # 判定ロジック実装
        pass
```

### 7.2 データ構造

```python
# 金融機関データの構造
bank_data = {
    "bank_id": "001",
    "bank_name": "○○銀行",
    "bank_type": "都市銀行",
    "interest_rates": {
        "variable": 0.625,
        "fixed_10y": 1.350,
        "fixed_20y": 1.850,
        "fixed_35y": 2.050,
    },
    "min_loan_amount": 5000000,
    "max_loan_amount": 100000000,
    "min_work_years": 3,
    "service_areas": ["全国"],
    "special_features": [
        "がん保障付き",
        "繰上返済手数料無料"
    ]
}
```

---

## 8. 顧客へのアドバイス

### 8.1 金利タイプ選択のガイド

#### 変動金利を選ぶべき人
- ✅ 金利上昇リスクを受け入れられる
- ✅ 短期間での完済を予定
- ✅ 返済余力がある
- ✅ 今後収入増加が見込める

#### 固定金利を選ぶべき人
- ✅ 金利上昇リスクを避けたい
- ✅ 長期的な返済計画を重視
- ✅ 収入が安定している
- ✅ 家計管理を確実にしたい

### 8.2 返済計画のポイント

1. **頭金の準備**
   - 物件価格の20%以上が理想
   - 頭金が多いほど金利優遇あり

2. **返済期間の設定**
   - 定年までに完済できる期間
   - 子供の教育費を考慮
   - 老後資金を確保

3. **繰上返済の活用**
   - ボーナス時の繰上返済
   - 期間短縮型 vs 返済額軽減型

---

## 9. トラブルシューティング

### 9.1 審査に通らない場合

#### 原因と対策
1. **返済負担率が高い**
   - 対策: 頭金を増やす、返済期間を延長

2. **勤続年数が短い**
   - 対策: 勤続3年を待つ、複数の金融機関を検討

3. **信用情報に問題**
   - 対策: 信用情報の確認と改善、期間をおいて再申請

4. **年齢が高い**
   - 対策: 返済期間を短縮、連帯保証人の検討

### 9.2 金利比較の注意点

#### 表面金利 vs 実質金利
- **表面金利**: 広告で表示される金利
- **実質金利**: 諸費用を含めた実際の負担

```python
# 実質コストの計算例
initial_costs = {
    "事務手数料": 660000,      # 借入額の2.2%
    "保証料": 0,               # フラット35は不要
    "団信保険料": 0,           # 金利に含まれる場合
    "登記費用": 150000,
    "火災保険": 200000,
}

total_cost = loan_amount + sum(initial_costs.values())
```

---

## 10. API リファレンス

### 10.1 主要メソッド

```python
class LoanChecker:
    
    def search_optimal_loans(
        self, 
        loan_amount: int,
        loan_period: int,
        interest_type: str,
        customer_profile: dict
    ) -> List[dict]:
        """最適なローンを検索して返す"""
        pass
    
    def calculate_monthly_payment(
        self,
        loan_amount: int,
        annual_rate: float,
        years: int
    ) -> int:
        """月々の返済額を計算"""
        pass
    
    def assess_approval_possibility(
        self,
        loan_info: dict,
        customer_profile: dict
    ) -> str:
        """審査通過可能性を判定（高/中/低）"""
        pass
    
    def get_bank_info(
        self,
        bank_id: str
    ) -> dict:
        """金融機関の詳細情報を取得"""
        pass
```

---

## 11. まとめ

### 活用のポイント
1. **107金融機関の幅広い選択肢**
2. **顧客条件に最適化された提案**
3. **正確な返済シミュレーション**
4. **審査通過可能性の事前判定**

### 推奨フロー
```
1. 顧客ヒアリング
   ↓
2. Loan Checkerで検索
   ↓
3. 最適3-5行を提案
   ↓
4. 返済シミュレーション提示
   ↓
5. 審査申込サポート
   ↓
6. 契約完了
```

---

## 12. 関連ドキュメント

- [TERASS-ADVISER_SPEC.md](./TERASS-ADVISER_SPEC.md) - システム全体仕様
- [PICKS_INTEGRATION.md](./PICKS_INTEGRATION.md) - 物件検索システム
- [報酬計算エンジン](../src/engine/reward_calculator.py) - 報酬計算実装

---

## 13. 更新履歴

- **2025年10月18日**: 初版リリース
- **対応バージョン**: TERASS-ADVISER v1.0.0
- **金利データ**: 2025年10月時点

---

Loan Checkerを活用して、顧客に最適な住宅ローンを提案し、
成約率の向上と顧客満足度の向上を実現しましょう！
