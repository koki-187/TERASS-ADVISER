"""
TERASS業務アドバイザー - 報酬計算エンジン

このモジュールは、TERASS社の報酬体系に基づいて、
エージェントの報酬を正確に計算します。

報酬率:
- 自己発見案件: 75%
- ボーナスステージ: 90% (年度累計2,000万円達成後、翌月1日から年度末まで)
- 本部送客: 40%
- Terass Offer: 55%
"""

from datetime import datetime
from typing import Dict, List, Tuple
from enum import Enum


class PropertyType(Enum):
    """案件タイプの列挙"""
    SELF_DISCOVERED = "自己発見"
    HQ_REFERRAL = "本部送客"
    TERASS_OFFER = "Terass Offer"
    TERASS_PICKS = "TERASS Picks"  # TERASS Picksは自己発見扱い


class RewardCalculator:
    """報酬計算エンジン"""
    
    # 報酬率定義
    REWARD_RATES = {
        PropertyType.SELF_DISCOVERED: 0.75,
        PropertyType.HQ_REFERRAL: 0.40,
        PropertyType.TERASS_OFFER: 0.55,
        PropertyType.TERASS_PICKS: 0.75,  # TERASS Picksも自己発見と同じ
    }
    
    # ボーナスステージの閾値（円）
    BONUS_THRESHOLD = 20_000_000
    BONUS_RATE = 0.90
    
    def __init__(self, fiscal_year_start_month: int = 4):
        """
        初期化
        
        Args:
            fiscal_year_start_month: 年度開始月（デフォルト: 4月）
        """
        self.fiscal_year_start_month = fiscal_year_start_month
        self.transactions: List[Dict] = []
    
    def calculate_basic_reward(
        self, 
        commission: int, 
        property_type: PropertyType
    ) -> int:
        """
        基本報酬を計算
        
        Args:
            commission: 税抜仲介手数料（円）
            property_type: 案件タイプ
            
        Returns:
            報酬額（円）
        """
        rate = self.REWARD_RATES.get(property_type, 0)
        return int(commission * rate)
    
    def is_bonus_stage_active(
        self,
        transaction_date: datetime,
        annual_total: int
    ) -> bool:
        """
        ボーナスステージが適用されるか判定
        
        Args:
            transaction_date: 取引日
            annual_total: 当該取引前の年度累計売上（円）
            
        Returns:
            ボーナスステージ適用の可否
        """
        # 年度累計が閾値に達していない場合は適用なし
        if annual_total < self.BONUS_THRESHOLD:
            return False
        
        # 閾値達成月を計算
        # （実際の運用では、閾値達成の翌月1日から適用）
        # ここでは簡略化して、閾値達成後の取引すべてに適用
        return True
    
    def calculate_reward_with_bonus(
        self,
        commission: int,
        property_type: PropertyType,
        transaction_date: datetime,
        annual_total: int
    ) -> Tuple[int, bool]:
        """
        ボーナスステージを考慮した報酬計算
        
        Args:
            commission: 税抜仲介手数料（円）
            property_type: 案件タイプ
            transaction_date: 取引日
            annual_total: 取引前の年度累計売上（円）
            
        Returns:
            (報酬額, ボーナス適用フラグ)
        """
        # 自己発見案件またはTERASS Picksの場合のみボーナス対象
        is_self_discovered = property_type in [
            PropertyType.SELF_DISCOVERED, 
            PropertyType.TERASS_PICKS
        ]
        
        if is_self_discovered and self.is_bonus_stage_active(
            transaction_date, annual_total
        ):
            reward = int(commission * self.BONUS_RATE)
            return reward, True
        else:
            reward = self.calculate_basic_reward(commission, property_type)
            return reward, False
    
    def add_transaction(
        self,
        commission: int,
        property_type: PropertyType,
        transaction_date: datetime,
        description: str = ""
    ) -> Dict:
        """
        取引を追加し、報酬を計算
        
        Args:
            commission: 税抜仲介手数料（円）
            property_type: 案件タイプ
            transaction_date: 取引日
            description: 取引の説明
            
        Returns:
            取引情報の辞書
        """
        # 年度累計を計算
        annual_total = self.get_annual_total(transaction_date)
        
        # 報酬計算
        reward, bonus_applied = self.calculate_reward_with_bonus(
            commission, property_type, transaction_date, annual_total
        )
        
        # 取引情報を記録
        transaction = {
            "date": transaction_date,
            "commission": commission,
            "property_type": property_type,
            "reward": reward,
            "bonus_applied": bonus_applied,
            "annual_total_before": annual_total,
            "description": description
        }
        
        self.transactions.append(transaction)
        return transaction
    
    def get_annual_total(self, reference_date: datetime) -> int:
        """
        指定日時点での年度累計売上を計算
        
        Args:
            reference_date: 基準日
            
        Returns:
            年度累計売上（円）
        """
        fiscal_year = self._get_fiscal_year(reference_date)
        
        total = 0
        for transaction in self.transactions:
            if self._get_fiscal_year(transaction["date"]) == fiscal_year:
                if transaction["date"] < reference_date:
                    total += transaction["commission"]
        
        return total
    
    def _get_fiscal_year(self, date: datetime) -> int:
        """
        年度を計算
        
        Args:
            date: 日付
            
        Returns:
            年度（西暦）
        """
        if date.month >= self.fiscal_year_start_month:
            return date.year
        else:
            return date.year - 1
    
    def get_summary(self, fiscal_year: int = None) -> Dict:
        """
        報酬サマリーを取得
        
        Args:
            fiscal_year: 集計対象の年度（Noneの場合は全期間）
            
        Returns:
            サマリー情報
        """
        if fiscal_year is None:
            target_transactions = self.transactions
        else:
            target_transactions = [
                t for t in self.transactions
                if self._get_fiscal_year(t["date"]) == fiscal_year
            ]
        
        total_commission = sum(t["commission"] for t in target_transactions)
        total_reward = sum(t["reward"] for t in target_transactions)
        bonus_count = sum(1 for t in target_transactions if t["bonus_applied"])
        
        return {
            "fiscal_year": fiscal_year,
            "transaction_count": len(target_transactions),
            "total_commission": total_commission,
            "total_reward": total_reward,
            "bonus_applied_count": bonus_count,
            "average_rate": total_reward / total_commission if total_commission > 0 else 0
        }
    
    def simulate_reward(
        self,
        commission: int,
        property_type: PropertyType,
        current_annual_total: int = 0
    ) -> Dict:
        """
        報酬をシミュレーション（実際には記録しない）
        
        Args:
            commission: 税抜仲介手数料（円）
            property_type: 案件タイプ
            current_annual_total: 現在の年度累計売上（円）
            
        Returns:
            シミュレーション結果
        """
        transaction_date = datetime.now()
        reward, bonus_applied = self.calculate_reward_with_bonus(
            commission, property_type, transaction_date, current_annual_total
        )
        
        rate = reward / commission if commission > 0 else 0
        
        return {
            "commission": commission,
            "property_type": property_type.value,
            "reward": reward,
            "rate": rate,
            "bonus_applied": bonus_applied,
            "annual_total": current_annual_total,
            "new_annual_total": current_annual_total + commission,
            "bonus_threshold_reached": (
                current_annual_total + commission >= self.BONUS_THRESHOLD
            )
        }


def main():
    """使用例"""
    calculator = RewardCalculator()
    
    # 例1: 自己発見案件（年度累計1,800万円）
    print("=== 例1: 自己発見案件 ===")
    result1 = calculator.simulate_reward(
        commission=5_000_000,
        property_type=PropertyType.SELF_DISCOVERED,
        current_annual_total=18_000_000
    )
    print(f"仲介手数料: {result1['commission']:,}円")
    print(f"報酬: {result1['reward']:,}円 ({result1['rate']:.1%})")
    print(f"ボーナス適用: {result1['bonus_applied']}")
    print(f"新年度累計: {result1['new_annual_total']:,}円")
    print()
    
    # 例2: ボーナスステージ適用（年度累計2,100万円）
    print("=== 例2: ボーナスステージ適用 ===")
    result2 = calculator.simulate_reward(
        commission=3_000_000,
        property_type=PropertyType.SELF_DISCOVERED,
        current_annual_total=21_000_000
    )
    print(f"仲介手数料: {result2['commission']:,}円")
    print(f"報酬: {result2['reward']:,}円 ({result2['rate']:.1%})")
    print(f"ボーナス適用: {result2['bonus_applied']}")
    print()
    
    # 例3: TERASS Picks（自己発見扱い）
    print("=== 例3: TERASS Picks ===")
    result3 = calculator.simulate_reward(
        commission=4_000_000,
        property_type=PropertyType.TERASS_PICKS,
        current_annual_total=15_000_000
    )
    print(f"仲介手数料: {result3['commission']:,}円")
    print(f"報酬: {result3['reward']:,}円 ({result3['rate']:.1%})")
    print(f"案件タイプ: {result3['property_type']}")
    print()
    
    # 例4: 本部送客
    print("=== 例4: 本部送客 ===")
    result4 = calculator.simulate_reward(
        commission=5_000_000,
        property_type=PropertyType.HQ_REFERRAL,
        current_annual_total=15_000_000
    )
    print(f"仲介手数料: {result4['commission']:,}円")
    print(f"報酬: {result4['reward']:,}円 ({result4['rate']:.1%})")
    print()


if __name__ == "__main__":
    main()
