# palserver GUI — v2.4.0

新手開服重設計(建立精靈/埠防撞/邀請朋友)、帕魯數值調整大升級(原版值/工作適性/熱重載)、模組改版日生存包(停用不刪檔/新版偵測)、Wine 與 Kubernetes 支援;修更新後前端 404 與 CPU 顯示
Onboarding redesign (wizard / port guard / invite friends), pal stats overhaul (vanilla values / work suitability / hot reload), mod survival kit (disable without deleting / update detection), Wine & Kubernetes support; fixes the post-update 404 and CPU readings
初心者向けサーバー作成の刷新(ウィザード/ポート保護/フレンド招待)、パルステータス編集の大幅強化(バニラ値/作業適性/ホットリロード)、モッド延命キット(無効化/新版検出)、Wine と Kubernetes 対応。更新後の 404 と CPU 表示を修正

> 有開自動更新會自己抓,或依下方手動下載。
> The in-app updater fetches it automatically, or download below.
> 自動更新で取得、または下記から手動でダウンロード。

<details>
<summary><b>🇹🇼 繁體中文</b></summary>

### 新功能
- **新手開服重設計** — 建立精靈三步驟(基本資料 → 玩法預設檔:官方/休閒/硬核 → 原生 vs 強化模組),建立完成直接進入伺服器頁;啟動前自動偵測五種埠(遊戲/查詢/RCON/REST/反作弊插件)被占用即跳修改面板;建立時自動分配未使用的遊戲埠;新伺服器預設啟用 RCON(自動產生管理員密碼與唯一埠)。
- **邀請朋友加入** — 總覽新卡片三選一:playit.gg(白話三步教學+教學影片連結)/ VPN(Radmin/Tailscale)/ 直連(公開 IP 預設馬賽克,點眼睛顯示);附「朋友這樣加入」遊戲內操作指引。
- **分頁自由化** — 每台伺服器獨立的分頁顯示與**拖曳排序**;分頁列尾端「＋」管理面板一鍵開關分頁、恢復預設;原味伺服器預設精簡五頁,強化版多出玩家/公會/地圖等分頁。
- **帕魯數值調整大升級**(贊助者) — 輸入框顯示**原版數值**(657 個資料列,含首領/塔主變體);**工作適性**13 項可調;×0.5/×2 倍率快捷;已修改清單顯示「原版 → 新值 (+%)」;PalSchema 一鍵更新;**熱重載**:伺服器運行中儲存即生效(對新遭遇帕魯);自動校正首領資料列大小寫(修正絕大多數 BOSS_ 首領版原本寫不進的問題)。
- **模組改版日生存包** — UE4SS / 反作弊插件 / PalSchema 三卡皆可「**停用**」(保留全部檔案,Lua 模組與設定不刪);已裝版本落後時顯示「**有新版**」徽章;更新遊戲本體前提醒模組可能暫時不相容。
- **出事時說人話** — 伺服器意外停止(閃退)顯示醒目橫幅與可能原因;連續崩潰達上限暫停自動重啟時明確提示;錯誤訊息附「查看日誌」;日誌新增過濾(全部/錯誤與警告/聊天與事件)與智慧捲動(回看時不再被拉到底部)。
- **自動化** — 自動備份預設啟用(每小時);「開機自動啟動 agent」(Windows)搭配每伺服器「自動啟動」= 主機開機即開服;停機倒數中按鈕變「**立即停止**」可跳過倒數;強化版建立自動開啟反作弊插件 REST API 並配好權杖。
- **Wine 與 Kubernetes 支援**(感謝 @teps3105,PR #36) — docker 可用 Wine 執行 Windows 版伺服器(反作弊插件因此可用),並支援 K8s 叢集內的模組/PalSchema 安裝。
- **配置評估健檢**(贊助者) — 首頁進階顯示擴充:主機硬體與網路實測評分。
- **介面打磨** — 世界設定(118 項)與反作弊插件(45+ 項)新增**搜尋**;危險選項黃色警告(硬核/帕魯永久死亡/關 RCON·REST 會斷 GUI 功能);白名單未啟用提示與空名單警告;還原備份確認顯示會回溯多少進度;離線玩家名冊可直接封鎖/解除;learntech/unlearntech 指令加科技目錄搜尋下拉(感謝 @UCKETX);空狀態提示統一虛線風格;廣播移到日誌下方;右下角貓貓可在設定關閉。

### 修正
- **更新 agent 後前端 404** — 自我更新換檔流程加固(staging + 原子替換)並新增啟動自癒(殘留的 web.old 自動救回)。
- **CPU 使用率亂跳/歸零** — 棄用 pidusage 的 cpu 欄位改自算差分。
- 分頁拖曳中字體不再忽大忽小;「翻譯」開啟時星星圖示不再被同色蓋住;帕魯數值調整分頁不再被誤踢回總覽;系統匣不再鎖住 logo.png;公會/排行榜無法取得快照時的重複提示與版面。

</details>

<details>
<summary><b>🇨🇳 简体中文</b></summary>

### 新功能
- **新手开服重设计** — 创建向导三步骤(基本资料 → 玩法预设:官方/休闲/硬核 → 原生 vs 强化模组),创建完成直接进入服务器页;启动前自动检测五种端口被占用即弹修改面板;创建时自动分配未使用的游戏端口;新服务器默认启用 RCON(自动生成管理员密码与唯一端口)。
- **邀请朋友加入** — 总览新卡片三选一:playit.gg(白话三步教程+教学视频链接)/ VPN / 直连(公开 IP 默认打码);附「朋友这样加入」游戏内操作指引。
- **标签页自由化** — 每台服务器独立的标签显示与**拖拽排序**;「＋」管理面板一键开关标签、恢复默认;原味服务器默认精简五页。
- **帕鲁数值调整大升级**(赞助者) — 输入框显示**原版数值**(657 个数据行,含首领/塔主变体);**工作适性** 13 项可调;×0.5/×2 倍率快捷;已修改清单显示「原版 → 新值 (+%)」;PalSchema 一键更新;**热重载**:服务器运行中保存即生效;自动校正首领数据行大小写(修正 BOSS_ 首领版原本写不进的问题)。
- **模组改版日生存包** — UE4SS / 反作弊插件 / PalSchema 三卡皆可「**停用**」(保留文件不删);版本落后显示「**有新版**」徽章;更新游戏前提醒模组可能暂时不兼容。
- **出事时说人话** — 服务器意外停止显示醒目横幅与可能原因;连续崩溃熔断明确提示;错误信息附「查看日志」;日志新增过滤与智能滚动。
- **自动化** — 自动备份默认启用;「开机自动启动 agent」搭配每服务器「自动启动」= 主机开机即开服;停机倒数中可「**立即停止**」;强化版自动开启反作弊插件 REST API 并配好令牌。
- **Wine 与 Kubernetes 支持**(感谢 @teps3105,PR #36) — docker 可用 Wine 运行 Windows 版服务器(反作弊插件因此可用),并支持 K8s 集群内的模组/PalSchema 安装。
- **配置评估健检**(赞助者)与界面打磨 — 世界设置/反作弊插件**搜索**、危险选项警告、白名单防呆、还原备份回溯提示、离线玩家可封锁、科技目录搜索下拉(感谢 @UCKETX)、空状态统一风格等。

### 修复
- **更新 agent 后前端 404** — 换档流程加固(staging+原子替换)+启动自愈。
- **CPU 使用率乱跳/归零** — 改自算差分。
- 标签拖拽字体缩放、翻译星星同色、帕鲁数值页误踢回总览、系统托盘锁 logo.png、公会/排行榜快照提示重复等。

</details>

<details>
<summary><b>🇬🇧 English</b></summary>

### New
- **Onboarding redesign** — 3-step creation wizard (basics → gameplay presets: official/casual/hardcore → vanilla vs enhanced mods) that lands you straight in the new server page; pre-start detection of all five ports (game/query/RCON/REST/anti-cheat) with a fix-it panel; automatic free game-port assignment; RCON enabled by default with a generated admin password and unique port.
- **Invite friends** — new overview card with three paths: playit.gg (plain-language steps + tutorial link) / VPN (Radmin/Tailscale) / direct (public IP masked by default); includes in-game joining instructions for your friends.
- **Tab freedom** — per-server tab visibility and **drag-to-reorder**; a "+" manager panel to toggle tabs and reset defaults; vanilla servers start with a lean five tabs.
- **Pal stats overhaul** (sponsors) — inputs show **vanilla values** (657 rows incl. boss/tower variants); **13 work-suitability** fields; ×0.5/×2 shortcuts; "vanilla → new (+%)" comparison; one-click PalSchema update; **hot reload** (saves apply while the server runs); automatic boss-row case correction (fixes BOSS_ variants that previously never applied).
- **Mod survival kit** — UE4SS / anti-cheat plugin / PalSchema can all be **disabled without deleting** anything (Lua mods and configs are kept); "update available" badges; game updates now warn about mod compatibility first.
- **Plain-spoken failures** — a clear banner when the server stops unexpectedly; explicit notice when crash-loop protection pauses auto-restart; errors link to logs; log filtering (errors/chat) and smart auto-scroll.
- **Automation** — scheduled backups on by default (hourly); "start agent on boot" (Windows) plus per-server "auto start" = servers come up with the machine; "**Stop now**" skips the shutdown countdown; enhanced servers get the anti-cheat REST API pre-configured with a token.
- **Wine & Kubernetes support** (thanks @teps3105, PR #36) — run the Windows server binary under Wine in docker (enabling the anti-cheat plugin), plus in-cluster mod/PalSchema installs for K8s.
- **Setup review** (sponsors) and polish — settings **search** (world & anti-cheat), dangerous-option warnings, whitelist safeguards, restore-rollback estimates, offline-player banning, tech-catalog dropdown for learntech (thanks @UCKETX), unified empty states, and more.

### Fixes
- **Post-update 404** — hardened self-update swap (staging + atomic rename) with startup self-healing for stranded web folders.
- **CPU readings jumping/zeroing** — replaced pidusage's cpu field with self-computed deltas.
- Tab-drag font scaling, translate-star contrast, pal-stats tab bounce, tray icon locking logo.png, duplicated guild/leaderboard hints, and more.

</details>

<details>
<summary><b>🇯🇵 日本語</b></summary>

### 新機能
- **サーバー作成の刷新** — 3 ステップウィザード(基本情報 → プリセット:公式/カジュアル/ハードコア → バニラ vs 強化モッド)。作成後はそのままサーバーページへ。起動前に 5 種のポート占有を検出して修正パネルを表示。ゲームポートの自動割当。RCON をデフォルト有効化(管理者パスワード自動生成+固有ポート)。
- **フレンド招待** — 3 つの方法(playit.gg のやさしい 3 ステップ+チュートリアルリンク / VPN / 直結・公開 IP はデフォルトでマスク)。フレンド側のゲーム内参加手順も案内。
- **タブの自由化** — サーバーごとのタブ表示と**ドラッグ並べ替え**。「＋」パネルでオンオフと初期化。バニラサーバーはすっきり 5 タブから。
- **パルステータス編集の大幅強化**(スポンサー) — 入力欄に**バニラ値**を表示(ボス/タワー変種含む 657 行)。**作業適性** 13 項目。×0.5/×2 ショートカット。「バニラ → 新値 (+%)」比較。PalSchema ワンクリック更新。**ホットリロード**(稼働中でも保存即反映)。ボス行の大文字小文字を自動補正(BOSS_ 変種が反映されなかった問題を修正)。
- **モッド延命キット** — UE4SS / アンチチート / PalSchema を**削除せず無効化**可能(Lua モッドや設定は保持)。「新バージョンあり」バッジ。ゲーム更新前にモッド互換性を警告。
- **わかりやすい障害通知** — 予期せぬ停止のバナー、クラッシュループ保護の明示、ログへのリンク、ログフィルタとスマートスクロール。
- **自動化** — 自動バックアップをデフォルト有効化。「起動時に agent を自動開始」+サーバーごとの「自動起動」でマシン起動と同時に開服。カウントダウン中の「**今すぐ停止**」。強化版はアンチチートの REST API とトークンを自動設定。
- **Wine と Kubernetes 対応**(@teps3105 さん、PR #36) — docker で Windows バイナリを Wine 実行(アンチチート利用可能に)。K8s クラスタ内のモッド/PalSchema インストールにも対応。
- **構成レビュー**(スポンサー)と磨き込み — 設定**検索**、危険設定の警告、ホワイトリスト保護、復元時のロールバック量表示、オフラインプレイヤーの BAN、テクノロジー検索ドロップダウン(@UCKETX さん)など。

### 修正
- **更新後にフロントエンドが 404** — 自己更新の入れ替えを強化(ステージング+アトミック置換)し、起動時の自己修復を追加。
- **CPU 使用率の乱高下/ゼロ表示** — 自前の差分計算に変更。
- タブドラッグ中のフォント変化、翻訳スターの視認性、パルステータスタブの誤リダイレクト、トレイアイコンの logo.png ロックなど。

</details>
