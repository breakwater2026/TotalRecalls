import React, { useRef } from 'react';
import { LibraryMeta, LIBRARY_DEFAULT_PATH, SAMPLE_SOURCE_LABEL, supportsDirectoryPicker } from '../Services/libraryLoader';

interface LibraryConnectProps {
  meta: LibraryMeta | null;
  busy: string | null;
  error: string | null;
  licensed: boolean;
  onFiles: (files: FileList) => void;
  onConnectPicker: () => void;
  onForget: () => void;
  onRequestLicense: () => void;
}

/**
 * Shows which corpus the app is actually searching.
 *
 * When nothing is connected the app is running on the 5 bundled sample
 * conversations, and this banner says so instead of letting the UI imply the
 * buyer's own history is loaded.
 */
export const LibraryConnect: React.FC<LibraryConnectProps> = ({ meta, busy, error, licensed, onFiles, onConnectPicker, onForget, onRequestLicense }) => {
  const inputRef = useRef<HTMLInputElement | null>(null);

  const pickFolder = () => inputRef.current?.click();
  const canUsePicker = supportsDirectoryPicker();

  const hiddenInput = (
    <input
      ref={inputRef}
      type="file"
      multiple
      // @ts-ignore -- non-standard but supported in Chromium, and the only
      // folder picker available on a file:// origin.
      webkitdirectory=""
      directory=""
      className="hidden"
      onChange={(e) => {
        const files = e.target.files;
        if (files && files.length) onFiles(files);
        e.target.value = '';
      }}
    />
  );

  if (!meta) {
    return (
      <div className="max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 pt-4">
        <div className="rounded-2xl border border-[var(--tr-accent)]/50 bg-[var(--tr-panel)] p-4 sm:p-5">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div className="min-w-0">
              <div className="flex items-center gap-2 flex-wrap">
                <span className="px-2 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider bg-[var(--tr-accent)]/15 text-[var(--tr-accent)] border border-[var(--tr-accent)]/40">
                  {licensed ? 'Demo data' : 'Demo mode'}
                </span>
                <span className="text-sm font-semibold text-[var(--tr-text)]">
                  {licensed ? 'Nothing indexed from your Library yet' : 'Smart Search Engine is not activated'}
                </span>
              </div>
              <p className="mt-1.5 text-xs text-[var(--tr-muted)] leading-relaxed">
                {licensed
                  ? `You are browsing the ${SAMPLE_SOURCE_LABEL.toLowerCase()}. Point the engine at your Downloader Pro library to search your own conversations — typically `
                  : 'Only the five sample conversations bundled with the app are available. Activate your SSE key to index and search your own library — typically '}
                <code className="font-mono text-[var(--tr-text)]">{LIBRARY_DEFAULT_PATH}</code>
              </p>
              {error && <p className="mt-1.5 text-xs text-red-400">{error}</p>}
              {busy && <p className="mt-1.5 text-xs text-[var(--tr-accent2)]">{busy}</p>}
            </div>
            <div className="flex flex-wrap items-center gap-2 shrink-0">
              {licensed ? (
                <>
                  <button
                    onClick={pickFolder}
                    disabled={!!busy}
                    className="px-4 py-2 rounded-lg bg-[var(--tr-accent)] hover:bg-[var(--tr-accent2)] text-[var(--tr-on-amber)] font-semibold text-sm disabled:opacity-50"
                  >
                    {busy ? 'Working…' : 'Connect Library folder…'}
                  </button>
                  {canUsePicker && (
                    <button
                      onClick={onConnectPicker}
                      disabled={!!busy}
                      title="Remembers the folder so you can re-scan with one click."
                      className="px-3 py-2 rounded-lg bg-[var(--tr-panel2)] border border-[var(--tr-border)] text-[var(--tr-text)] text-xs font-semibold hover:border-[var(--tr-accent)] disabled:opacity-50"
                    >
                      Remember folder
                    </button>
                  )}
                </>
              ) : (
                <button
                  onClick={onRequestLicense}
                  className="px-4 py-2 rounded-lg bg-[var(--tr-accent)] hover:bg-[var(--tr-accent2)] text-[var(--tr-on-amber)] font-semibold text-sm"
                >
                  Activate SSE key
                </button>
              )}
              {hiddenInput}
            </div>
          </div>
        </div>
      </div>
    );
  }

  const indexed = new Date(meta.indexedAt);
  const providerList = Object.entries(meta.providers)
    .sort((a, b) => b[1] - a[1])
    .map(([name, count]) => `${name} ${count}`)
    .join(' · ');

  return (
    <div className="max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 pt-4">
      <div className="rounded-2xl border border-[var(--tr-border)] bg-[var(--tr-panel)] px-4 py-3">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
          <div className="min-w-0">
            <div className="flex items-center gap-2 flex-wrap">
              <span className="px-2 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider bg-emerald-500/15 text-emerald-400 border border-emerald-500/40">
                Library connected
              </span>
              <span className="text-xs font-semibold text-[var(--tr-text)]">
                {meta.conversationCount.toLocaleString()} conversations · {meta.messageCount.toLocaleString()} messages · {meta.providerCount} providers
              </span>
            </div>
            <p className="mt-1 text-[11px] text-[var(--tr-muted)] truncate" title={providerList}>
              {providerList}
            </p>
            <p className="mt-0.5 text-[11px] text-[var(--tr-muted)]">
              {meta.sourceLabel} · indexed {indexed.toLocaleString()} · {meta.filesSeen.toLocaleString()} files read
              {meta.skipped > 0 ? ` · ${meta.skipped} skipped` : ''}
            </p>
            {busy && <p className="mt-1 text-xs text-[var(--tr-accent2)]">{busy}</p>}
            {error && <p className="mt-1 text-xs text-red-400">{error}</p>}
          </div>
          <div className="flex flex-wrap items-center gap-2 shrink-0">
            <button
              onClick={pickFolder}
              disabled={!!busy}
              className="px-3 py-1.5 rounded-lg bg-[var(--tr-panel2)] border border-[var(--tr-border)] text-[var(--tr-text)] text-xs font-semibold hover:border-[var(--tr-accent)] disabled:opacity-50"
            >
              Re-scan folder…
            </button>
            {canUsePicker && (
              <button
                onClick={onConnectPicker}
                disabled={!!busy}
                className="px-3 py-1.5 rounded-lg bg-[var(--tr-panel2)] border border-[var(--tr-border)] text-[var(--tr-text)] text-xs font-semibold hover:border-[var(--tr-accent)] disabled:opacity-50"
              >
                Remember folder
              </button>
            )}
            <button
              onClick={onForget}
              disabled={!!busy}
              className="px-3 py-1.5 rounded-lg border border-[var(--tr-border)] text-[var(--tr-muted)] text-xs hover:text-[var(--tr-text)] disabled:opacity-50"
            >
              Forget library
            </button>
            {hiddenInput}
          </div>
        </div>
      </div>
    </div>
  );
};

export default LibraryConnect;
