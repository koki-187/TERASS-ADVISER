@echo off
setlocal
REM ===== Desktop One-Tap Start (Windows) =====
where /q bws || (echo [ERROR] bws (Bitwarden Secrets Manager CLI) が必要です & pause & exit /b 1)
where /q py  || where /q python || (echo [ERROR] Python 3 が必要です & pause & exit /b 1)

if not exist .venv (
  echo [SETUP] 仮想環境を作成...
  py -3 -m venv .venv 2>nul || python -m venv .venv
)
call .venv\Scripts\python -m pip -q install --upgrade pip
if exist requirements.txt call .venv\Scripts\pip -q install -r requirements.txt

REM --- BWS_PROJECT_ID が未設定なら促す（トークンは OS へ設定模子想） ---
if "%BWS_PROJECT_ID%"=="" (
  echo [INFO] BWS_PROJECT_ID が未設定です。Bitwarden の Project ID を環境変数に設定して下さい。
  pause & exit /b 1
)

echo [RUN] ワンタップ起動（Bitwardenから秘密を注入）...
bws run --project-id %BWS_PROJECT_ID% -- ".venv\Scripts\python.exe" "terass_assistant_with_scenarios.py"
