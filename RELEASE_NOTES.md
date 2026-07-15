# palserver GUI — v2.2.1

存檔深度整合大版本:玩家/公會完整檔案(離線可查)、存檔健檢、重灌伺服器選項、共玩存檔問題自動修復
Deep save integration: full player/guild profiles (works offline), save health check, server reinstall option, automatic co-op save fixes
セーブ深掘り統合版:プレイヤー/ギルドの完全プロフィール(オフライン対応)、セーブ健康診断、サーバー再インストール、協力プレイセーブの自動修復

> 有開自動更新會自己抓,或依下方手動下載。
> The in-app updater fetches it automatically, or download below.
> 自動更新で取得、または下記から手動でダウンロード。

<details>
<summary><b>🇹🇼 繁體中文</b></summary>

### 新功能
- **玩家詳情全面升級** — 即時資料(PalDefender)與存檔資料合併成同一視圖,**離線玩家也能查**、不依賴 PalDefender。帕魯依位置分頁(身上/帕魯箱/據點)+ 名稱/物種/詞條即時搜尋;公會據點清單可一鍵跳到地圖。右上角「詳細資訊 ★」開關(贊助者):個體值、詞條、星級、離線背包/武器/防具/金錢、加點分配、進度與科技。
- **公會分頁(新)** — 公會清單與詳情彈窗:成員與最後上線、據點座標跳地圖(免費);詳細資訊(贊助者):據點駐守帕魯、公會倉庫內容、研究進度(三語名稱)。
- **存檔健檢(贊助者)** — 存檔備份頁一鍵分析世界存檔:組成大小、空公會、不活躍玩家、已搜刮容器殘留、掉落物統計 —— 判斷存檔是否肥大。分析工具首次使用自動下載,全程唯讀不動存檔。
- **重灌伺服器** — 更新一直失敗?遊戲版本卡新增「重灌伺服器」:刪除遊戲本體後全新下載,**世界存檔與設定檔(整個 Pal/Saved)完整保留**,開始前自動備份;模組需重新安裝。
- **共玩(四人)存檔自動修復** — 匯入時自動停用殘留的 WorldOptions.sav(修「世界設定不生效/管理員密碼不符」);「共玩修復」一併把帕魯過戶給新角色,已修復過的世界也能單獨過戶帕魯歸屬。
- **世界設定同步** — 直接編輯 PalWorldSettings.ini(含外部編輯器),面板現在會自動同步顯示,不會再被下次啟動蓋掉(docker 也支援)。
- **首頁進階顯示(贊助者)** — 卡片顯示在線玩家/伺服器 FPS/CPU/記憶體/影格時間 + 全伺服器加總總覽。
- **地圖強化** — 點玩家先開小卡(基礎資訊+操作選單),公會據點圖層開放所有人使用;操作選單新增「傳送到此玩家位置」(贊助者)。
- **指令台「清理」分類** — killnearestbase/deletepals/clearinv 等除肥指令集中一處,附用途說明;世界設定 8 個效能鍵附建議值提示。
- **圖鑑補完** — 人類 NPC 目錄(432 筆三語+頭像,獵人/入侵者不再顯示內部代號)、公會研究名稱三語、修復傑諾貝達等 14 隻帕魯圖示。

### 修正
- 在線玩家的詞條/個體值無法顯示(跨資料來源以 InstanceId 精準對聯)。
- 離線天數改以存檔內世界時鐘計算(與社群工具一致)。
- 玩家詳情在平台不支援/快照缺失時顯示明確原因,不再出現無反應的按鈕。
- mods 頁在 Linux/macOS 明示 UE4SS/PalDefender 僅支援 Windows。

### 其他
- 贊助者先行版功能改為永久贊助者專屬(原「到期後開放」機制取消)。

</details>

<details>
<summary><b>🇨🇳 简体中文</b></summary>

### 新功能
- **玩家详情全面升级** — 实时资料(PalDefender)与存档资料合并成同一视图,**离线玩家也能查**、不依赖 PalDefender。帕鲁按位置分页(身上/帕鲁箱/据点)+ 名称/物种/词条即时搜索;公会据点清单可一键跳到地图。右上角「详细资讯 ★」开关(赞助者):个体值、词条、星级、离线背包/武器/防具/金钱、加点分配、进度与科技。
- **公会分页(新)** — 公会清单与详情弹窗:成员与最后上线、据点坐标跳地图(免费);详细资讯(赞助者):据点驻守帕鲁、公会仓库内容、研究进度(三语名称)。
- **存档健检(赞助者)** — 存档备份页一键分析世界存档:组成大小、空公会、不活跃玩家、已搜刮容器残留、掉落物统计 —— 判断存档是否肥大。分析工具首次使用自动下载,全程只读不动存档。
- **重装服务器** — 更新一直失败?游戏版本卡新增「重装服务器」:删除游戏本体后全新下载,**世界存档与设定档(整个 Pal/Saved)完整保留**,开始前自动备份;模组需重新安装。
- **联机(四人)存档自动修复** — 导入时自动停用残留的 WorldOptions.sav(修「世界设定不生效/管理员密码不符」);「联机修复」一并把帕鲁过户给新角色,已修复过的世界也能单独过户帕鲁归属。
- **世界设定同步** — 直接编辑 PalWorldSettings.ini(含外部编辑器),面板现在会自动同步显示,不会再被下次启动覆盖(docker 也支持)。
- **首页进阶显示(赞助者)** — 卡片显示在线玩家/服务器 FPS/CPU/内存/帧时间 + 全服务器加总总览。
- **地图强化** — 点玩家先开小卡(基础资料+操作菜单),公会据点图层开放所有人使用;操作菜单新增「传送到此玩家位置」(赞助者)。
- **指令台「清理」分类** — killnearestbase/deletepals/clearinv 等除肥指令集中一处,附用途说明;世界设定 8 个性能键附建议值提示。
- **图鉴补完** — 人类 NPC 目录(432 笔三语+头像,猎人/入侵者不再显示内部代号)、公会研究名称三语、修复杰诺贝达等 14 只帕鲁图标。

### 修复
- 在线玩家的词条/个体值无法显示(跨资料来源以 InstanceId 精准对联)。
- 离线天数改以存档内世界时钟计算(与社群工具一致)。
- 玩家详情在平台不支持/快照缺失时显示明确原因,不再出现无反应的按钮。
- mods 页在 Linux/macOS 明示 UE4SS/PalDefender 仅支持 Windows。

### 其他
- 赞助者先行版功能改为永久赞助者专属(原「到期后开放」机制取消)。

</details>

<details>
<summary><b>🇬🇧 English</b></summary>

### New
- **Player details, fully upgraded** — live data (PalDefender) and save data merged into one view; **works for offline players**, no PalDefender required. Pals grouped by location (party / palbox / base) with instant search by name, species, or passive; guild base list with jump-to-map. New "Details ★" toggle in the top-right (sponsor): IVs, passives, star rank, offline inventory / weapons / armor / money, stat-point allocation, progression & tech.
- **Guilds tab (new)** — guild list and detail modal: members with last-online, base coordinates with jump-to-map (free); details (sponsor): working pals per base, guild storage contents, research progress (localized names).
- **Save health check (sponsor)** — one click on the Saves tab analyzes the world save: composition size, empty guilds, inactive players, looted-container residue, drop items — to judge save bloat. The analysis tool downloads automatically on first use; strictly read-only.
- **Reinstall server** — updates keep failing? The version card gains "Reinstall Server": deletes the game files and downloads fresh, **keeping world saves and configs (the entire Pal/Saved) intact**, with an automatic backup first; mods need reinstalling.
- **Automatic co-op save fixes** — importing now auto-disables the leftover WorldOptions.sav (fixes "world settings not applying / admin password mismatch"); the co-op repair also transfers pal ownership to the new character, and already-repaired worlds can transfer pal ownership on its own.
- **World-settings sync** — editing PalWorldSettings.ini directly (external editors too) now syncs into the panel instead of being overwritten on next launch (docker included).
- **Dashboard advanced view (sponsor)** — cards show online players / server FPS / CPU / memory / frame time, plus an all-servers totals board.
- **Map upgrades** — clicking a player opens a compact card (basics + actions menu); the guild-bases layer is now free for everyone; new "Teleport to this player" action (sponsor).
- **Console "Cleanup" category** — killnearestbase / deletepals / clearinv and friends in one place with usage notes; 8 performance keys in world settings show suggested values.
- **Catalog completeness** — human NPC catalog (432 entries, localized, with portraits — hunters/invaders no longer show internal IDs), localized guild research names, and 14 broken pal icons fixed (Xenovader et al.).

### Fixes
- Passives/IVs now show for online players (precise cross-source join by InstanceId).
- Days-offline now uses the save's world clock (matching community tools).
- Player details show clear reasons when the platform is unsupported or the snapshot is missing — no more dead buttons.
- The mods page states clearly that UE4SS/PalDefender are Windows-only on Linux/macOS hosts.

### Other
- Sponsor early-access features are now permanently sponsor-only (the "free after expiry" mechanism is removed).

</details>

<details>
<summary><b>🇯🇵 日本語</b></summary>

### 新機能
- **プレイヤー詳細を全面刷新** — リアルタイム情報(PalDefender)とセーブデータを一つのビューに統合。**オフラインのプレイヤーも閲覧可**、PalDefender 不要。パルは所在別タブ(手持ち/パルボックス/拠点)+ 名前・種族・パッシブの即時検索;ギルド拠点はマップへジャンプ。右上の「詳細情報 ★」トグル(スポンサー):個体値・パッシブ・ランク・オフライン所持品/武器/防具/所持金・ステータス振り分け・進捗と技術。
- **ギルドタブ(新設)** — ギルド一覧と詳細モーダル:メンバーと最終ログイン、拠点座標のマップジャンプ(無料);詳細情報(スポンサー):拠点の作業パル、ギルド倉庫の中身、研究進捗(ローカライズ名)。
- **セーブ健康診断(スポンサー)** — セーブ/バックアップタブからワンクリックでワールドセーブを分析:構成サイズ、空ギルド、非アクティブプレイヤー、回収済みコンテナ残留、ドロップ品 —— 肥大化の判断に。分析ツールは初回に自動ダウンロード、完全読み取り専用。
- **サーバー再インストール** — 更新が失敗し続けるときに:ゲーム本体を削除して新規ダウンロード。**ワールドセーブと設定(Pal/Saved 全体)は完全保持**、開始前に自動バックアップ;MOD は再導入が必要。
- **協力プレイセーブの自動修復** — インポート時に残留 WorldOptions.sav を自動無効化(「ワールド設定が反映されない/管理者パスワード不一致」を修正);ホスト修復でパルの所有者も一括移行、修復済みワールドでも所有者移行を単独実行可能。
- **ワールド設定の同期** — PalWorldSettings.ini を直接編集(外部エディタ含む)しても、パネルに自動反映され、次回起動で上書きされません(docker 対応)。
- **ダッシュボード拡張表示(スポンサー)** — カードにオンライン人数/サーバー FPS/CPU/メモリ/フレーム時間 + 全サーバー合計ボード。
- **マップ強化** — プレイヤーをクリックするとまず小カード(基本情報+操作メニュー);ギルド拠点レイヤーは全員無料に;「このプレイヤーの位置へ転送」を追加(スポンサー)。
- **コンソール「クリーンアップ」カテゴリ** — killnearestbase / deletepals / clearinv などの軽量化コマンドを一箇所に集約、用途説明つき;ワールド設定のパフォーマンス 8 項目に推奨値ヒント。
- **図鑑の補完** — 人間 NPC カタログ(432 件・多言語・ポートレート付き。ハンター/侵入者が内部 ID 表示にならない)、ギルド研究名の多言語化、ゼノベーダなど 14 体のパルアイコン修復。

### 修正
- オンラインプレイヤーのパッシブ/個体値が表示されない問題(InstanceId によるソース間の正確な突合)。
- オフライン日数をセーブ内のワールド時計基準に(コミュニティツールと一致)。
- プラットフォーム未対応/スナップショット欠如時に明確な理由を表示(反応しないボタンを排除)。
- MOD ページで UE4SS/PalDefender が Windows 専用であることを Linux/macOS ホストに明示。

### その他
- スポンサー先行機能は恒久的にスポンサー限定に(「期限後に無料開放」の仕組みは廃止)。

</details>
