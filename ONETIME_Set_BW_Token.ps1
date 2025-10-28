Param([string]$ProjectId = $env:BWS_PROJECT_ID)
Write-Host "Bitwarden Secrets Manager のアクセストークンを入力してください（非表示）):" -ForegroundColor Cyan
$sec = Read-Host -AsSecureString
$tok = [Runtime.InteropServices.Marshal]::PtrToStringUni([Runtime.InteropServices.Marshal]::SecureStringToBSTR($sec))
if (-not $ProjectId) { $ProjectId = Read-Host "Bitwarden Project ID を入力してください" }
[Environment]::SetEnvironmentVariable("BWS_ACCESS_TOKEN", $tok, "User")
[Environment]::SetEnvironmentVariable("BWS_PROJECT_ID", $ProjectId, "User")
Write-Host "設定しました。再ログイン後に反映されます。" -ForegroundColor Green
