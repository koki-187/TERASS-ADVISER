import os
import tkinter as tk
from tkinter import scrolledtext
from openai import OpenAI
from dotenv import load_dotenv
import datetime

# 環境変数読み込み
load_dotenv()

# OpenAIクライアント初期化
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# TERASS業務マニュアル
TERASS_KNOWLEDGE = """
【TERASS業務サポートAI - ナレッジベース】

## 手付金預かり手順（14ステップ）
1. 本人確認
2. 契約書作成
3. 重説実施
4. 手付金確認
5. 預り証準備
6. 手付金受領
7. 預り証発行
8. TERASS Cloud登録
9. 保全措置確認
10. 本部報告
11. 記録保管
12. 決済日管理
13. 手付金充当
14. 完了報告

## TERASS Picks
- 物件数: 284,096件
- 学区・ハザード情報対応

## Loan Checker
- 対応銀行: 107行
- 最低金利: SBI新生 0.520%

## Agent Class報酬
Beginner:75% Bronze:76% Silver:78% Gold:80% 
Platinum:82% Diamond:84% Master:86% Grand Master:87%
Legend:88% Champion:89% Chairman:90%

## 役所調査6大カテゴリー
1.都市計画 2.建築基準法 3.道路 4.上下水道 5.埋蔵文化財 6.その他制限
"""

class TERASSAssistant:
    def __init__(self, root):
        self.root = root
        self.root.title("TERASS業務サポートAI")
        self.root.geometry("900x700")
        self.conversation_history = []
        self.system_prompt = f"""TERASS不動産エージェント専用AIアシスタントです。

{TERASS_KNOWLEDGE}

具体的で実践的なアドバイスを提供します。
"""
        self.setup_ui()
    
    def setup_ui(self):
        title_label = tk.Label(self.root, text="TERASS業務サポートAI", font=("Yu Gothic UI", 16, "bold"), bg="#2d6bb5", fg="white", pady=10)
        title_label.pack(fill=tk.X)
        
        self.chat_display = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=100, height=35, font=("Yu Gothic UI", 10), bg="#f5f5f5")
        self.chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        input_frame = tk.Frame(self.root)
        input_frame.pack(padx=10, pady=(0, 10), fill=tk.X)
        
        self.input_field = tk.Entry(input_frame, font=("Yu Gothic UI", 11))
        self.input_field.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.input_field.bind("<Return>", lambda e: self.send_message())
        
        self.send_button = tk.Button(input_frame, text="送信", command=self.send_message, font=("Yu Gothic UI", 10, "bold"), bg="#2d6bb5", fg="white", padx=20)
        self.send_button.pack(side=tk.RIGHT)
        
        welcome_msg = """TERASS業務サポートAI（GPT-4o版）

質問例:
・手付金預かりの手順を教えて
・TERASS Picksの機能は？
・最低金利の銀行はどこ？

お気軽にご質問ください！"""
        self.add_message("システム", welcome_msg)
    
    def add_message(self, sender, message):
        timestamp = datetime.datetime.now().strftime('%H:%M:%S')
        self.chat_display.insert(tk.END, f"\n[{timestamp}] {sender}\n{message}\n")
        self.chat_display.see(tk.END)
    
    def send_message(self):
        user_message = self.input_field.get().strip()
        if not user_message:
            return
        
        self.add_message("あなた", user_message)
        self.input_field.delete(0, tk.END)
        
        self.send_button.config(state=tk.DISABLED, text="応答中...")
        self.root.update()
        
        try:
            self.conversation_history.append({"role": "user", "content": user_message})
            messages = [{"role": "system", "content": self.system_prompt}] + self.conversation_history[-10:]
            
            response = client.chat.completions.create(model="gpt-4o-mini", messages=messages, temperature=0.7, max_tokens=2000)
            
            ai_response = response.choices[0].message.content
            self.add_message("TERASS AI", ai_response)
            
            self.conversation_history.append({"role": "assistant", "content": ai_response})
            
            if len(self.conversation_history) > 20:
                self.conversation_history = self.conversation_history[-20:]
        except Exception as e:
            error_msg = f"エラー: {str(e)}\n\n確認事項:\n1. .envファイルのAPIキー\n2. インターネット接続"
            self.add_message("エラー", error_msg)
        finally:
            self.send_button.config(state=tk.NORMAL, text="送信")
            self.input_field.focus()

if __name__ == "__main__":
    root = tk.Tk()
    app = TERASSAssistant(root)
    root.mainloop()
