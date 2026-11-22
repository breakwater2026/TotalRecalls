// Manual export utility for the downloadable Markdown (.md) manuals.
// Generated client-side with zero external telemetry or server dependencies.
// Buyers receive Markdown and PDF; Word files are internal repo artifacts and
// are deliberately not offered in the app.

/**
 * The manuals ARE the shipped docs. esbuild inlines them with
 * `--loader:.md=text`, so the app cannot drift from the guides again.
 *
 * They used to be hardcoded copies, and they did drift: the in-app text still
 * described the app before library connection and the licence gate existed.
 * One source per manual.
 */
import USER_GUIDE_MARKDOWN from '../../../docs/TOTALRECALLS_SSE_QUICK_START_GUIDE.md';
import POWER_USER_MANUAL_MARKDOWN from '../../../docs/TOTALRECALLS_POWER_USER_MANUAL.md';

/** 'user' is the everyday guide; 'power' is the technical manual. */
export type ManualKind = 'user' | 'power';

export const downloadManualMarkdown = (kind: ManualKind = 'power'): void => {
  const content = kind === 'user' ? USER_GUIDE_MARKDOWN : POWER_USER_MANUAL_MARKDOWN;
  const filename = kind === 'user' ? 'TOTALRECALLS_USER_GUIDE.md' : 'TOTALRECALLS_POWER_USER_MANUAL.md';
  
  const blob = new Blob([content], { type: 'text/markdown;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
};
