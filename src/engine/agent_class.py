"""
TERASS業務アドバイザー - Agent Class 判定システム

このモジュールは、エージェントの実績に基づいて
Agent Classを判定し、昇格までの道のりを示します。

Agent Class:
- Premier Agent
- Executive Agent
- Master Agent
- Senior Agent
- Professional Agent
- Lead Agent
- Standard Agent
- Junior Agent
"""

from enum import Enum
from typing import Dict, Tuple, Optional
from dataclasses import dataclass


class Region(Enum):
    """地域区分"""
    TOKYO_AREA = "首都圏"
    OTHER = "地方"


class AgentClass(Enum):
    """Agent Class 階級"""
    PREMIER = "Premier Agent"
    EXECUTIVE = "Executive Agent"
    MASTER = "Master Agent"
    SENIOR = "Senior Agent"
    PROFESSIONAL = "Professional Agent"
    LEAD = "Lead Agent"
    STANDARD = "Standard Agent"
    JUNIOR = "Junior Agent"


@dataclass
class ClassCriteria:
    """クラス判定基準"""
    half_year_sales: int  # 半期売上（円）
    total_deals: int      # 累計成約件数
    
    
@dataclass
class AgentProfile:
    """エージェントプロフィール"""
    name: str
    region: Region
    half_year_sales: int  # 半期売上（円）
    total_deals: int      # 累計成約件数
    current_class: Optional[AgentClass] = None


class AgentClassifier:
    """Agent Class 判定システム"""
    
    # 首都圏の判定基準
    TOKYO_CRITERIA = {
        AgentClass.PREMIER: ClassCriteria(15_000_000, 30),
        AgentClass.EXECUTIVE: ClassCriteria(12_000_000, 24),
        AgentClass.MASTER: ClassCriteria(10_000_000, 20),
        AgentClass.SENIOR: ClassCriteria(7_500_000, 15),
        AgentClass.PROFESSIONAL: ClassCriteria(6_000_000, 12),
        AgentClass.LEAD: ClassCriteria(5_000_000, 10),
        AgentClass.STANDARD: ClassCriteria(3_000_000, 6),
        AgentClass.JUNIOR: ClassCriteria(0, 0),
    }
    
    # 地方の判定基準（首都圏より緩和）
    OTHER_CRITERIA = {
        AgentClass.PREMIER: ClassCriteria(12_000_000, 25),
        AgentClass.EXECUTIVE: ClassCriteria(10_000_000, 20),
        AgentClass.MASTER: ClassCriteria(8_000_000, 16),
        AgentClass.SENIOR: ClassCriteria(6_000_000, 12),
        AgentClass.PROFESSIONAL: ClassCriteria(4_500_000, 9),
        AgentClass.LEAD: ClassCriteria(3_500_000, 7),
        AgentClass.STANDARD: ClassCriteria(2_000_000, 4),
        AgentClass.JUNIOR: ClassCriteria(0, 0),
    }
    
    # クラス順序（上位から下位）
    CLASS_ORDER = [
        AgentClass.PREMIER,
        AgentClass.EXECUTIVE,
        AgentClass.MASTER,
        AgentClass.SENIOR,
        AgentClass.PROFESSIONAL,
        AgentClass.LEAD,
        AgentClass.STANDARD,
        AgentClass.JUNIOR,
    ]
    
    # 各クラスの特典
    CLASS_BENEFITS = {
        AgentClass.PREMIER: [
            "最優先サポート",
            "専用ブランディングツール",
            "特別報酬プログラム",
            "経営戦略サポート",
            "VIP顧客紹介",
        ],
        AgentClass.EXECUTIVE: [
            "優先サポート",
            "プレミアムツールアクセス",
            "特別報酬プログラム",
            "ビジネスコーチング",
        ],
        AgentClass.MASTER: [
            "優先サポート",
            "高度なツールアクセス",
            "ボーナスプログラム",
            "スキルアップ研修",
        ],
        AgentClass.SENIOR: [
            "標準サポート",
            "ツールフルアクセス",
            "研修プログラム",
            "マーケティング支援",
        ],
        AgentClass.PROFESSIONAL: [
            "標準サポート",
            "基本ツールアクセス",
            "研修プログラム",
        ],
        AgentClass.LEAD: [
            "基本サポート",
            "エントリーツール",
            "基礎研修",
        ],
        AgentClass.STANDARD: [
            "基本サポート",
            "スターター研修",
        ],
        AgentClass.JUNIOR: [
            "新人サポート",
            "オンボーディング",
        ],
    }
    
    def __init__(self):
        """初期化"""
        pass
    
    def get_criteria(self, region: Region) -> Dict[AgentClass, ClassCriteria]:
        """
        地域に応じた判定基準を取得
        
        Args:
            region: 地域区分
            
        Returns:
            判定基準の辞書
        """
        if region == Region.TOKYO_AREA:
            return self.TOKYO_CRITERIA
        else:
            return self.OTHER_CRITERIA
    
    def determine_class(
        self, 
        half_year_sales: int, 
        total_deals: int,
        region: Region
    ) -> AgentClass:
        """
        Agent Classを判定
        
        Args:
            half_year_sales: 半期売上（円）
            total_deals: 累計成約件数
            region: 地域区分
            
        Returns:
            判定されたAgent Class
        """
        criteria = self.get_criteria(region)
        
        # 上位から順にチェック
        for agent_class in self.CLASS_ORDER:
            requirement = criteria[agent_class]
            if (half_year_sales >= requirement.half_year_sales and
                total_deals >= requirement.total_deals):
                return agent_class
        
        # どれにも該当しない場合はJunior
        return AgentClass.JUNIOR
    
    def get_next_class(self, current_class: AgentClass) -> Optional[AgentClass]:
        """
        次のクラスを取得
        
        Args:
            current_class: 現在のクラス
            
        Returns:
            次のクラス（最上位の場合はNone）
        """
        try:
            current_index = self.CLASS_ORDER.index(current_class)
            if current_index > 0:
                return self.CLASS_ORDER[current_index - 1]
            else:
                return None  # すでに最上位
        except ValueError:
            return None
    
    def get_promotion_gap(
        self,
        current_sales: int,
        current_deals: int,
        region: Region,
        target_class: AgentClass
    ) -> Dict:
        """
        昇格までの差額を計算
        
        Args:
            current_sales: 現在の半期売上（円）
            current_deals: 現在の累計成約件数
            region: 地域区分
            target_class: 目標クラス
            
        Returns:
            差額情報
        """
        criteria = self.get_criteria(region)
        target_requirement = criteria[target_class]
        
        sales_gap = max(0, target_requirement.half_year_sales - current_sales)
        deals_gap = max(0, target_requirement.total_deals - current_deals)
        
        sales_achieved = current_sales >= target_requirement.half_year_sales
        deals_achieved = current_deals >= target_requirement.total_deals
        
        return {
            "target_class": target_class.value,
            "target_sales": target_requirement.half_year_sales,
            "target_deals": target_requirement.total_deals,
            "current_sales": current_sales,
            "current_deals": current_deals,
            "sales_gap": sales_gap,
            "deals_gap": deals_gap,
            "sales_achieved": sales_achieved,
            "deals_achieved": deals_achieved,
            "can_promote": sales_achieved and deals_achieved,
        }
    
    def analyze_profile(self, profile: AgentProfile) -> Dict:
        """
        エージェントプロフィールを分析
        
        Args:
            profile: エージェントプロフィール
            
        Returns:
            分析結果
        """
        # 現在のクラスを判定
        determined_class = self.determine_class(
            profile.half_year_sales,
            profile.total_deals,
            profile.region
        )
        
        # 次のクラスを取得
        next_class = self.get_next_class(determined_class)
        
        result = {
            "name": profile.name,
            "region": profile.region.value,
            "current_class": determined_class.value,
            "half_year_sales": profile.half_year_sales,
            "total_deals": profile.total_deals,
            "benefits": self.CLASS_BENEFITS[determined_class],
        }
        
        # 次のクラスへの昇格情報
        if next_class:
            promotion_info = self.get_promotion_gap(
                profile.half_year_sales,
                profile.total_deals,
                profile.region,
                next_class
            )
            result["next_class"] = next_class.value
            result["promotion_gap"] = promotion_info
        else:
            result["next_class"] = None
            result["message"] = "最上位クラスに到達しています！"
        
        return result
    
    def get_class_path(
        self,
        current_sales: int,
        current_deals: int,
        region: Region
    ) -> list:
        """
        現在位置から最上位までの道のりを取得
        
        Args:
            current_sales: 現在の半期売上（円）
            current_deals: 現在の累計成約件数
            region: 地域区分
            
        Returns:
            各クラスへの昇格情報のリスト
        """
        current_class = self.determine_class(
            current_sales, current_deals, region
        )
        current_index = self.CLASS_ORDER.index(current_class)
        
        path = []
        for i in range(current_index, -1, -1):
            target_class = self.CLASS_ORDER[i]
            gap_info = self.get_promotion_gap(
                current_sales, current_deals, region, target_class
            )
            gap_info["is_current"] = (i == current_index)
            path.append(gap_info)
        
        return path


def main():
    """使用例"""
    classifier = AgentClassifier()
    
    # 例1: 首都圏のエージェント
    print("=== 例1: 首都圏のエージェント ===")
    profile1 = AgentProfile(
        name="田中太郎",
        region=Region.TOKYO_AREA,
        half_year_sales=4_500_000,
        total_deals=8
    )
    
    analysis1 = classifier.analyze_profile(profile1)
    print(f"名前: {analysis1['name']}")
    print(f"地域: {analysis1['region']}")
    print(f"現在のクラス: {analysis1['current_class']}")
    print(f"半期売上: {analysis1['half_year_sales']:,}円")
    print(f"累計成約件数: {analysis1['total_deals']}件")
    print(f"\n特典:")
    for benefit in analysis1['benefits']:
        print(f"  - {benefit}")
    
    if analysis1.get('next_class'):
        print(f"\n次のクラス: {analysis1['next_class']}")
        gap = analysis1['promotion_gap']
        print(f"必要売上: {gap['target_sales']:,}円")
        print(f"必要成約件数: {gap['target_deals']}件")
        print(f"売上不足: {gap['sales_gap']:,}円")
        print(f"成約件数不足: {gap['deals_gap']}件")
    print()
    
    # 例2: 地方のエージェント
    print("=== 例2: 地方のエージェント ===")
    profile2 = AgentProfile(
        name="佐藤花子",
        region=Region.OTHER,
        half_year_sales=10_500_000,
        total_deals=21
    )
    
    analysis2 = classifier.analyze_profile(profile2)
    print(f"名前: {analysis2['name']}")
    print(f"地域: {analysis2['region']}")
    print(f"現在のクラス: {analysis2['current_class']}")
    print(f"半期売上: {analysis2['half_year_sales']:,}円")
    print(f"累計成約件数: {analysis2['total_deals']}件")
    
    if analysis2.get('next_class'):
        print(f"\n次のクラス: {analysis2['next_class']}")
        gap = analysis2['promotion_gap']
        if gap['can_promote']:
            print("昇格条件を満たしています！")
        else:
            print(f"売上不足: {gap['sales_gap']:,}円")
            print(f"成約件数不足: {gap['deals_gap']}件")
    elif analysis2.get('message'):
        print(f"\n{analysis2['message']}")
    print()
    
    # 例3: 昇格までの道のり
    print("=== 例3: 昇格までの道のり ===")
    path = classifier.get_class_path(
        current_sales=3_000_000,
        current_deals=6,
        region=Region.TOKYO_AREA
    )
    
    print("首都圏・売上300万円・6件のエージェントの昇格パス:")
    for step in path:
        marker = "★" if step['is_current'] else "→"
        status = "（現在）" if step['is_current'] else ""
        if step['can_promote']:
            status = "（達成可能）"
        
        print(f"{marker} {step['target_class']}: "
              f"売上{step['target_sales']:,}円 / {step['target_deals']}件 {status}")
        
        if not step['is_current'] and not step['can_promote']:
            print(f"   不足: 売上{step['sales_gap']:,}円 / {step['deals_gap']}件")


if __name__ == "__main__":
    main()
