"""報酬計算エンジン（サンプル実装）。

従来実装はシンプルながらも条件分岐が散在し、辞書のアンパックによる
中間オブジェクト生成など、処理コストと可読性の面で改善余地があった。
本モジュールでは以下の最適化を行っている:

* ``Deal`` dataclass を ``slots=True`` にしてインスタンスあたりのメモリを削減
* ソース毎の報酬率判定をテーブル化して条件分岐を整理
* 報酬明細の構築時に辞書のアンパックを避け、余分なオブジェクト生成を抑制

これらの変更により既存の API 仕様を維持しつつ、計算処理を軽量化する。
"""

from dataclasses import dataclass
from typing import Dict, Iterable, Tuple

# Business logic constants
BONUS_STAGE_THRESHOLD = 20_000_000  # 年度累計2,000万円でボーナスステージ
RATE_SELF_NORMAL = 0.75  # 自己発見の基本報酬率
RATE_SELF_BONUS = 0.90   # 自己発見のボーナス報酬率
RATE_HQ = 0.40           # 本部送客の報酬率
RATE_TERASS_OFFER = 0.55 # TERASS Offerの報酬率

@dataclass(slots=True)
class Deal:
    tax_excluded_fee: float  # 税抜仲介手数料（円）
    source: str  # 'self' | 'hq' | 'terass_offer'
    date: str  # 'YYYY-MM-DD' など


_SOURCE_RATE_TABLE: Dict[str, float] = {
    'hq': RATE_HQ,
    'terass_offer': RATE_TERASS_OFFER,
}

def is_bonus_stage(year_to_date_total: float) -> bool:
    # 年度累計がBONUS_STAGE_THRESHOLD以上でボーナスステージ対象
    return year_to_date_total >= BONUS_STAGE_THRESHOLD


def _resolve_rate(deal: Deal, year_to_date_total_before: float) -> Tuple[float, bool]:
    """ソースに応じた適用レートとボーナスフラグを返す。"""

    if deal.source == 'self':
        bonus = is_bonus_stage(year_to_date_total_before)
        return (RATE_SELF_BONUS if bonus else RATE_SELF_NORMAL, bonus)

    try:
        return _SOURCE_RATE_TABLE[deal.source], False
    except KeyError as exc:  # pragma: no cover - ガード節
        raise ValueError("Unknown source") from exc

def calc_reward_for_deal(deal: Deal, year_to_date_total_before: float) -> dict:
    """
    deal: 当該案件
    year_to_date_total_before: 当案件が発生する前の年度累計売上（税抜仲介手数料）
    戻り値: dict { reward_amount, rate_applied, bonus_activated (True/False) }
    """
    rate, bonus = _resolve_rate(deal, year_to_date_total_before)
    reward = round(deal.tax_excluded_fee * rate, 2)
    return {
        'reward_amount': reward,
        'rate_applied': rate,
        'bonus_activated': bonus,
    }

def calc_portfolio_reward(deals: Iterable[Deal]) -> dict:
    """複数案件の累積計算（年度内累計を考慮）"""
    total_reward = 0.0
    year_to_date = 0.0
    details = []
    for deal in deals:
        result = calc_reward_for_deal(deal, year_to_date)
        total_reward += result['reward_amount']
        year_to_date += deal.tax_excluded_fee
        details.append({
            'deal': deal,
            'reward_amount': result['reward_amount'],
            'rate_applied': result['rate_applied'],
            'bonus_activated': result['bonus_activated'],
            'year_to_date_after': year_to_date,
        })
    return {
        'total_reward': round(total_reward, 2),
        'details': details
    }
