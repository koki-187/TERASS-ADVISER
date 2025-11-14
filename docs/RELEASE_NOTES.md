# TERASS業動サポートAI v1.0.0 Release Notes

This release delivers a one‑click desktop launcher and automated iOS build process for
the TERASS業動サポートAI app. The goal is to provide a seamless setup for real
estate agents using the application on both desktop and mobile platforms.

## 新機能

- **ワンタップ起動【デスクトップ】**
  - Windows では `start_terass_ai.cmd`、macOS では `start_terass_ai.command` を
    ダブルクリックするだけで、Python 環境の作成・依存モジュールの
    インストール・Bitwarden 経由の秘密情報注入・アプリ起動までを自動実行します。

- **GitHub Actions による iOS 自動ビルド**
  - `.github/workflows/ios-build.yml` を追加しました。これにより、
    Expo EAS を用いた iOS アプリのビルドと TestFlight への自動提出が
    GitHub Actions 上で行えます。GitHub の Secrets に
    `BWS_ACCESS_TOKEN` と `EAS_TOKEN` を登録することで機能します。

## 改善点

- **Bitwarden Secrets Manager の統合**
  - `start_desktop.ps1` では Bitwarden CLI (`bws`) が存在する場合は
    自動的にシークレットを注入して起動します。CLI が未インストールでも
    アプリ自体は起動しますが、OpenAI のキーは環境変数に設定する必要があります。

- **クロスプラットフォーム対応**
  - Windows、macOS どちらでも同じ操作性でアプリを起動できるように
    スクリプトを用意しました。

## 既知の注意点

- **Bitwarden 未インストール時の挙動**
  - `bws` コマンドが無い場合、Secrets は注入されません。手動で
    OPENAI_API_KEY などの環境変数を設定してください。

- **EAS トークン**
  - Expo EAS の API トークンは必須です。まだ作成していない場合は
    Expo のアカウント設定から取得し、GitHub の Secrets に `EAS_TOKEN`
    として登録してください。
