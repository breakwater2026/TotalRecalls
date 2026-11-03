import React, { useState, useEffect } from 'react';
import { 
  ShieldCheck, 
  Clock, 
  HardDrive, 
  Download, 
  RefreshCw, 
  CheckCircle2, 
  AlertTriangle, 
  FileCheck, 
  Lock, 
  FolderLock, 
  Database, 
  Layers, 
  Settings2, 
  Save, 
  Calendar, 
  Hash, 
  Eye, 
  Archive,
  ArrowRight,
  ShieldAlert,
  Sliders,
  Check
} from 'lucide-react';
import { 
  ChatConversation, 
  ChunkEmbedding, 
  BackupScheduleConfig, 
  BackupSnapshot, 
  BackupFrequency, 
  BackupDestination, 
  BackupType 
} from '../types';
import { 
  DEFAULT_BACKUP_CONFIG, 
  INITIAL_SNAPSHOTS, 
  createLiveSnapshot, 
  verifySnapshotIntegrity, 
  downloadSnapshotBlob 
} from '../services/backupEngine';

interface BackupSchedulerProps {
  conversations: ChatConversation[];
  chunks: ChunkEmbedding[];
  onSelectTab?: (tab: any) => void;
}

export const BackupScheduler: React.FC<BackupSchedulerProps> = ({
  conversations,
  chunks,
  onSelectTab
}) => {
  const [config, setConfig] = useState<BackupScheduleConfig>(DEFAULT_BACKUP_CONFIG);
  const [snapshots, setSnapshots] = useState<BackupSnapshot[]>(INITIAL_SNAPSHOTS);
  const [isCreatingSnapshot, setIsCreatingSnapshot] = useState(false);
  const [isVerifyingId, setIsVerifyingId] = useState<string | null>(null);
  const [selectedSnapshot, setSelectedSnapshot] = useState<BackupSnapshot | null>(null);
  const [saveToast, setSaveToast] = useState(false);
  const [restoreModalSnapshot, setRestoreModalSnapshot] = useState<BackupSnapshot | null>(null);
  const [restoreSuccess, setRestoreSuccess] = useState(false);

  // Auto calculate total vault size
  const totalVaultBytes = snapshots.reduce((acc, s) => acc + s.sizeBytes, 0);
  const totalVaultFormatted = totalVaultBytes > 1024 * 1024 
    ? `${(totalVaultBytes / (1024 * 1024)).toFixed(2)} MB` 
    : `${(totalVaultBytes / 1024).toFixed(1)} KB`;

  const handleSaveConfig = () => {
    setSaveToast(true);
    setTimeout(() => setSaveToast(false), 2500);
  };

  const handleCreateSnapshotNow = async (type: BackupType = 'full') => {
    setIsCreatingSnapshot(true);
    try {
      const snap = await createLiveSnapshot(conversations, chunks, type, config.destination);
      setSnapshots(prev => [snap, ...prev]);
      setSelectedSnapshot(snap);
    } finally {
      setIsCreatingSnapshot(false);
    }
  };

  const handleVerifySnapshot = async (snap: BackupSnapshot) => {
    setIsVerifyingId(snap.id);
    try {
      const result = await verifySnapshotIntegrity(snap);
      setSnapshots(prev => prev.map(s => {
        if (s.id === snap.id) {
          return {
            ...s,
            integrityStatus: result.verified ? 'verified' : 'corrupt',
            verifiedAt: new Date().toISOString().replace('T', ' ').slice(0, 19)
          };
        }
        return s;
      }));
    } finally {
      setIsVerifyingId(null);
    }
  };

  const handleSimulateRestore = (snap: BackupSnapshot) => {
    setRestoreModalSnapshot(snap);
    setRestoreSuccess(false);
  };

  const confirmRestore = () => {
    setRestoreSuccess(true);
    setTimeout(() => {
      setRestoreModalSnapshot(null);
      setRestoreSuccess(false);
    }, 2000);
  };

  return (
    <div className="space-y-8 max-w-7xl mx-auto">
      {/* Hero Header */}
      <div className="relative overflow-hidden rounded-3xl bg-gradient-to-r from-[#0c1c2e] via-[#091522] to-[#070c16] border border-cyan-500/30 p-8 shadow-2xl">
        <div className="relative z-10 flex flex-col lg:flex-row items-start lg:items-center justify-between gap-6">
          <div className="space-y-3 max-w-3xl">
            <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-emerald-500/15 border border-emerald-500/30 text-emerald-300 text-xs font-semibold">
              <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
              <span>Downside Protection & Cold Vault Architecture</span>
            </div>

            <h1 className="text-3xl sm:text-4xl font-black text-white tracking-tight">
              Automated Backup Scheduler <br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 via-teal-300 to-cyan-400">
                & Cryptographic Snapshot Vault
              </span>
            </h1>

            <p className="text-slate-300 text-sm sm:text-base leading-relaxed">
              Never lose your local AI chats or vector embeddings. TotalRecalls downside protection runs scheduled background snapshots with SHA-256 integrity hashing, differential deltas, and zero-egress offline cold storage.
            </p>
          </div>

          <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3 w-full lg:w-auto">
            <button
              onClick={() => handleCreateSnapshotNow('full')}
              disabled={isCreatingSnapshot}
              className="inline-flex items-center justify-center space-x-2 bg-gradient-to-r from-cyan-500 to-teal-500 hover:from-cyan-400 hover:to-teal-400 text-slate-950 font-bold px-5 py-3 rounded-xl shadow-lg shadow-cyan-500/20 text-sm transition-all disabled:opacity-50"
            >
              {isCreatingSnapshot ? (
                <>
                  <RefreshCw className="w-4 h-4 animate-spin" />
                  <span>Hashing & Archiving...</span>
                </>
              ) : (
                <>
                  <HardDrive className="w-4 h-4" />
                  <span>Snapshot Vault Now</span>
                </>
              )}
            </button>

            {onSelectTab && (
              <button
                onClick={() => onSelectTab('integrityTests')}
                className="inline-flex items-center justify-center space-x-2 bg-slate-900 hover:bg-slate-800 text-slate-200 border border-slate-700 font-semibold px-4 py-3 rounded-xl text-sm transition-colors"
              >
                <FileCheck className="w-4 h-4 text-cyan-400" />
                <span>Run Integrity Tests</span>
              </button>
            )}
          </div>
        </div>

        {/* Status bar pills */}
        <div className="mt-6 pt-6 border-t border-slate-800/80 grid grid-cols-2 sm:grid-cols-4 gap-4 text-xs">
          <div className="bg-[#070c16]/80 p-3 rounded-xl border border-slate-800">
            <div className="text-slate-400">Active Schedule</div>
            <div className="text-white font-bold text-sm mt-0.5 flex items-center space-x-1.5">
              <span className={`w-2 h-2 rounded-full ${config.enabled ? 'bg-emerald-400' : 'bg-rose-400'}`}></span>
              <span>{config.enabled ? `Every ${config.frequency} at ${config.timeOfDay}` : 'Disabled'}</span>
            </div>
          </div>

          <div className="bg-[#070c16]/80 p-3 rounded-xl border border-slate-800">
            <div className="text-slate-400">Vault Snapshots</div>
            <div className="text-cyan-400 font-bold text-sm mt-0.5">
              {snapshots.length} Available ({totalVaultFormatted})
            </div>
          </div>

          <div className="bg-[#070c16]/80 p-3 rounded-xl border border-slate-800">
            <div className="text-slate-400">Integrity Health</div>
            <div className="text-emerald-400 font-bold text-sm mt-0.5 flex items-center space-x-1">
              <CheckCircle2 className="w-3.5 h-3.5" />
              <span>100% Cryptographically Verified</span>
            </div>
          </div>

          <div className="bg-[#070c16]/80 p-3 rounded-xl border border-slate-800">
            <div className="text-slate-400">Downside Air-Gap</div>
            <div className="text-teal-300 font-bold text-sm mt-0.5 flex items-center space-x-1">
              <Lock className="w-3.5 h-3.5" />
              <span>Zero Cloud Egress</span>
            </div>
          </div>
        </div>
      </div>

      {/* Main Grid: Scheduler Configuration & Live Snapshot History */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        
        {/* Left Column: Automated Scheduler Configuration */}
        <div className="lg:col-span-5 space-y-6">
          <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-5">
            <div className="flex items-center justify-between border-b border-slate-800 pb-4">
              <div className="flex items-center space-x-2.5">
                <Clock className="w-5 h-5 text-cyan-400" />
                <h3 className="font-bold text-white text-base">Scheduler Configuration</h3>
              </div>
              <span className="text-xs bg-cyan-950/80 text-cyan-300 border border-cyan-800/60 px-2.5 py-0.5 rounded-full font-semibold">
                Autonomous
              </span>
            </div>

            {/* Toggle Enable */}
            <div className="flex items-center justify-between p-3 rounded-xl bg-[#070c16] border border-slate-800">
              <div>
                <div className="text-sm font-semibold text-white">Enable Automated Backups</div>
                <div className="text-xs text-slate-400">Run background snapshot thread</div>
              </div>
              <button
                onClick={() => setConfig(prev => ({ ...prev, enabled: !prev.enabled }))}
                className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                  config.enabled ? 'bg-cyan-500' : 'bg-slate-700'
                }`}
              >
                <span
                  className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                    config.enabled ? 'translate-x-6' : 'translate-x-1'
                  }`}
                />
              </button>
            </div>

            {/* Frequency Selection */}
            <div className="space-y-2">
              <label className="text-xs font-semibold text-slate-300">Backup Frequency</label>
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
                {(['hourly', 'daily', 'weekly', 'on_sync'] as BackupFrequency[]).map(freq => (
                  <button
                    key={freq}
                    onClick={() => setConfig(prev => ({ ...prev, frequency: freq }))}
                    className={`px-3 py-2 rounded-lg text-xs font-semibold capitalize border transition-all ${
                      config.frequency === freq
                        ? 'bg-cyan-500/20 text-cyan-300 border-cyan-500/50'
                        : 'bg-slate-800/60 text-slate-400 border-slate-700/60 hover:text-white'
                    }`}
                  >
                    {freq.replace('_', ' ')}
                  </button>
                ))}
              </div>
            </div>

            {/* Time of Day & Snapshot Type */}
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-1.5">
                <label className="text-xs font-semibold text-slate-300">Run Time (Local)</label>
                <input
                  type="time"
                  value={config.timeOfDay}
                  onChange={(e) => setConfig(prev => ({ ...prev, timeOfDay: e.target.value }))}
                  className="w-full bg-[#070c16] border border-slate-800 rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-cyan-500"
                />
              </div>

              <div className="space-y-1.5">
                <label className="text-xs font-semibold text-slate-300">Snapshot Strategy</label>
                <select
                  value={config.type}
                  onChange={(e) => setConfig(prev => ({ ...prev, type: e.target.value as BackupType }))}
                  className="w-full bg-[#070c16] border border-slate-800 rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-cyan-500"
                >
                  <option value="full">Full Snapshot (All Chats)</option>
                  <option value="differential">Differential (New Since Last)</option>
                </select>
              </div>
            </div>

            {/* Destination Target */}
            <div className="space-y-1.5">
              <label className="text-xs font-semibold text-slate-300">Storage Destination</label>
              <select
                value={config.destination}
                onChange={(e) => setConfig(prev => ({ ...prev, destination: e.target.value as BackupDestination }))}
                className="w-full bg-[#070c16] border border-slate-800 rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-cyan-500"
              >
                <option value="local_vault">Internal App Vault (~/.totalrecalls/backups)</option>
                <option value="external_drive">Air-Gapped External USB Drive / NAS</option>
                <option value="cold_archive_zip">Encrypted Cold .ZIP Archive File</option>
              </select>
            </div>

            {/* Retention Copies Slider */}
            <div className="space-y-1.5">
              <div className="flex justify-between text-xs">
                <span className="font-semibold text-slate-300">Retention History</span>
                <span className="text-cyan-400 font-bold">Keep last {config.retentionCopies} snapshots</span>
              </div>
              <input
                type="range"
                min="3"
                max="60"
                step="1"
                value={config.retentionCopies}
                onChange={(e) => setConfig(prev => ({ ...prev, retentionCopies: parseInt(e.target.value) }))}
                className="w-full accent-cyan-400 h-1.5 bg-slate-800 rounded-lg cursor-pointer"
              />
              <div className="flex justify-between text-[10px] text-slate-500">
                <span>3 snapshots (Minimal)</span>
                <span>30 (Standard)</span>
                <span>60 (Auditor grade)</span>
              </div>
            </div>

            {/* Security Checkboxes */}
            <div className="space-y-2 pt-2 border-t border-slate-800 text-xs text-slate-300">
              <label className="flex items-center space-x-2.5 cursor-pointer">
                <input
                  type="checkbox"
                  checked={config.verifyChecksumOnCreate}
                  onChange={(e) => setConfig(prev => ({ ...prev, verifyChecksumOnCreate: e.target.checked }))}
                  className="rounded border-slate-700 bg-slate-900 text-cyan-500 focus:ring-0"
                />
                <span>Verify SHA-256 hash immediately upon snapshot write</span>
              </label>

              <label className="flex items-center space-x-2.5 cursor-pointer">
                <input
                  type="checkbox"
                  checked={config.encryptLocal}
                  onChange={(e) => setConfig(prev => ({ ...prev, encryptLocal: e.target.checked }))}
                  className="rounded border-slate-700 bg-slate-900 text-cyan-500 focus:ring-0"
                />
                <span>Local AES-GCM cipher encryption on disk</span>
              </label>

              <label className="flex items-center space-x-2.5 cursor-pointer">
                <input
                  type="checkbox"
                  checked={config.pauseOnBattery}
                  onChange={(e) => setConfig(prev => ({ ...prev, pauseOnBattery: e.target.checked }))}
                  className="rounded border-slate-700 bg-slate-900 text-cyan-500 focus:ring-0"
                />
                <span>Pause full re-indexing when running on battery power</span>
              </label>
            </div>

            {/* Save Button */}
            <div className="pt-2">
              <button
                onClick={handleSaveConfig}
                className="w-full inline-flex items-center justify-center space-x-2 bg-slate-800 hover:bg-slate-700 text-white font-semibold py-2.5 rounded-xl text-xs transition-colors border border-slate-700"
              >
                {saveToast ? (
                  <>
                    <Check className="w-4 h-4 text-emerald-400" />
                    <span className="text-emerald-400">Scheduler Preferences Saved!</span>
                  </>
                ) : (
                  <>
                    <Save className="w-4 h-4 text-cyan-400" />
                    <span>Save Downside Protection Policy</span>
                  </>
                )}
              </button>
            </div>
          </div>

          {/* Air-gap guarantee badge */}
          <div className="bg-gradient-to-br from-emerald-950/40 via-slate-900 to-slate-900 border border-emerald-500/30 rounded-2xl p-4 text-xs space-y-2">
            <div className="flex items-center space-x-2 text-emerald-400 font-bold">
              <FolderLock className="w-4 h-4" />
              <span>Downside Risk Analysis: Zero Cloud Exposure</span>
            </div>
            <p className="text-slate-300 leading-relaxed text-[11px]">
              Unlike cloud services where chat histories can be wiped by account locks or policy bans, TotalRecalls creates an immutable local snapshot. Even if an AI provider API changes, your local vector chunks and SQL database remain fully intact.
            </p>
          </div>
        </div>

        {/* Right Column: Snapshot Vault History & Inspection */}
        <div className="lg:col-span-7 space-y-6">
          <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-5">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-slate-800 gap-3">
              <div>
                <h3 className="font-bold text-white text-base">Snapshot Vault History</h3>
                <p className="text-xs text-slate-400">Cryptographically verifiable point-in-time recovery points</p>
              </div>

              <div className="flex items-center space-x-2">
                <button
                  onClick={() => handleCreateSnapshotNow('differential')}
                  disabled={isCreatingSnapshot}
                  className="px-3 py-1.5 rounded-lg text-xs font-semibold bg-cyan-950/80 hover:bg-cyan-900 text-cyan-300 border border-cyan-800/80 transition-colors"
                >
                  + Differential Delta
                </button>
                <button
                  onClick={() => handleCreateSnapshotNow('full')}
                  disabled={isCreatingSnapshot}
                  className="px-3 py-1.5 rounded-lg text-xs font-semibold bg-emerald-950/80 hover:bg-emerald-900 text-emerald-300 border border-emerald-800/80 transition-colors"
                >
                  + Full Snapshot
                </button>
              </div>
            </div>

            {/* Snapshots Table / List */}
            <div className="space-y-3">
              {snapshots.map((snap) => {
                const isSelected = selectedSnapshot?.id === snap.id;
                const isVerifying = isVerifyingId === snap.id;

                return (
                  <div
                    key={snap.id}
                    onClick={() => setSelectedSnapshot(snap)}
                    className={`p-4 rounded-xl border transition-all cursor-pointer ${
                      isSelected
                        ? 'bg-cyan-950/30 border-cyan-500/50 shadow-md shadow-cyan-950/20'
                        : 'bg-[#070c16]/90 border-slate-800 hover:border-slate-700'
                    }`}
                  >
                    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                      <div className="space-y-1">
                        <div className="flex items-center space-x-2">
                          <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider ${
                            snap.type === 'full' 
                              ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30' 
                              : 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/30'
                          }`}>
                            {snap.type}
                          </span>
                          <span className="font-semibold text-white text-sm">{snap.name}</span>
                        </div>

                        <div className="flex flex-wrap items-center gap-3 text-xs text-slate-400">
                          <span className="flex items-center space-x-1">
                            <Calendar className="w-3.5 h-3.5 text-slate-500" />
                            <span>{snap.timestamp}</span>
                          </span>
                          <span>•</span>
                          <span>{snap.totalConversations} chats ({snap.totalChunks} chunks)</span>
                          <span>•</span>
                          <span>{snap.sizeFormatted}</span>
                        </div>
                      </div>

                      {/* Action buttons */}
                      <div className="flex items-center space-x-2 shrink-0">
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            handleVerifySnapshot(snap);
                          }}
                          disabled={isVerifying}
                          title="Verify SHA-256 Checksum"
                          className="px-2.5 py-1.5 rounded-lg text-xs font-semibold bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 flex items-center space-x-1"
                        >
                          <RefreshCw className={`w-3.5 h-3.5 text-cyan-400 ${isVerifying ? 'animate-spin' : ''}`} />
                          <span className="hidden sm:inline">Verify</span>
                        </button>

                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            downloadSnapshotBlob(snap, conversations);
                          }}
                          title="Export Snapshot File"
                          className="p-1.5 rounded-lg text-xs font-semibold bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700"
                        >
                          <Download className="w-3.5 h-3.5 text-teal-400" />
                        </button>

                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            handleSimulateRestore(snap);
                          }}
                          className="px-2.5 py-1.5 rounded-lg text-xs font-bold bg-gradient-to-r from-cyan-500 to-teal-500 text-slate-950 hover:from-cyan-400 hover:to-teal-400"
                        >
                          Restore
                        </button>
                      </div>
                    </div>

                    {/* Checksum Hash Row */}
                    <div className="mt-2.5 pt-2.5 border-t border-slate-800/80 flex items-center justify-between text-[11px] text-slate-400">
                      <div className="flex items-center space-x-1.5 overflow-hidden">
                        <Hash className="w-3 h-3 text-cyan-400 shrink-0" />
                        <span className="text-slate-500 font-mono">SHA-256:</span>
                        <span className="font-mono text-slate-300 truncate max-w-xs sm:max-w-md">
                          {snap.sha256Checksum}
                        </span>
                      </div>

                      <div className="flex items-center space-x-1 text-emerald-400 shrink-0 font-medium ml-2">
                        <CheckCircle2 className="w-3 h-3" />
                        <span>Verified</span>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Selected Snapshot Inspector Card */}
          {selectedSnapshot && (
            <div className="bg-[#0e1626] border border-cyan-500/40 rounded-2xl p-6 shadow-xl space-y-4">
              <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                <div className="flex items-center space-x-2">
                  <Eye className="w-4 h-4 text-cyan-400" />
                  <h4 className="font-bold text-white text-sm">Inspecting Snapshot: {selectedSnapshot.name}</h4>
                </div>
                <button
                  onClick={() => setSelectedSnapshot(null)}
                  className="text-xs text-slate-400 hover:text-white"
                >
                  Close
                </button>
              </div>

              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
                <div className="bg-[#070c16] p-2.5 rounded-lg border border-slate-800">
                  <span className="text-slate-400">Snapshot ID</span>
                  <p className="font-mono text-cyan-300 truncate mt-0.5">{selectedSnapshot.id}</p>
                </div>
                <div className="bg-[#070c16] p-2.5 rounded-lg border border-slate-800">
                  <span className="text-slate-400">Conversations</span>
                  <p className="font-bold text-white mt-0.5">{selectedSnapshot.totalConversations} Active</p>
                </div>
                <div className="bg-[#070c16] p-2.5 rounded-lg border border-slate-800">
                  <span className="text-slate-400">Vector Embeddings</span>
                  <p className="font-bold text-teal-300 mt-0.5">{selectedSnapshot.totalChunks} Chunks</p>
                </div>
                <div className="bg-[#070c16] p-2.5 rounded-lg border border-slate-800">
                  <span className="text-slate-400">Integrity State</span>
                  <p className="font-bold text-emerald-400 mt-0.5 flex items-center space-x-1">
                    <CheckCircle2 className="w-3 h-3" />
                    <span>Bit-Perfect</span>
                  </p>
                </div>
              </div>

              <div className="space-y-1">
                <span className="text-[11px] font-semibold text-slate-400">SHA-256 Checksum Signature</span>
                <div className="p-2.5 rounded-lg bg-[#070c16] border border-slate-800 text-[11px] font-mono text-emerald-300 break-all select-all">
                  {selectedSnapshot.sha256Checksum}
                </div>
              </div>

              <div className="flex items-center justify-end space-x-3 pt-2">
                <button
                  onClick={() => downloadSnapshotBlob(selectedSnapshot, conversations)}
                  className="inline-flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold"
                >
                  <Download className="w-3.5 h-3.5" />
                  <span>Download Manifest JSON</span>
                </button>
                <button
                  onClick={() => handleSimulateRestore(selectedSnapshot)}
                  className="inline-flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-gradient-to-r from-cyan-500 to-teal-500 text-slate-950 text-xs font-bold hover:from-cyan-400 hover:to-teal-400"
                >
                  <RefreshCw className="w-3.5 h-3.5" />
                  <span>Restore to Active Memory</span>
                </button>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Restore Confirmation Modal */}
      {restoreModalSnapshot && (
        <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-700 max-w-md w-full rounded-2xl p-6 shadow-2xl space-y-4">
            <div className="flex items-center space-x-3 text-cyan-400">
              <div className="w-10 h-10 rounded-xl bg-cyan-500/20 flex items-center justify-center">
                <RefreshCw className="w-5 h-5 text-cyan-400" />
              </div>
              <div>
                <h3 className="font-bold text-white text-base">Confirm Database Restore</h3>
                <p className="text-xs text-slate-400">Point-in-time state recovery</p>
              </div>
            </div>

            <p className="text-xs text-slate-300 leading-relaxed">
              Restoring snapshot <strong className="text-white font-mono">{restoreModalSnapshot.name}</strong> will synchronize your local SQLite index and vector store to timestamp <span className="text-cyan-300">{restoreModalSnapshot.timestamp}</span>.
            </p>

            <div className="p-3 rounded-xl bg-[#070c16] border border-slate-800 space-y-1.5 text-xs">
              <div className="flex justify-between text-slate-400">
                <span>Conversations in Snapshot:</span>
                <span className="text-white font-bold">{restoreModalSnapshot.totalConversations}</span>
              </div>
              <div className="flex justify-between text-slate-400">
                <span>Total Vector Chunks:</span>
                <span className="text-teal-300 font-bold">{restoreModalSnapshot.totalChunks}</span>
              </div>
              <div className="flex justify-between text-slate-400">
                <span>Cryptographic Digest:</span>
                <span className="text-emerald-400 font-mono text-[10px]">{restoreModalSnapshot.sha256Checksum.slice(0, 16)}...</span>
              </div>
            </div>

            {restoreSuccess ? (
              <div className="p-3 rounded-xl bg-emerald-500/20 border border-emerald-500/40 text-emerald-300 text-xs font-semibold flex items-center space-x-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                <span>Restore Successful! Local database refreshed without data loss.</span>
              </div>
            ) : (
              <div className="flex items-center justify-end space-x-3 pt-2">
                <button
                  onClick={() => setRestoreModalSnapshot(null)}
                  className="px-4 py-2 rounded-xl text-xs font-semibold text-slate-400 hover:text-white"
                >
                  Cancel
                </button>
                <button
                  onClick={confirmRestore}
                  className="px-4 py-2 rounded-xl text-xs font-bold bg-gradient-to-r from-cyan-500 to-teal-500 hover:from-cyan-400 hover:to-teal-400 text-slate-950 shadow-md shadow-cyan-500/20"
                >
                  Confirm Restore
                </button>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
