# ワンタップ起動ガイド (Windows / Mac)

このアプリは Bitwarden Secrets Manager にある秘密情報を「実行時だけ」読み込む安全設計です。  
「ワンタップ」はダブルクリックで起動できることを意味し、OS別に起動ファイルを用意しました。

## Windows

1. `RUN_Terass_Assistant.cmd` をダブルクリック  
2. 初回のみ `ONETIME_Set_BW_Token.ps1` を実行し、BWS_ACCESS_TOKEN と BWS_PROJECT_ID を登録  
3. 以降は入力不要でそのまま起動します

## macOS

1. `RUN_Terass_Assistant.command` をダブルクリック  
2. 初回のみトークン保存し `~/.terass/bw.env` に保存（600権限）  
3. 以降はそのまま起動します

> 補足：Bitwarden とは秘密のメモ帳です。APIキーやパスワードを暗号化保管し、`bws run --project-id` で実行中だけ環境変数にしてくれます。
