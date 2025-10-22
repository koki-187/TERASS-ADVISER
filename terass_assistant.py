import os
import tkinter as tk
from tkinter import scrolledtext, messagebox
from openai import OpenAI
from dotenv import load_dotenv
import datetime
import json

# 環境変数読み込み
load_dotenv()

# OpenAIクライアント初期化
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# TERASS業務マニュアル
TERASS_KNOWLEDGE = """
【TERASS業務サポートAI - ナレッジベース】

## 手付金預かり手順（14ステップ）
1. 本人確認 2. 契約書作成 3. 重説実施 4. 手付金確認 5. 預り証準備
6. 手付金受領 7. 預り証発行 8. TERASS Cloud登録 9. 保全措置確認
10. 本部報告 11. 記録保管 12. 決済日管理 13. 手付金充当 14. 完了報告

## TERASS Picks: 物件数284,096件、学区・ハザード対応
## Loan Checker: 107行対応、最低金利SBI新生0.520%
## Agent Class報酬: Beginner75%～Chairman90%
## 役所調査6大カテゴリー: 都市計画、建築基準法、道路、上下水道、埋蔵文化財、その他
"""

class ModernTERASSAssistant:
    def __init__(self, root):
        self.root = root
        self.root.title("TERASS業務サポートAI - Premium Edition")
        self.root.geometry("1000x750")
        self.root.configure(bg='#f0f2f5')
        
        # アイコン設定（Windows用）
        try:
            self.root.iconbitmap('terass_icon.ico')
        except:
            pass
        
        self.conversation_history = []
        self.message_widgets = []
        
        self.system_prompt = f"""TERASS不動産エージェント専用AIアシスタント（GPT-4o-mini版）

{TERASS_KNOWLEDGE}

具体的で実践的なアドバイスを、親しみやすく提供します。
"""
        
        self.setup_modern_ui()
        self.load_history()
    
    def setup_modern_ui(self):
        # ヘッダー（グラデーション風）
        header_frame = tk.Frame(self.root, bg='#2563eb', height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # タイトル
        title_label = tk.Label(
            header_frame,
            text="🏠 TERASS業務サポートAI",
            font=("Yu Gothic UI", 20, "bold"),
            bg='#2563eb',
            fg='white'
        )
        title_label.pack(pady=15)
        
        # サブタイトル
        subtitle_label = tk.Label(
            header_frame,
            text="powered by GPT-4o-mini  |  あなたの業務を24時間サポート",
            font=("Yu Gothic UI", 9),
            bg='#2563eb',
            fg='#93c5fd'
        )
        subtitle_label.place(x=20, y=50)
        
        # ステータスバー
        self.status_frame = tk.Frame(self.root, bg='#e0e7ff', height=30)
        self.status_frame.pack(fill=tk.X)
        
        self.status_label = tk.Label(
            self.status_frame,
            text="✓ 接続済み  |  会話数: 0",
            font=("Yu Gothic UI", 9),
            bg='#e0e7ff',
            fg='#1e40af',
            anchor='w'
        )
        self.status_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        # メインコンテナ
        main_container = tk.Frame(self.root, bg='#f0f2f5')
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # チャット表示エリア（カスタムキャンバス）
        chat_frame = tk.Frame(main_container, bg='white', relief=tk.FLAT)
        chat_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # スクロール可能なキャンバス
        self.canvas = tk.Canvas(chat_frame, bg='white', highlightthickness=0)
        scrollbar = tk.Scrollbar(chat_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg='white')
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # ウェルカムメッセージ
        self.add_welcome_message()
        
        # 入力エリア
        input_container = tk.Frame(main_container, bg='#f0f2f5')
        input_container.pack(fill=tk.X)
        
        # 入力フレーム（角丸風）
        input_frame = tk.Frame(input_container, bg='white', relief=tk.SOLID, bd=1)
        input_frame.pack(fill=tk.X)
        
        # 入力フィールド
        self.input_field = tk.Entry(
            input_frame,
            font=("Yu Gothic UI", 12),
            bg='white',
            fg='#1f2937',
            relief=tk.FLAT,
            insertbackground='#2563eb'
        )
        self.input_field.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=15, pady=12)
        self.input_field.bind("<Return>", lambda e: self.send_message())
        self.input_field.focus()
        
        # 送信ボタン（モダンスタイル）
        self.send_button = tk.Button(
            input_frame,
            text="送信 ✈",
            command=self.send_message,
            font=("Yu Gothic UI", 11, "bold"),
            bg='#2563eb',
            fg='white',
            relief=tk.FLAT,
            padx=25,
            pady=10,
            cursor="hand2",
            activebackground='#1d4ed8',
            activeforeground='white'
        )
        self.send_button.pack(side=tk.RIGHT, padx=10, pady=5)
        
        # ヒントラベル
        hint_label = tk.Label(
            input_container,
            text="💡 Enterキーで送信  |  Ctrl+Lで履歴クリア  |  Ctrl+Sで会話保存",
            font=("Yu Gothic UI", 8),
            bg='#f0f2f5',
            fg='#6b7280'
        )
        hint_label.pack(pady=(5, 0))
        
        # ショートカットキー
        self.root.bind('<Control-l>', lambda e: self.clear_chat())
        self.root.bind('<Control-s>', lambda e: self.save_history())
    
    def add_welcome_message(self):
        welcome_frame = tk.Frame(self.scrollable_frame, bg='white')
        welcome_frame.pack(fill=tk.X, padx=20, pady=20)
        
        icon_label = tk.Label(
            welcome_frame,
            text="🤖",
            font=("Segoe UI Emoji", 40),
            bg='white'
        )
        icon_label.pack()
        
        title = tk.Label(
            welcome_frame,
            text="TERASS業務サポートAIへようこそ！",
            font=("Yu Gothic UI", 16, "bold"),
            bg='white',
            fg='#1f2937'
        )
        title.pack(pady=(10, 5))
        
        subtitle = tk.Label(
            welcome_frame,
            text="AIがあなたの業務をサポートします。お気軽にご質問ください。",
            font=("Yu Gothic UI", 10),
            bg='white',
            fg='#6b7280'
        )
        subtitle.pack(pady=(0, 15))
        
        # クイック質問ボタン
        quick_frame = tk.Frame(welcome_frame, bg='white')
        quick_frame.pack(pady=10)
        
        quick_questions = [
            "📋 手付金預かりの手順",
            "🏢 TERASS Picksの機能",
            "💰 最低金利の銀行"
        ]
        
        for i, q in enumerate(quick_questions):
            btn = tk.Button(
                quick_frame,
                text=q,
                font=("Yu Gothic UI", 9),
                bg='#eff6ff',
                fg='#1e40af',
                relief=tk.FLAT,
                padx=15,
                pady=8,
                cursor="hand2",
                command=lambda question=q: self.quick_question(question)
            )
            btn.pack(side=tk.LEFT, padx=5)
    
    def quick_question(self, question):
        # ボタンからテキストを抽出して質問
        question_text = question.split(' ', 1)[1] + "を教えて"
        self.input_field.insert(0, question_text)
        self.send_message()
    
    def add_message_bubble(self, sender, message, is_user=False):
        # メッセージバブル
        bubble_container = tk.Frame(self.scrollable_frame, bg='white')
        bubble_container.pack(fill=tk.X, padx=20, pady=10)
        
        if is_user:
            # ユーザーメッセージ（右寄せ）
            bubble_frame = tk.Frame(bubble_container, bg='white')
            bubble_frame.pack(side=tk.RIGHT)
            
            avatar = tk.Label(
                bubble_frame,
                text="👤",
                font=("Segoe UI Emoji", 20),
                bg='white'
            )
            avatar.pack(side=tk.RIGHT, padx=(10, 0))
            
            message_frame = tk.Frame(bubble_frame, bg='#2563eb', relief=tk.FLAT)
            message_frame.pack(side=tk.RIGHT)
            
            message_label = tk.Label(
                message_frame,
                text=message,
                font=("Yu Gothic UI", 11),
                bg='#2563eb',
                fg='white',
                wraplength=500,
                justify=tk.LEFT,
                padx=15,
                pady=10
            )
            message_label.pack()
        else:
            # AIメッセージ（左寄せ）
            bubble_frame = tk.Frame(bubble_container, bg='white')
            bubble_frame.pack(side=tk.LEFT)
            
            avatar = tk.Label(
                bubble_frame,
                text="🤖",
                font=("Segoe UI Emoji", 20),
                bg='white'
            )
            avatar.pack(side=tk.LEFT, padx=(0, 10))
            
            message_frame = tk.Frame(bubble_frame, bg='#f3f4f6', relief=tk.FLAT)
            message_frame.pack(side=tk.LEFT)
            
            message_label = tk.Label(
                message_frame,
                text=message,
                font=("Yu Gothic UI", 11),
                bg='#f3f4f6',
                fg='#1f2937',
                wraplength=550,
                justify=tk.LEFT,
                padx=15,
                pady=10
            )
            message_label.pack()
            
            # タイムスタンプ
            timestamp = datetime.datetime.now().strftime('%H:%M')
            time_label = tk.Label(
                bubble_frame,
                text=timestamp,
                font=("Yu Gothic UI", 8),
                bg='white',
                fg='#9ca3af'
            )
            time_label.pack(side=tk.LEFT, padx=(10, 0))
        
        self.message_widgets.append(bubble_container)
        self.canvas.update_idletasks()
        self.canvas.yview_moveto(1.0)
    
    def send_message(self):
        user_message = self.input_field.get().strip()
        if not user_message:
            return
        
        # ユーザーメッセージ表示
        self.add_message_bubble("あなた", user_message, is_user=True)
        self.input_field.delete(0, tk.END)
        
        # ボタン無効化
        self.send_button.config(state=tk.DISABLED, text="応答中 ⏳")
        self.status_label.config(text="⏳ 応答生成中...")
        self.root.update()
        
        try:
            self.conversation_history.append({
                "role": "user",
                "content": user_message
            })
            
            messages = [
                {"role": "system", "content": self.system_prompt}
            ] + self.conversation_history[-10:]
            
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.7,
                max_tokens=2000
            )
            
            ai_response = response.choices[0].message.content
            
            # AI応答表示
            self.add_message_bubble("TERASS AI", ai_response, is_user=False)
            
            self.conversation_history.append({
                "role": "assistant",
                "content": ai_response
            })
            
            if len(self.conversation_history) > 20:
                self.conversation_history = self.conversation_history[-20:]
            
            # ステータス更新
            conv_count = len([m for m in self.conversation_history if m["role"] == "user"])
            self.status_label.config(text=f"✓ 接続済み  |  会話数: {conv_count}")
            
        except Exception as e:
            error_msg = f"エラーが発生しました:\n{str(e)}\n\n確認事項:\n1. インターネット接続\n2. APIキーの有効性"
            self.add_message_bubble("システム", error_msg, is_user=False)
            self.status_label.config(text="❌ エラー発生")
        
        finally:
            self.send_button.config(state=tk.NORMAL, text="送信 ✈")
            self.input_field.focus()
    
    def clear_chat(self):
        if messagebox.askyesno("確認", "会話履歴をクリアしますか？"):
            for widget in self.message_widgets:
                widget.destroy()
            self.message_widgets = []
            self.conversation_history = []
            self.add_welcome_message()
            self.status_label.config(text="✓ 接続済み  |  会話数: 0")
    
    def save_history(self):
        try:
            with open('chat_history.json', 'w', encoding='utf-8') as f:
                json.dump(self.conversation_history, f, ensure_ascii=False, indent=2)
            self.status_label.config(text="💾 会話を保存しました")
            self.root.after(2000, lambda: self.status_label.config(text="✓ 接続済み"))
        except Exception as e:
            messagebox.showerror("エラー", f"保存に失敗しました:\n{str(e)}")
    
    def load_history(self):
        try:
            if os.path.exists('chat_history.json'):
                with open('chat_history.json', 'r', encoding='utf-8') as f:
                    self.conversation_history = json.load(f)
        except:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernTERASSAssistant(root)
    root.mainloop()
