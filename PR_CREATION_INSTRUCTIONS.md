# Pull Request Creation Instructions

## Overview
This document provides instructions for creating a pull request for the TERASS業務アドバイザー (Super Agent) initial specification and implementation.

## Branches
- **Source Branch**: `feature/initial-spec` (or `copilot/feature-initial-spec`)
- **Target Branch**: `main`

## PR Title
```
Add initial specification and sample implementation for TERASS業務アドバイザー
```

## PR Description

Use the following description for the pull request:

---

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
- `docs/TERASS-ADVISER_SPEC.md` - Complete system specification (4,515 characters)
- `docs/PICKS_INTEGRATION.md` - TERASS Picks integration guide (5,994 characters)
- `docs/LOAN_CHECKER.md` - Loan Checker implementation guide (9,117 characters)
- `.github/PULL_REQUEST_TEMPLATE.md` - Template for future PRs

#### Source Code
- `src/prompts/terass_advisor_prompt_jp.txt` - Japanese prompt for the AI advisor (1,795 characters)
- `src/engine/reward_calculator.py` - Reward calculation engine (9,037 characters, fully tested)
- `src/engine/agent_class.py` - Agent class determination logic (11,369 characters, fully tested)
- `src/cli/main.py` - Command-line interface (8,863 characters)

#### Other Files
- `.gitignore` - Python and IDE exclusions

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

3. **Test individual modules**:
   ```bash
   # Test reward calculator
   python src/engine/reward_calculator.py
   
   # Test agent class system
   python src/engine/agent_class.py
   ```

4. **Verify functionality**:
   - Test reward calculation with sample data
   - Test agent class determination
   - Review documentation completeness

### ✅ Verification Results

All modules have been tested and verified:

#### Reward Calculator Tests
```
✅ Example 1: Self-discovered property (75% commission) - Working
✅ Example 2: Bonus stage application (90% commission) - Working
✅ Example 3: TERASS Picks (treated as self-discovered) - Working
✅ Example 4: Head office referral (40% commission) - Working
```

#### Agent Class System Tests
```
✅ Tokyo area agent classification - Working
✅ Regional area agent classification - Working
✅ Promotion gap calculation - Working
✅ Benefits display - Working
```

#### CLI Tests
```
✅ Menu display - Working
✅ Help system - Working
✅ Module integration - Working
```

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

### 📝 Commits in this PR
1. Initial plan
2. Add initial specification and sample implementation files
3. Add .gitignore and remove Python cache files

### 🔍 Review Checklist
- [x] All files are properly documented
- [x] Code follows Python conventions
- [x] Documentation is clear and comprehensive in Japanese
- [x] CLI can be run without errors
- [x] All modules are tested and working
- [x] All integration points are documented
- [x] .gitignore excludes build artifacts

### 📝 Notes for Reviewers
- This is the initial specification and sample implementation
- Focus on documentation clarity and completeness
- Verify that the reward calculation logic matches TERASS requirements
- Check that all integration points (Picks, Loan Checker) are well-documented
- All code includes examples and test cases

### 🚀 Ready for Review
This PR is ready for review. **Please do not assign reviewers or merge yet** as specified in requirements. Mark PR as ready for review when created.

---

## How to Create the PR

### Option 1: Using GitHub Web Interface
1. Go to https://github.com/koki-187/TERASS-ADVISER
2. Click "Pull requests" tab
3. Click "New pull request"
4. Select base: `main`
5. Select compare: `feature/initial-spec`
6. Click "Create pull request"
7. Copy the PR description from above
8. Click "Create pull request"
9. Mark as "Ready for review"

### Option 2: Using GitHub CLI (if authenticated)
```bash
gh pr create \
  --base main \
  --head feature/initial-spec \
  --title "Add initial specification and sample implementation for TERASS業務アドバイザー" \
  --body-file PR_DESCRIPTION.md \
  --draft=false
```

## Verification Steps After PR Creation

1. Verify all files are visible in the PR diff
2. Verify the PR description is complete
3. Verify the branch comparison shows `feature/initial-spec` → `main`
4. Ensure "Ready for review" status is set
5. Do NOT assign reviewers (as per requirements)
6. Do NOT merge (as per requirements)

## Expected PR Statistics

- **Files changed**: ~13 files
- **Additions**: ~2,600 lines
- **Deletions**: ~0 lines
- **Commits**: 3 commits

## Files That Should Appear in PR

1. `.github/PULL_REQUEST_TEMPLATE.md`
2. `.gitignore`
3. `docs/LOAN_CHECKER.md`
4. `docs/PICKS_INTEGRATION.md`
5. `docs/TERASS-ADVISER_SPEC.md`
6. `src/__init__.py`
7. `src/cli/__init__.py`
8. `src/cli/main.py`
9. `src/engine/__init__.py`
10. `src/engine/agent_class.py`
11. `src/engine/reward_calculator.py`
12. `src/prompts/__init__.py`
13. `src/prompts/terass_advisor_prompt_jp.txt`

## Main Branch Setup

If the `main` branch doesn't exist in the remote repository, create it first:

```bash
# Checkout to the main branch (local)
git checkout main

# Push main branch to remote
git push origin main

# Then create the PR from feature/initial-spec to main
```

The main branch should contain only the initial README.md file, which serves as the base for this PR.
