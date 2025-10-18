## Pull Request Description

### 📋 Summary
This PR adds the initial project specification and sample implementation files for the TERASS業務アドバイザー (Super Agent) system.

### 🎯 Purpose
Add comprehensive documentation and sample engine implementations for:
- Reward calculation system (報酬計算エンジン)
- Agent class determination system (Agent Class判定システム)
- CLI interface for user interaction
- Integration documentation for TERASS Picks and Loan Checker

### 📦 Changes Included

#### Documentation
- `docs/TERASS-ADVISER_SPEC.md` - Complete system specification
- `docs/PICKS_INTEGRATION.md` - TERASS Picks integration guide
- `docs/LOAN_CHECKER.md` - Loan Checker (住宅ローン) implementation guide
- `.github/PULL_REQUEST_TEMPLATE.md` - This template for future PRs

#### Source Code
- `src/prompts/terass_advisor_prompt_jp.txt` - Japanese prompt for the AI advisor
- `src/engine/reward_calculator.py` - Reward calculation engine implementation
- `src/engine/agent_class.py` - Agent class determination logic
- `src/cli/main.py` - Command-line interface for the system

### 🎨 Key Features

#### 1. Reward Calculation Engine (報酬計算エンジン)
- Self-discovered properties: 75% commission
- Bonus stage: 90% commission (after reaching ¥20M annual total)
- Head office referrals: 40% commission
- Terass Offer: 55% commission

#### 2. Agent Class System (Agent Class判定システム)
- 8-tier classification system (Premier → Junior)
- Regional criteria (Tokyo area vs. other regions)
- Automatic promotion tracking
- Benefits overview for each class

#### 3. TERASS Picks Integration
- Multi-portal property search (SUUMO, at HOME, REINS)
- Customer reaction tracking
- Comparison with Terass Offer
- Treated as self-discovered properties (75-90% commission)

#### 4. Loan Checker
- 107 financial institutions database
- Interest rate comparison (0.520% - 3.242%)
- Variable and fixed-rate loan support
- Customer-optimized recommendations

### 🧪 Testing Instructions

To test this implementation locally:

1. **Clone and checkout the branch**:
   ```bash
   git clone https://github.com/koki-187/TERASS-ADVISER.git
   cd TERASS-ADVISER
   git checkout feature/initial-spec
   ```

2. **Run the CLI**:
   ```bash
   python src/cli/main.py start
   ```

3. **Verify functionality**:
   - Test reward calculation with sample data
   - Test agent class determination
   - Review documentation completeness

### 📚 Documentation Structure
```
docs/
├── TERASS-ADVISER_SPEC.md   # Main system specification
├── PICKS_INTEGRATION.md      # Property search integration
└── LOAN_CHECKER.md           # Loan recommendation system

src/
├── cli/
│   └── main.py              # CLI entry point
├── engine/
│   ├── reward_calculator.py # Reward calculation logic
│   └── agent_class.py       # Agent classification logic
└── prompts/
    └── terass_advisor_prompt_jp.txt  # AI advisor prompt
```

### ✅ Checklist
- [ ] All files are properly documented
- [ ] Code follows project conventions
- [ ] Documentation is clear and comprehensive
- [ ] CLI can be run without errors
- [ ] All integration points are documented

### 📝 Notes for Reviewers
- This is the initial specification and sample implementation
- Focus on documentation clarity and completeness
- Verify that the reward calculation logic matches TERASS requirements
- Check that all integration points (Picks, Loan Checker) are well-documented

### 🔗 Related Issues
- Initial project setup
- Foundation for TERASS業務アドバイザー Super Agent

---

**Ready for Review**: This PR is ready for review. Please do not merge until approved.
