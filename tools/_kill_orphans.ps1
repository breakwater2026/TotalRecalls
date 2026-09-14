$procs = Get-CimInstance Win32_Process -Filter "name='msedgewebview2.exe'"
$kill = @()
foreach ($p in $procs) {
  $cl = $p.CommandLine
  if ($cl -and $cl -match 'login-webview-' -and $cl -match 'PerplexityExporter') {
    Write-Output ("KILL pid={0} parent={1} :: {2}" -f $p.ProcessId, $p.ParentProcessId, $cl.Substring(0,[Math]::Min(140,$cl.Length)))
    $kill += $p.ProcessId
  }
}
if ($kill.Count -gt 0) {
  Stop-Process -Id $kill -Force -ErrorAction SilentlyContinue
  Start-Sleep -Seconds 3
}
Write-Output ("killed_count=" + $kill.Count)
# test the lock
$d = Join-Path $env:APPDATA 'PerplexityExporter'
$ok = $false
foreach ($name in @('login-webview-chatgpt')) {
  $full = Join-Path $d $name
  if (Test-Path $full) {
    try {
      Rename-Item -LiteralPath $full -NewName ($name + '-T') -ErrorAction Stop
      Rename-Item -LiteralPath (Join-Path $d ($name + '-T')) -NewName $name -ErrorAction Stop
      $ok = $true
      Write-Output ("PROFILE " + $name + " UNLOCKED")
    } catch {
      Write-Output ("PROFILE " + $name + " STILL LOCKED")
    }
  } else {
    Write-Output ("PROFILE " + $name + " (folder absent)")
  }
}
