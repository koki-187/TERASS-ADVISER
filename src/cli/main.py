"""
簡易 CLI（開発用）
起動: python src/cli/main.py start
"""

import sys
from src.engine.reward_calculator import calc_portfolio_reward, Deal
from src.engine.agent_class import determine_class, AgentRecord

def cmd_start():
    print("TERASS 業務アドバイザー 起動（開発モード）")
    # サンプル: 簡易的に計算を行って結果表示
    sample_deals = [
        Deal(5_000_000, 'self', '2025-04-01'),
        Deal(2_000_000, 'hq', '2025-05-01'),
    ]
    res = calc_portfolio_reward(sample_deals)
    print("総報酬:", res['total_reward'])
    for d in res['details']:
        print(d)

    # Agent class 判定サンプル
    rec = AgentRecord(region='capital', period_sales=4_500_000, cumulative_cases=3)
    cls = determine_class(rec)
    print("Agent class 判定:", cls)

if __name__ == '__main__':
    if len(sys.argv) >= 2 and sys.argv[1] == 'start':
        cmd_start()
    else:
        print("usage: python src/cli/main.py start")
"""
