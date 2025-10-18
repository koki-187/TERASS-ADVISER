#!/usr/bin/env python3
"""
TERASS業務アドバイザー - コマンドラインインターフェース

TERASS社の業務委託エージェント向けアドバイザーシステムのCLI

使用方法:
    python src/cli/main.py start
"""

import sys
import os
from pathlib import Path

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.engine.reward_calculator import RewardCalculator, PropertyType
from src.engine.agent_class import AgentClassifier, AgentProfile, Region


def print_header():
    """ヘッダーを表示"""
    print("=" * 60)
    print("    TERASS業務アドバイザー Super Agent")
    print("    TERASS Business Adviser - CLI Interface")
    print("=" * 60)
    print()


def print_menu():
    """メインメニューを表示"""
    print("\n【メインメニュー】")
    print("1. 💰 報酬計算シミュレーション")
    print("2. 📊 Agent Class 判定")
    print("3. 🏠 TERASS Picks について")
    print("4. 💳 Loan Checker について")
    print("5. 📋 ヘルプ")
    print("0. 終了")
    print()


def reward_simulation():
    """報酬計算シミュレーション"""
    print("\n" + "=" * 60)
    print("💰 報酬計算シミュレーション")
    print("=" * 60)
    
    calculator = RewardCalculator()
    
    # 案件タイプの選択
    print("\n【案件タイプを選択してください】")
    print("1. 自己発見案件")
    print("2. 本部送客")
    print("3. Terass Offer")
    print("4. TERASS Picks")
    
    try:
        type_choice = input("\n選択 (1-4): ").strip()
        
        type_map = {
            "1": PropertyType.SELF_DISCOVERED,
            "2": PropertyType.HQ_REFERRAL,
            "3": PropertyType.TERASS_OFFER,
            "4": PropertyType.TERASS_PICKS,
        }
        
        if type_choice not in type_map:
            print("❌ 無効な選択です")
            return
        
        property_type = type_map[type_choice]
        
        # 仲介手数料の入力
        commission_input = input("\n税抜仲介手数料（万円）: ").strip()
        commission = int(float(commission_input) * 10000)
        
        # 年度累計売上の入力
        annual_input = input("現在の年度累計売上（万円、0の場合は0）: ").strip()
        annual_total = int(float(annual_input) * 10000) if annual_input else 0
        
        # シミュレーション実行
        result = calculator.simulate_reward(
            commission=commission,
            property_type=property_type,
            current_annual_total=annual_total
        )
        
        # 結果表示
        print("\n" + "-" * 60)
        print("【シミュレーション結果】")
        print("-" * 60)
        print(f"案件タイプ: {result['property_type']}")
        print(f"仲介手数料: {result['commission']:,}円")
        print(f"報酬額: {result['reward']:,}円")
        print(f"報酬率: {result['rate']:.1%}")
        print(f"ボーナス適用: {'✅ はい' if result['bonus_applied'] else '❌ いいえ'}")
        print(f"\n現在の年度累計: {result['annual_total']:,}円")
        print(f"成約後の年度累計: {result['new_annual_total']:,}円")
        
        if result['bonus_threshold_reached']:
            if result['annual_total'] < RewardCalculator.BONUS_THRESHOLD:
                print(f"\n🎉 おめでとうございます！")
                print(f"この成約でボーナスステージ（{RewardCalculator.BONUS_THRESHOLD:,}円）に到達します！")
                print(f"翌月1日から年度末まで、自己発見案件の報酬率が90%になります。")
        
        if not result['bonus_applied'] and result['annual_total'] >= RewardCalculator.BONUS_THRESHOLD:
            print(f"\n💡 ヒント: 自己発見案件またはTERASS Picksの場合、")
            print(f"   ボーナスステージで報酬率90%が適用されます。")
        
    except ValueError as e:
        print(f"❌ 入力エラー: {e}")
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")


def agent_class_check():
    """Agent Class判定"""
    print("\n" + "=" * 60)
    print("📊 Agent Class 判定")
    print("=" * 60)
    
    classifier = AgentClassifier()
    
    try:
        # エージェント情報の入力
        name = input("\nお名前: ").strip()
        
        print("\n地域を選択してください:")
        print("1. 首都圏")
        print("2. 地方")
        region_choice = input("選択 (1-2): ").strip()
        
        if region_choice == "1":
            region = Region.TOKYO_AREA
        elif region_choice == "2":
            region = Region.OTHER
        else:
            print("❌ 無効な選択です")
            return
        
        # 実績の入力
        sales_input = input("\n半期売上（万円）: ").strip()
        half_year_sales = int(float(sales_input) * 10000)
        
        deals_input = input("累計成約件数: ").strip()
        total_deals = int(deals_input)
        
        # プロフィール作成
        profile = AgentProfile(
            name=name,
            region=region,
            half_year_sales=half_year_sales,
            total_deals=total_deals
        )
        
        # 分析実行
        analysis = classifier.analyze_profile(profile)
        
        # 結果表示
        print("\n" + "-" * 60)
        print("【判定結果】")
        print("-" * 60)
        print(f"お名前: {analysis['name']}")
        print(f"地域: {analysis['region']}")
        print(f"現在のクラス: {analysis['current_class']}")
        print(f"半期売上: {analysis['half_year_sales']:,}円")
        print(f"累計成約件数: {analysis['total_deals']}件")
        
        print(f"\n【{analysis['current_class']} の特典】")
        for benefit in analysis['benefits']:
            print(f"  ✓ {benefit}")
        
        # 昇格情報
        if analysis.get('next_class'):
            print(f"\n【次のクラス: {analysis['next_class']}】")
            gap = analysis['promotion_gap']
            
            print(f"必要条件:")
            print(f"  - 半期売上: {gap['target_sales']:,}円")
            print(f"  - 累計成約件数: {gap['target_deals']}件")
            
            print(f"\n現在の状況:")
            if gap['sales_achieved']:
                print(f"  ✅ 売上条件: 達成済み")
            else:
                print(f"  ⏳ 売上条件: あと{gap['sales_gap']:,}円")
            
            if gap['deals_achieved']:
                print(f"  ✅ 成約件数: 達成済み")
            else:
                print(f"  ⏳ 成約件数: あと{gap['deals_gap']}件")
            
            if gap['can_promote']:
                print(f"\n🎉 おめでとうございます！昇格条件を満たしています！")
        elif analysis.get('message'):
            print(f"\n{analysis['message']}")
        
    except ValueError as e:
        print(f"❌ 入力エラー: {e}")
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")


def terass_picks_info():
    """TERASS Picks の説明"""
    print("\n" + "=" * 60)
    print("🏠 TERASS Picks について")
    print("=" * 60)
    
    print("""
TERASS Picksは、複数の不動産ポータルサイトを統合検索できるシステムです。

【対応ポータル】
  • SUUMO（スーモ）
  • at HOME（アットホーム）
  • REINS（レインズ：東日本・中部・西日本・近畿）

【主な特徴】
  • 複数ポータルを一括検索
  • 顧客のリアクション機能
  • 自己発見案件として報酬75-90%

【報酬について】
  TERASS Picksで発見した物件は「自己発見案件」として扱われます。
  - 通常: 75%
  - ボーナスステージ: 90%（年度累計2,000万円達成後）

【使い分けのポイント】
  ✓ 幅広い選択肢を提示したい → TERASS Picks
  ✓ TERASS独自の物件がある → Terass Offer（報酬55%）

詳細は docs/PICKS_INTEGRATION.md をご覧ください。
    """)


def loan_checker_info():
    """Loan Checker の説明"""
    print("\n" + "=" * 60)
    print("💳 Loan Checker について")
    print("=" * 60)
    
    print("""
Loan Checkerは、107の金融機関に対応した住宅ローン最適提案システムです。

【対応金融機関】
  • 都市銀行: 5行
  • 地方銀行: 64行
  • 信用金庫: 26組織
  • ネット銀行: 8行
  • その他: 4行
  合計: 107金融機関

【金利範囲】
  • 最低金利: 0.520%（変動）
  • 最高金利: 3.242%（固定）

【主な機能】
  • 金利比較と検索
  • 返済シミュレーション
  • 審査通過可能性の判定
  • 顧客条件に最適化された提案

【提案の流れ】
  1. 顧客ヒアリング
  2. Loan Checkerで検索
  3. 最適3-5行を提案
  4. 返済シミュレーション提示
  5. 審査申込サポート

詳細は docs/LOAN_CHECKER.md をご覧ください。
    """)


def show_help():
    """ヘルプ情報を表示"""
    print("\n" + "=" * 60)
    print("📋 ヘルプ")
    print("=" * 60)
    
    print("""
【TERASS業務アドバイザー Super Agent について】

このシステムは、TERASS社の業務委託不動産エージェント向けに
開発された専門アドバイザーAIシステムです。

【主な機能】
  1. 💰 報酬計算シミュレーション
     - 案件タイプ別の報酬計算
     - ボーナスステージの判定
     - 年度累計の追跡

  2. 📊 Agent Class 判定
     - 8段階のクラス判定
     - 昇格までの道のり表示
     - 地域別基準の適用

  3. 🏠 TERASS Picks
     - 複数ポータル統合検索
     - 自己発見案件として高報酬
     
  4. 💳 Loan Checker
     - 107金融機関対応
     - 最適なローン提案

【関連ドキュメント】
  - README.md: システム概要
  - docs/TERASS-ADVISER_SPEC.md: 詳細仕様
  - docs/PICKS_INTEGRATION.md: TERASS Picks ガイド
  - docs/LOAN_CHECKER.md: Loan Checker ガイド

【問い合わせ】
  リポジトリのIssueまたは担当窓口へご連絡ください。
    """)


def main():
    """メイン関数"""
    if len(sys.argv) < 2:
        print("使用方法: python src/cli/main.py start")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "start":
        print_header()
        
        while True:
            print_menu()
            choice = input("選択してください (0-5): ").strip()
            
            if choice == "1":
                reward_simulation()
            elif choice == "2":
                agent_class_check()
            elif choice == "3":
                terass_picks_info()
            elif choice == "4":
                loan_checker_info()
            elif choice == "5":
                show_help()
            elif choice == "0":
                print("\nTERASS業務アドバイザーを終了します。")
                print("お疲れさまでした！\n")
                break
            else:
                print("❌ 無効な選択です。0-5の数字を入力してください。")
            
            input("\nEnterキーを押して続行...")
    
    else:
        print(f"❌ 不明なコマンド: {command}")
        print("使用方法: python src/cli/main.py start")
        sys.exit(1)


if __name__ == "__main__":
    main()
