'use client';

import { useEffect, useMemo, useRef, useState } from 'react';
import { useSearchParams } from 'next/navigation';
import dynamic from 'next/dynamic';
import { getMapDict, pickMapLang, type MapLang } from './i18n';
import type { MapSnapshotV1, MapWorld, SnapshotApiResponse, StaticLandmark } from './types';

const LeafletMap = dynamic(() => import('./LeafletMap'), { ssr: false });

const PRIMARY_BASE = 'https://stats.iosoftware.ai';
const BACKUP_BASE = 'https://palserver-stats.iosoftware.workers.dev';
const POLL_MS = 20_000;
const STALE_MS = 5 * 60 * 1000;

type LoadStatus = 'loading' | 'ok' | 'not-found' | 'missing-id' | 'error';

type FetchResult =
  | { status: 'ok'; data: SnapshotApiResponse }
  | { status: 'not-found' }
  | { status: 'error'; message: string };

/** 主端點失敗(非 404)才試備援;帶 ?api= 覆寫時只打那一個 base,不自動兜底
 * (本機聯測 / 未來 agent 直連模式要能精準指到單一端點)。 */
async function fetchSnapshot(id: string, apiOverride: string | null): Promise<FetchResult> {
  const askOnce = (base: string) =>
    fetch(`${base}/api/map/snapshot?id=${encodeURIComponent(id)}`, { cache: 'no-store' });

  const primary = apiOverride || PRIMARY_BASE;
  try {
    const res = await askOnce(primary);
    if (res.status === 404) return { status: 'not-found' };
    if (res.ok) return { status: 'ok', data: (await res.json()) as SnapshotApiResponse };
    if (apiOverride) return { status: 'error', message: `HTTP ${res.status}` };
  } catch (err) {
    if (apiOverride) return { status: 'error', message: err instanceof Error ? err.message : String(err) };
  }
  if (apiOverride) return { status: 'error', message: 'unreachable' };

  try {
    const res = await askOnce(BACKUP_BASE);
    if (res.status === 404) return { status: 'not-found' };
    if (res.ok) return { status: 'ok', data: (await res.json()) as SnapshotApiResponse };
    return { status: 'error', message: `HTTP ${res.status}` };
  } catch (err) {
    return { status: 'error', message: err instanceof Error ? err.message : String(err) };
  }
}

export default function MapPageClient() {
  const searchParams = useSearchParams();
  const shareId = searchParams.get('s');
  const apiOverride = searchParams.get('api');

  // SSR/靜態匯出的第一次渲染沒有 navigator,先用預設繁中,掛載後才切成瀏覽器語言
  // (避免 hydration 的伺服端/client 文字不一致警告)。
  const [lang, setLang] = useState<MapLang>('zh');
  useEffect(() => {
    setLang(pickMapLang());
  }, []);
  const d = getMapDict(lang);

  const [status, setStatus] = useState<LoadStatus>('loading');
  const [snapshot, setSnapshot] = useState<MapSnapshotV1 | null>(null);
  const [updatedAt, setUpdatedAt] = useState<number | null>(null);
  const hasDataRef = useRef(false);

  const [world, setWorld] = useState<MapWorld>('main');
  const [showPlayers, setShowPlayers] = useState(true);
  const [showOffline, setShowOffline] = useState(false);
  const [showBases, setShowBases] = useState(true);
  const [showLandmarks, setShowLandmarks] = useState(true);

  const [landmarks, setLandmarks] = useState<StaticLandmark[]>([]);
  const [treeLandmarks, setTreeLandmarks] = useState<StaticLandmark[]>([]);

  // 靜態地標(隨網站一起打包,只載一次;缺檔就當沒有這個圖層)。
  useEffect(() => {
    fetch('/map-assets/landmarks.json')
      .then((r) => (r.ok ? (r.json() as Promise<StaticLandmark[]>) : []))
      .then((v) => setLandmarks(Array.isArray(v) ? v : []))
      .catch(() => setLandmarks([]));
    fetch('/map-assets/worldtree-landmarks.json')
      .then((r) => (r.ok ? (r.json() as Promise<StaticLandmark[]>) : []))
      .then((v) => setTreeLandmarks(Array.isArray(v) ? v : []))
      .catch(() => setTreeLandmarks([]));
  }, []);

  // 快照輪詢:第一次立即抓,之後每 20 秒;拿過資料後,之後的輪詢失敗不清畫面,
  // 只是不更新(agoText/離線橫幅會自然反映資料變舊)。連結被撤銷(404)則不論
  // 先前是否成功過,一律切到「連結不存在」畫面。
  useEffect(() => {
    if (!shareId) {
      setStatus('missing-id');
      return;
    }
    let cancelled = false;
    const load = async () => {
      const r = await fetchSnapshot(shareId, apiOverride);
      if (cancelled) return;
      if (r.status === 'ok') {
        hasDataRef.current = true;
        setSnapshot(r.data.snapshot);
        setUpdatedAt(r.data.updatedAt);
        setStatus('ok');
      } else if (r.status === 'not-found') {
        setStatus('not-found');
      } else if (!hasDataRef.current) {
        setStatus('error');
      }
    };
    void load();
    const timer = setInterval(load, POLL_MS);
    return () => {
      cancelled = true;
      clearInterval(timer);
    };
  }, [shareId, apiOverride]);

  // 「更新於 N 秒前」的顯示用時鐘,跟輪詢頻率脫鉤,每秒跳一次比較順眼。
  const [now, setNow] = useState<number | null>(null);
  useEffect(() => {
    setNow(Date.now());
    const t = setInterval(() => setNow(Date.now()), 1000);
    return () => clearInterval(t);
  }, []);

  const agoText = useMemo(() => {
    if (updatedAt == null || now == null) return null;
    const sec = Math.max(0, Math.round((now - updatedAt) / 1000));
    if (sec < 5) return d.updatedJustNow;
    if (sec < 60) return d.updatedSecondsAgo(sec);
    return d.updatedMinutesAgo(Math.round(sec / 60));
  }, [updatedAt, now, d]);

  const isStale = updatedAt != null && now != null && now - updatedAt > STALE_MS;

  const playersAvailable = !!snapshot?.show?.players;
  const offlineAvailable = !!snapshot?.show?.offline;
  const basesAvailable = !!snapshot?.show?.bases;
  const showNames = snapshot?.show?.names !== false;
  const showGuildNames = snapshot?.show?.guildNames !== false;
  const landmarksAvailable = landmarks.length > 0 || treeLandmarks.length > 0;

  const hasTreeData = useMemo(() => {
    if (!snapshot) return false;
    const all = [...(snapshot.players ?? []), ...(snapshot.offline ?? []), ...(snapshot.bases ?? [])];
    return all.some((e) => e.m === 'tree');
  }, [snapshot]);

  if (status === 'missing-id') {
    return <StateScreen title={d.missingIdTitle} body={d.missingIdBody} />;
  }
  if (status === 'not-found') {
    return <StateScreen title={d.notFoundTitle} body={d.notFoundBody} />;
  }
  if (!snapshot) {
    if (status === 'error') return <StateScreen title={d.fetchErrorTitle} body={d.fetchErrorBody} />;
    return (
      <div className="map2-boot">
        <p>{d.loading}</p>
      </div>
    );
  }

  return (
    <div className="map2-page">
      <header className="map2-header">
        <div className="map2-title">
          <span className="map2-servername">{snapshot.name || '—'}</span>
          <span className="map2-online">{d.online(snapshot.onlineCount, snapshot.maxPlayers)}</span>
        </div>
        {agoText && <span className="map2-ago">{agoText}</span>}
      </header>

      {isStale && <div className="map2-banner">{d.offlineBanner}</div>}

      <div className="map2-toolbar">
        {playersAvailable && (
          <ToggleBtn active={showPlayers} onClick={() => setShowPlayers((v) => !v)} label={d.players} />
        )}
        {offlineAvailable && (
          <ToggleBtn active={showOffline} onClick={() => setShowOffline((v) => !v)} label={d.offlinePlayers} />
        )}
        {basesAvailable && <ToggleBtn active={showBases} onClick={() => setShowBases((v) => !v)} label={d.bases} />}
        {landmarksAvailable && (
          <ToggleBtn active={showLandmarks} onClick={() => setShowLandmarks((v) => !v)} label={d.landmarks} />
        )}
        {hasTreeData && (
          <div className="map2-worldswitch">
            <button
              className={world === 'main' ? 'map2-wbtn map2-wbtn-on' : 'map2-wbtn'}
              onClick={() => setWorld('main')}
            >
              {d.mainWorld}
            </button>
            <button
              className={world === 'tree' ? 'map2-wbtn map2-wbtn-on' : 'map2-wbtn'}
              onClick={() => setWorld('tree')}
            >
              {d.worldTree}
            </button>
          </div>
        )}
      </div>

      <div className="map2-stage">
        <LeafletMap
          world={world}
          snapshot={snapshot}
          landmarks={landmarks}
          treeLandmarks={treeLandmarks}
          showPlayers={showPlayers}
          showOffline={showOffline}
          showBases={showBases}
          showLandmarks={showLandmarks}
          showNames={showNames}
          showGuildNames={showGuildNames}
          lang={lang}
        />
      </div>

      <footer className="map2-footer">{d.poweredBy}</footer>
    </div>
  );
}

function ToggleBtn({ active, onClick, label }: { active: boolean; onClick: () => void; label: string }) {
  return (
    <button className={active ? 'map2-tbtn map2-tbtn-on' : 'map2-tbtn'} onClick={onClick}>
      {label}
    </button>
  );
}

function StateScreen({ title, body }: { title: string; body: string }) {
  return (
    <div className="map2-boot">
      <div className="map2-state-card">
        <h1>{title}</h1>
        <p>{body}</p>
      </div>
    </div>
  );
}
