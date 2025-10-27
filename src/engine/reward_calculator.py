"""
報酬計算エンジン（サンプル実装）
- 税抜仲介手数料を基準に計算
- 自己発見 / 本部送客 / Terass Offer に対応
- ボーナスステージ自動判定（年度累計2,000万円）
"""

from dataclasses import dataclass
from typing import List

@dataclass
class Deal:
    tax_excluded_fee: float  # 税抜仲介手数料（円）
    source: str  # 'self' | 'hq' | 'terass_offer'
    date: str  # 'YYYY-MM-DD' など

def is_bonus_stage(year_to_date_total: float) -> bool:
    # 年度累計2,000万円（20,000,000円）達成でボーナスステージ（90%）対象
    return year_to_date_total >= 20_000_000

def calc_reward_for_deal(deal: Deal, year_to_date_total_before: float) -> dict:
    """
    deal: 当該案件
    year_to_date_total_before: 当案件が発生する前の年度累計売上（税抜仲介手数料）
    戻り値: dict { reward_amount, rate_applied, bonus_activated (True/False) }
    """
    # 基本率
    if deal.source == 'self':
        # 自己発見：基本75%、ボーナス90%
        if is_bonus_stage(year_to_date_total_before):
            rate = 0.90
            bonus = True
        else:
            rate = 0.75
            bonus = False
    elif deal.source == 'hq':
        rate = 0.40
        bonus = False
    elif deal.source == 'terass_offer':
        rate = 0.55
        bonus = False
    else:
        raise ValueError("Unknown source")

    reward = deal.tax_excluded_fee * rate
    return {
        'reward_amount': round(reward, 2),
        'rate_applied': rate,
        'bonus_activated': bonus
    }

def calc_portfolio_reward(deals: List[Deal]) -> dict:
    """複数案件の累積計算（年度内累計を考慮）"""
    total_reward = 0.0
    year_to_date = 0.0
    details = []
    for d in deals:
        result = calc_reward_for_deal(d, year_to_date)
        total_reward += result['reward_amount']
        year_to_date += d.tax_excluded_fee
        details.append({
            'deal': d,
            **result,
            'year_to_date_after': year_to_date
        })
    return {
        'total_reward': round(total_reward, 2),
        'details': details
    }
