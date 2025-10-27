"""
Agent Class 判定ロジック（サンプル）
- 首都圏/地方 の閾値を入力して判定
- 半期/通期、累計件数要件に基づく判定サンプル
"""

from dataclasses import dataclass

@dataclass
class AgentRecord:
    region: str  # 'capital' or 'local'
    period_sales: float  # 半期または通期の売上（税抜）
    cumulative_cases: int

CLASS_RULES = [
    # クラス名, region, min_sales, min_cases, period (half/annual)
    ('Premier', 'capital', 30_000_000, 10, 'annual'),  # 3,000万円（単位に注意）
    ('Premier', 'local', 25_000_000, 10, 'annual'),
    ('Senior', 'capital', 12_000_000, 5, 'half'),
    ('Senior', 'local', 10_000_000, 5, 'half'),
    ('Expert', 'capital', 8_000_000, 5, 'half'),
    ('Expert', 'local', 6_000_000, 5, 'half'),
    ('Lead', 'capital', 5_000_000, 5, 'half'),
    ('Lead', 'local', 4_000_000, 5, 'half'),
    # その他 Tier / Junior は別途条件
]

def determine_class(record: AgentRecord) -> dict:
    for cls, region, min_sales, min_cases, period in CLASS_RULES:
        if record.region == region and record.period_sales >= min_sales and record.cumulative_cases >= min_cases:
            return {'class': cls, 'met_sales': True, 'met_cases': True}
    # デフォルト：未達なら最も近いクラスと不足分を返す
    # 簡易：Lead までの不足を計算するサンプル
    target = CLASS_RULES[-2]  # Lead 地方等の参照
    needed_sales = max(0, target[2] - record.period_sales)
    needed_cases = max(0, target[3] - record.cumulative_cases)
    return {'class': 'Unranked', 'needed_sales': needed_sales, 'needed_cases': needed_cases}
