# ChatGPT Integration Guide

このドキュメントでは、TERASS Adviser APIをChatGPTと統合する方法を説明します。

## 概要

TERASS Adviser APIを使用すると、ChatGPTから直接以下の機能にアクセスできます:

- **報酬計算**: 不動産取引の報酬を自動計算
- **エージェントクラス判定**: 売上と実績に基づくクラス判定
- **フィードバック投稿**: 意見や要望を直接送信

## ChatGPT Actions設定方法

### 1. OpenAPI仕様のインポート

1. ChatGPT画面で「GPTを作成」をクリック
2. 「Configure」タブを開く
3. 「Actions」セクションで「Create new action」をクリック
4. 「Import from URL」または「Schema」エディタに以下のURLまたは内容を貼り付け:
   - URL: `https://your-api-domain.com/openapi.json`
   - または、`openapi.json`ファイルの内容を直接貼り付け

### 2. 認証設定

1. Authentication設定で「API Key」を選択
2. 以下のように設定:
   - **Auth Type**: API Key
   - **API Key**: サーバーの`API_TOKEN`環境変数と同じ値
   - **Header Name**: `X-API-Token`

### 3. プライバシーポリシー設定

Privacy policyフィールドに適切なURLを入力します。

### 4. テスト

「Test」ボタンを押して、各エンドポイントが正常に動作することを確認します。

## API使用例

### 報酬計算

ChatGPTに以下のように質問できます:

```
自己発見案件で税抜仲介手数料が500万円の場合の報酬を計算してください。
```

ChatGPTは以下のようなAPIリクエストを送信します:

```json
POST /api/v1/reward/calculate
{
  "deals": [
    {
      "tax_excluded_fee": 5000000,
      "source": "self",
      "date": "2025-10-27"
    }
  ]
}
```

### エージェントクラス判定

```
首都圏で売上が1200万円、案件数が5件の場合のエージェントクラスを教えてください。
```

ChatGPTは以下のようなAPIリクエストを送信します:

```json
POST /api/v1/agent/class
{
  "region": "capital",
  "period_sales": 12000000,
  "cumulative_cases": 5
}
```

### フィードバック投稿

```
モバイルアプリがあるともっと便利だと思います。この要望を記録してください。
```

ChatGPTは以下のようなAPIリクエストを送信します:

```json
POST /api/v1/feedback
{
  "user_id": "chatgpt_user",
  "category": "feature_request",
  "message": "モバイルアプリがあるともっと便利だと思います。"
}
```

## サーバー起動方法

### 必要な依存関係のインストール

```bash
pip install flask flask-cors
```

### 環境変数の設定

```bash
export API_TOKEN="your-secure-token-here"
export API_PORT=5000
export DEBUG=false
```

### サーバー起動

```bash
python api_server.py
```

デフォルトでは `http://localhost:5000` でサーバーが起動します。

## セキュリティ考慮事項

1. **API認証**: すべてのAPIエンドポイント（health check以外）は`X-API-Token`ヘッダーによる認証が必要です。
2. **トークン管理**: API_TOKENは環境変数で管理し、決してコードにハードコードしないでください。
3. **HTTPS使用**: 本番環境では必ずHTTPSを使用してください。
4. **レート制限**: 必要に応じてレート制限を実装してください（Flaskの拡張機能を使用）。

## トラブルシューティング

### 401 Unauthorized エラー

- `X-API-Token`ヘッダーが正しく設定されているか確認
- サーバー側の`API_TOKEN`環境変数が設定されているか確認

### 500 Internal Server Error

- サーバーログを確認
- 必要なPythonモジュールがインストールされているか確認
- `src/engine/`モジュールが正しく読み込めるか確認

### ChatGPTからAPIが呼べない

1. サーバーが起動しているか確認
2. ファイアウォールでポートが開いているか確認
3. ChatGPT ActionsでURLが正しく設定されているか確認
4. CORSが有効になっているか確認（`flask-cors`がインストールされているか）

## 高度な使用例

### カスタムGPT作成

TERASS業務アシスタント専用のカスタムGPTを作成できます:

1. **名前**: TERASS業務アシスタント
2. **説明**: TERASS不動産エージェント向けの業務サポートAI
3. **Instructions**:
```
あなたはTERASS不動産エージェントをサポートするAIアシスタントです。
報酬計算、エージェントクラス判定、物件情報の提供を行います。
常に日本語で親切丁寧に対応してください。
```
4. **Actions**: 上記で設定したAPIアクションを有効化

### バッチ処理

複数の案件を一度に計算する例:

```json
POST /api/v1/reward/calculate
{
  "deals": [
    {
      "tax_excluded_fee": 5000000,
      "source": "self",
      "date": "2025-04-01"
    },
    {
      "tax_excluded_fee": 3000000,
      "source": "hq",
      "date": "2025-05-15"
    },
    {
      "tax_excluded_fee": 4000000,
      "source": "terass_offer",
      "date": "2025-06-20"
    }
  ]
}
```

## API仕様詳細

完全なAPI仕様は`openapi.json`ファイルを参照してください。主要なエンドポイント:

- `GET /`: API情報
- `GET /api/v1/health`: ヘルスチェック
- `POST /api/v1/reward/calculate`: 報酬計算
- `POST /api/v1/agent/class`: エージェントクラス判定
- `POST /api/v1/feedback`: フィードバック投稿
- `GET /api/v1/feedback`: フィードバック一覧取得

## サポート

問題が発生した場合は、以下の情報を含めてIssueを作成してください:

- エラーメッセージ
- 実行したコマンド
- 環境情報（Python version, OS等）
- サーバーログ（該当部分）
