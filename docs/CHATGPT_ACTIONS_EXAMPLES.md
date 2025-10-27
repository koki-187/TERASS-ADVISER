# ChatGPT Actions設定例

このファイルは、ChatGPT Actionsでの設定例を示します。

## 基本設定

### Instructions（カスタムGPTの指示）

```
あなたはTERASS不動産エージェントをサポートする業務アシスタントです。

主な機能:
1. 報酬計算: 不動産取引の報酬を計算します
2. エージェントクラス判定: 売上と実績からクラスを判定します
3. フィードバック管理: ユーザーの意見や要望を記録します

常に日本語で丁寧に対応し、計算結果は分かりやすく説明してください。
報酬計算時は、自己発見(self)、本部送客(hq)、TERASS Offer(terass_offer)の
どれに該当するか確認してください。

エージェントクラスは以下の8段階です:
- Premier（最上位）
- Senior
- Expert
- Lead
- TERASS Agent (Tier 1/2/3)
- Junior

ユーザーが意見や要望を伝えた場合は、自動的にフィードバックとして記録してください。
```

### Actions設定

1. OpenAPIスキーマをインポート
   - `openapi.json`の内容を貼り付け
   - または、APIサーバーのURL `/openapi.json` を指定

2. Authentication
   - Type: API Key
   - API Key: （環境変数API_TOKENと同じ値）
   - Auth Type: Custom
   - Custom Header Name: `X-API-Token`

## 使用例

### 例1: 報酬計算

**ユーザー入力:**
```
自己発見案件で税抜仲介手数料が500万円の場合、報酬はいくらですか？
```

**ChatGPTの動作:**
1. `/api/v1/reward/calculate` エンドポイントを呼び出し
2. 以下のデータを送信:
```json
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
3. レスポンスを解析して日本語で説明

**期待される応答:**
```
自己発見案件で税抜仲介手数料が500万円の場合、報酬は以下の通りです：

報酬額: 375万円
適用率: 75%
ボーナスステージ: 未適用

年度累計が2,000万円を超えると、翌月からボーナスステージ（90%）が
適用されます。現在の年度累計は500万円です。
```

### 例2: エージェントクラス判定

**ユーザー入力:**
```
首都圏で半期売上が1,200万円、累計案件数が5件です。私のクラスは？
```

**ChatGPTの動作:**
1. `/api/v1/agent/class` エンドポイントを呼び出し
2. 以下のデータを送信:
```json
{
  "region": "capital",
  "period_sales": 12000000,
  "cumulative_cases": 5
}
```

**期待される応答:**
```
おめでとうございます！あなたのエージェントクラスは「Senior」です。

判定基準:
- 地域: 首都圏
- 半期売上: 1,200万円（基準: 1,200万円以上）✓
- 累計案件数: 5件（基準: 5件以上）✓

次のクラス「Premier」を目指す場合は、年間売上3,000万円、
累計10件が必要です。
```

### 例3: フィードバック投稿

**ユーザー入力:**
```
TERASS Picksにスマホアプリ版があると外出先でも使いやすいと思います。
```

**ChatGPTの動作:**
1. フィードバックとして認識
2. `/api/v1/feedback` エンドポイントを呼び出し
3. 以下のデータを送信:
```json
{
  "user_id": "chatgpt_user",
  "category": "feature_request",
  "message": "TERASS Picksにスマホアプリ版があると外出先でも使いやすいと思います。",
  "context": {
    "source": "chatgpt",
    "timestamp": "2025-10-27T12:00:00"
  }
}
```

**期待される応答:**
```
貴重なご意見ありがとうございます！

以下の内容でフィードバックを記録しました:
- カテゴリ: 機能リクエスト
- 内容: TERASS Picksにスマホアプリ版があると外出先でも使いやすいと思います。
- フィードバックID: fb_20251027120000

ご意見は今後のサービス改善に活用させていただきます。
```

### 例4: 複数案件の一括計算

**ユーザー入力:**
```
以下の案件の報酬を計算してください:
1. 自己発見 500万円 (4月)
2. 本部送客 300万円 (5月)
3. TERASS Offer 400万円 (6月)
```

**ChatGPTの動作:**
```json
{
  "deals": [
    {"tax_excluded_fee": 5000000, "source": "self", "date": "2025-04-01"},
    {"tax_excluded_fee": 3000000, "source": "hq", "date": "2025-05-01"},
    {"tax_excluded_fee": 4000000, "source": "terass_offer", "date": "2025-06-01"}
  ]
}
```

**期待される応答:**
```
3件の案件の報酬計算結果です：

1. 自己発見 500万円 (4月)
   報酬: 375万円 (75%)
   年度累計: 500万円

2. 本部送客 300万円 (5月)
   報酬: 120万円 (40%)
   年度累計: 800万円

3. TERASS Offer 400万円 (6月)
   報酬: 220万円 (55%)
   年度累計: 1,200万円

合計報酬: 715万円

※年度累計が2,000万円を超えると、翌月からボーナスステージ
（自己発見90%）が適用されます。現在まであと800万円です。
```

## テスト用コマンド

### curl でのテスト

```bash
# 報酬計算
curl -X POST http://localhost:5000/api/v1/reward/calculate \
  -H "X-API-Token: terass-api-token-2025" \
  -H "Content-Type: application/json" \
  -d '{
    "deals": [
      {
        "tax_excluded_fee": 5000000,
        "source": "self",
        "date": "2025-04-01"
      }
    ]
  }'

# エージェントクラス判定
curl -X POST http://localhost:5000/api/v1/agent/class \
  -H "X-API-Token: terass-api-token-2025" \
  -H "Content-Type: application/json" \
  -d '{
    "region": "capital",
    "period_sales": 12000000,
    "cumulative_cases": 5
  }'

# フィードバック投稿
curl -X POST http://localhost:5000/api/v1/feedback \
  -H "X-API-Token: terass-api-token-2025" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test_user",
    "category": "feature_request",
    "message": "テスト用のフィードバックです"
  }'

# フィードバック一覧取得
curl -X GET "http://localhost:5000/api/v1/feedback?limit=10" \
  -H "X-API-Token: terass-api-token-2025"
```

## トラブルシューティング

### ChatGPTでAPIが呼べない場合

1. **サーバーが起動しているか確認**
   ```bash
   curl http://localhost:5000/api/v1/health
   ```

2. **認証トークンが正しいか確認**
   - ChatGPT Actionsの設定とサーバーの`API_TOKEN`環境変数が一致しているか

3. **OpenAPIスキーマが正しくインポートされているか確認**
   - ChatGPT Actionsの「Test」ボタンで各エンドポイントをテスト

4. **ネットワーク接続を確認**
   - ChatGPTから外部APIを呼ぶには、公開されたURLが必要
   - 開発環境では`ngrok`などのトンネリングツールを使用

### ngrokを使った公開例

```bash
# ngrokをインストール（https://ngrok.com/）
# アカウント登録してauthトークンを設定

# APIサーバーを公開
ngrok http 5000

# 表示されたURLをChatGPT Actionsに設定
# 例: https://abc123.ngrok.io
```

## セキュリティ注意事項

1. **本番環境では強力なAPI_TOKENを使用**
   ```bash
   export API_TOKEN=$(openssl rand -hex 32)
   ```

2. **HTTPSを使用**
   - 本番環境では必ずHTTPSで通信

3. **レート制限を実装**
   - 過度なリクエストを防ぐため

4. **ログ監査**
   - APIアクセスログを記録し、定期的にチェック

5. **個人情報の取り扱い**
   - フィードバックに個人情報が含まれる場合は適切に管理
