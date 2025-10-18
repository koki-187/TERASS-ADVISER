# TERASS-ADVISER

このリポジトリは、TERASS社の業務委託不動産エージェント向け「TERASS業務アドバイザー (Super Agent)」の実装・ドキュメントを格納します。

目的:
- 報酬計算、Agent Class判定、TERASS Picks連携、住宅ローン提案、Terass Cloudワークフローなどを統合した対話型AIアドバイザーを構築するための仕様・プロンプト・実装コードを管理します。

セットアップ（ローカル）
1. Python (3.10+) を推奨
2. 仮想環境作成:
   python -m venv .venv
   source .venv/bin/activate
3. 依存関係インストール:
   pip install -r requirements.txt

起動
- 開発用:
   python src/cli/main.py start

主要ドキュメント
- docs/TERASS-ADVISER_SPEC.md : 統合仕様（日本語）
- docs/PICKS_INTEGRATION.md : TERASS Picks 連携仕様
- docs/LOAN_CHECKER.md : Loan Checker 仕様

貢献
- Issue / PR を歓迎します。リポジトリにファイル追加の許可をいただければ、初期実装を作成してPRを出します.
