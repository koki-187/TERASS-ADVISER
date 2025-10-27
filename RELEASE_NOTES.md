# TERASS業務サポートAI – リリースノート（2025‑10‑27）

このリポジトリでは、不動産エージェント向けチャットAI「TERASS業務サポートAI」を開発しています。Tkinter を用いたデスクトップ版アプリと、Expo/React Native を用いた iOS 版アプリの双方を提供し、物件相談や手付金預かりに関する対話シナリオ、ナレッジ検索、FAQ 画面などを備えています。現在は第１版であり、ユーザーテストやフィードバックに基づいて継続的に改善していく予定です。

## 🎯 現行バージョンの主な機能

- **チャット UI と AI 連携** – Tkinter ベースのメインスクリプト `terass_assistant_with_scenarios.py` でチャットウインドウを構築し、OpenAI API を用いた自然な会話と、14 ステップの「手付金預かり」シナリオによる会話誘導を実装しています【116776203789687†screenshot】。
- **ナレッジ検索と RAG** – デスクトップ版では `rag_utils.py` と `rag_ingestion.py` を用いてベクタDB検索や Retrieval Augmented Generation による資料検索を実装。iOS 版では `vectorSearch.js` で外部ベクタ API に接続し、`rag.js` で埋め込み資料を検索できます。
- **安全な秘密情報管理** – `bitwarden_guide.md` に従い、Bitwarden Secrets Manager から CLI（bw/bws）経由で API キーを注入する方法を解説しています【843620883738721†screenshot】。コードにキーをハードコードせず、`bws run` により実行時に環境変数として注入します。
- **パッケージング** – デスクトップ版は PyInstaller でスタンドアロン実行ファイル化し、`packaging_guide.md` で `pyinstaller --onefile` による手順を説明しています【843620883738721†screenshot】。iOS 版は Expo/EAS CLI により .ipa を生成し、TestFlight で配布可能です。
- **UI/UX 改善と付属画面** – ダークモード、ヘルプ/FAQ 画面、開発メモ画面を実装し、3D 風アイコンや女性アバターの画像を統一してユーザー体験を向上させています。

## ✅ 最近の改善点

- **GitHub 書き込み権限の検証** – PR #8 で `docs/write‑access‑check.md` を追加し、本リポジトリへの直接書き込みが有効であることを確認しました。また、Issue コメントからファイルをコミットできる GitHub Actions ワークフロー (`.github/workflows/commit-from-issue.yml`) とその説明書 (`docs/COMMIT_FROM_ISSUE_WORKFLOW.md`) を追加しました。
- **自動化キットの整備** – `terass-automation-kit` ディレクトリには、定期的にデータ取得とベクタDB更新を行う Node.js スクリプトと GitHub Actions 用のワークフローが含まれており、運用に応じてスケジューリングできます。
- **Bitwarden シークレット名の統一** – bws CLI で日本語キーを英数字＋アンダースコアへリネームし、`--uuids-as-keynames` オプションで UUID 利用も可能にしました。アプリを起動する際は `bws run --project-id <プロジェクトID> -- python terass_assistant_with_scenarios.py` を使用します。

## 🔧 残課題および第２フェーズ計画

このリリースは第１版であり、今後ユーザーテストを通じて UI/UX や機能を改善します。Phase 2 以降では以下の機能拡張を検討しています。

|カテゴリー|内容|
|---|---|
|ローン診断機能|ユーザーの条件に基づいて適切なローン種類や金額を提案する診断モジュール。|
|PICKS 連携|TERASS Picks と Terass Cloud から物件情報を取得し、チャット内で提示する統合機能。|
|FAQ の拡充|よくある質問を追加・整理し、ユーザーが自己解決しやすくする。|
|入力補助|フォーム入力時のオートコンプリートやバリデーション強化。|
|自動化キットの本番連携|スクリプト実行環境を整え、定期的なデータ取得とベクタDB更新のフローを確立する。|

## 📦 配布用アーカイブ

`terass_full_package_updated.zip` には以下が含まれます。

- デスクトップ版 (`terass_desktop_release`)：メインスクリプト、シナリオモジュール、RAG ユーティリティ、フェーズ２ドキュメント、アイコン類、パッケージングガイドなど【116776203789687†screenshot】。
- iOS 版 (`terass_ios_app`)：React Native ソース、Expo 設定 (`app.json`)、ヘルプ/FAQ 画面、開発メモ画面、アセット類、設定ファイル。ベクタAPIの URL は `src/config.js` 内で設定します【843620883738721†screenshot】。
- 自動化キット (`terass-automation-kit`)：Node.js スクリプト、Cron 実行例、GitHub Actions ワークフロー、`.env.example`。Secrets は Bitwarden で管理し、`.env` ファイルには記入しません。【116776203789687†screenshot】

アーカイブを解凍した後、README とドキュメントの手順に従って環境構築とビルドを行ってください。

## 🧭 次のステップ

1. **リリースパッケージのコミット** – `terass_full_package_updated.zip` とこの `RELEASE_NOTES.md` をリポジトリに追加し、メインブランチへコミットします。ブランチ保護ルールに従い PR を作成してマージしてください。
2. **運用 URL の設定** – iOS 版の `src/config.js` にある `VECTOR_API_URL` および `KNOWLEDGE_API_URL` を本番環境のエンドポイントに置き換えます。
3. **自動化キットの本番運用** – GitHub Actions またはサーバの Cron で自動化スクリプトを定期実行し、ナレッジ資料とベクタDB を最新状態に保ちます。
4. **ユーザーテストと改善** – 事前に計画した UI/UX テストを実施し、フィードバックを基に画面や機能を改善します。特にチャット応答速度や RAG 検索精度、FAQ 内容の充実度を確認します。
5. **Phase 2 の企画検討** – ローン診断や PICKS 連携など未実装の機能について要件定義と設計を行い、優先順位を付けます。

今後のアップデートでは、ユーザーの意見を取り入れてアプリ全体を洗練させていきます。ご意見やフィードバックは歓迎します。
