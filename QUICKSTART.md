# TERASS Adviser API - Quick Start Guide

## 最速スタートガイド

### 1. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 2. 環境変数の設定

```bash
export API_TOKEN="your-secure-token-here"
export API_PORT=5000
```

### 3. APIサーバーの起動

```bash
python api_server.py
```

サーバーが `http://localhost:5000` で起動します。

### 4. APIのテスト

```bash
python test_api.py
```

すべてのテストが成功すれば、APIは正常に動作しています。

## ChatGPTとの統合

### OpenAI ChatGPT Actions設定

1. ChatGPTで新しいGPTを作成
2. 「Actions」セクションで「Create new action」をクリック
3. `openapi.json`ファイルの内容をインポート
4. Authentication設定:
   - Type: API Key
   - Header Name: `X-API-Token`
   - API Key: サーバーの`API_TOKEN`と同じ値

### カスタムGPTの指示例

```
あなたはTERASS不動産エージェントをサポートするAIアシスタントです。

主な機能:
- 報酬計算: 不動産取引の報酬を自動計算
- エージェントクラス判定: 売上実績に基づくクラス判定
- フィードバック記録: ユーザーの意見を記録

常に日本語で丁寧に対応してください。
```

## 使用例

### APIを直接呼び出す

#### 報酬計算
```bash
curl -X POST http://localhost:5000/api/v1/reward/calculate \
  -H "X-API-Token: your-token" \
  -H "Content-Type: application/json" \
  -d '{
    "deals": [
      {
        "tax_excluded_fee": 5000000,
        "source": "self",
        "date": "2025-10-27"
      }
    ]
  }'
```

#### エージェントクラス判定
```bash
curl -X POST http://localhost:5000/api/v1/agent/class \
  -H "X-API-Token: your-token" \
  -H "Content-Type: application/json" \
  -d '{
    "region": "capital",
    "period_sales": 12000000,
    "cumulative_cases": 5
  }'
```

#### フィードバック投稿
```bash
curl -X POST http://localhost:5000/api/v1/feedback \
  -H "X-API-Token: your-token" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "agent001",
    "category": "feature_request",
    "message": "新機能のリクエストです"
  }'
```

### ChatGPTから使用する

ChatGPTに以下のように質問すると、自動的にAPIを呼び出します:

```
自己発見案件で税抜仲介手数料が500万円の場合、報酬を計算してください。
```

ChatGPTが報酬計算APIを呼び出し、結果を日本語で説明します。

## トラブルシューティング

### サーバーが起動しない
- Pythonのバージョンを確認（3.10以上推奨）
- 依存関係がインストールされているか確認
- ポート5000が使用されていないか確認

### 401 Unauthorized エラー
- `X-API-Token`ヘッダーが設定されているか確認
- トークンがサーバーの`API_TOKEN`と一致しているか確認

### ChatGPTからAPIが呼べない
- サーバーが外部からアクセス可能か確認
- OpenAPIスキーマが正しくインポートされているか確認
- 開発環境では`ngrok`などのトンネリングツールを使用

## 詳細ドキュメント

- [ChatGPT統合ガイド](docs/CHATGPT_INTEGRATION.md)
- [使用例とサンプル](docs/CHATGPT_ACTIONS_EXAMPLES.md)
- [API仕様](openapi.json)

## サポート

問題が発生した場合は、GitHubのIssueで報告してください。
