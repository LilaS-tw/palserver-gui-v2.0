# palserver GUI — v2.2.5

Hotfix:更新/重灌失敗的真兇修復 — 崩潰殘留的 CrashReportClient 鎖住伺服器檔案,現在會自動清除;安裝失敗直接顯示診斷輸出
Hotfix: the real culprit behind failing updates/reinstalls — a leftover CrashReportClient locking server files is now cleaned up automatically; install failures now show diagnostic output inline
Hotfix:更新/再インストール失敗の真因を修正 — クラッシュ後に残る CrashReportClient がファイルをロックする問題を自動解消;失敗時に診断出力を直接表示

> 有開自動更新會自己抓,或依下方手動下載。
> The in-app updater fetches it automatically, or download below.
> 自動更新で取得、または下記から手動でダウンロード。

<details>
<summary><b>🇹🇼 繁體中文</b></summary>

### 修正
- **更新/重灌一直失敗的真兇** — 伺服器崩潰後,UE 的崩潰回報程式(CrashReportClient.exe)或殭屍 PalServer 會殘留在背景鎖住遊戲檔案(如 `dbghelp.dll`);GUI 顯示「已停止」,但更新一開檔就失敗(`0xE0434352`)、重灌刪檔 `EPERM`。現在**更新/重灌前會自動找出並結束**這些鎖檔的殘留程序(記錄在日誌);若仍撞到鎖檔,錯誤訊息會直接指引「結束 CrashReportClient 或重開機」。
- **安裝失敗直接顯示死因** — 失敗訊息現在附上下載器輸出的尾段(含例外堆疊摘要),不用再翻日誌檔。

</details>

<details>
<summary><b>🇨🇳 简体中文</b></summary>

### 修复
- **更新/重装一直失败的真凶** — 服务器崩溃后,UE 的崩溃报告程序(CrashReportClient.exe)或僵尸 PalServer 会残留在后台锁住游戏档案(如 `dbghelp.dll`);GUI 显示「已停止」,但更新一开档就失败(`0xE0434352`)、重装删档 `EPERM`。现在**更新/重装前会自动找出并结束**这些锁档的残留程序(记录在日志);若仍撞到锁档,错误信息会直接指引「结束 CrashReportClient 或重启电脑」。
- **安装失败直接显示死因** — 失败信息现在附上下载器输出的尾段(含异常堆栈摘要),不用再翻日志档。

</details>

<details>
<summary><b>🇬🇧 English</b></summary>

### Fixes
- **The real culprit behind persistently failing updates/reinstalls** — after a server crash, UE's crash reporter (CrashReportClient.exe) or a zombie PalServer can linger in the background holding locks on game files (e.g. `dbghelp.dll`); the GUI shows "stopped", but updates fail on file open (`0xE0434352`) and reinstalls hit `EPERM`. Updates/reinstalls now **automatically find and terminate** these leftover file-locking processes (logged); if a lock is still hit, the error message points straight to "end CrashReportClient or reboot".
- **Install failures now show the cause inline** — the error message includes the tail of the downloader output (with the exception summary), no more digging through log files.

</details>

<details>
<summary><b>🇯🇵 日本語</b></summary>

### 修正
- **更新/再インストールが失敗し続ける真因** — サーバークラッシュ後、UE のクラッシュレポーター(CrashReportClient.exe)やゾンビ PalServer がバックグラウンドに残り、ゲームファイル(`dbghelp.dll` など)をロックすることがあります。GUI は「停止中」と表示しますが、更新はファイルオープンで失敗(`0xE0434352`)、再インストールは `EPERM` になります。更新/再インストール前に**これらの残留プロセスを自動検出して終了**するようにしました(ログに記録)。それでもロックに当たる場合は「CrashReportClient を終了するか再起動」と明確に案内します。
- **インストール失敗時に原因を直接表示** — エラーメッセージにダウンローダー出力の末尾(例外の要約含む)を添付。ログファイルを掘る必要はもうありません。

</details>
