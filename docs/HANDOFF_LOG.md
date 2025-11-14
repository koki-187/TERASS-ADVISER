# TERASS業動サポートAI – ハンドオフログ

このドキュメントは、プロジェクトの引き継ぎ時に行われた作業と
決定事項を記録するためのものです。AI 代行アシスタントや
新しい開発者がプロジェクトの背景を理解しやすくすることを目的としています。

## 2025 11 14

- ユーザーが GitHub Actions での iOS ビルドを希望したため、
  `.github/workflows/ios-build.yml` を作成。
  - Bitwarden Secrets Manager を使って OpenAI API などの機密値を
    自動注入し、EAS CLI で TestFlight へ自動提出する設計。
  - Workflow は `workflow_dispatch` で手動実行可能。

- デスクトップアプリのワンタップ起動スクリプトを作成。
  - `scripts/start_desktop.ps1` は PowerShell 上で仮想環境生成、依存インストール、Bitwarden 注入を行う。
  - `start_terass_ai.cmd` と `start_terass_ai.command` は各 OS から
    `start_desktop.ps1` を呼び出す薄いラッパー。

- リリースノート (`docs/RELEASE_NOTES.md`) を追加し、
  新機能・改善点・注意点を整理。

## 次のステップ

- README の更新: iOS とデスクトップの起動・ビルド手順、Bitwarden 設定方法をまとめる。
- EAS トークン (`EAS_TOKEN`) を GitHub Secrets に登録していない場合、
  Expo アカウントから取得して追加する。
- TestFlight でアプリをインストールし、実機動作を確認。
