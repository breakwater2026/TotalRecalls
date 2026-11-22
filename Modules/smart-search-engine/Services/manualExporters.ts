// Manual export utility providing downloadable Markdown (.md) and Microsoft Word (.docx/.doc) formats.
// Formats are generated client-side with zero external telemetry or server dependencies.

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

export const downloadManualWordDocx = (kind: ManualKind = 'power'): void => {
  const markdown = kind === 'user' ? USER_GUIDE_MARKDOWN : POWER_USER_MANUAL_MARKDOWN;
  const title = kind === 'user'
    ? 'TotalRecalls User Guide - Smart Search Engine'
    : 'TotalRecalls Power User Technical Manual - Smart Search Engine';
  const filename = kind === 'user' ? 'TOTALRECALLS_USER_GUIDE.doc' : 'TOTALRECALLS_POWER_USER_MANUAL.doc';

  // Format as clean HTML document with Word XML envelope
  const htmlContent = `
<html xmlns:o='urn:schemas-microsoft-com:office:office' xmlns:w='urn:schemas-microsoft-com:office:word' xmlns='http://www.w3.org/TR/REC-html40'>
<head>
  <meta charset="utf-8">
  <title>${title}</title>
  <style>
    body {
      font-family: 'Segoe UI', Calibri, Arial, sans-serif;
      font-size: 11pt;
      line-height: 1.5;
      color: #1e293b;
      margin: 40px;
    }
    h1 {
      color: #0891b2;
      font-size: 20pt;
      border-bottom: 2px solid #0891b2;
      padding-bottom: 6px;
      margin-top: 24px;
    }
    h2 {
      color: #0f766e;
      font-size: 15pt;
      margin-top: 20px;
    }
    h3 {
      color: #155e75;
      font-size: 12pt;
      margin-top: 14px;
    }
    p {
      margin-bottom: 10pt;
    }
    table {
      border-collapse: collapse;
      width: 100%;
      margin: 16px 0;
      font-size: 10pt;
    }
    th, td {
      border: 1px solid #cbd5e1;
      padding: 8px 12px;
      text-align: left;
    }
    th {
      background-color: #f1f5f9;
      color: #0f172a;
      font-weight: bold;
    }
    pre {
      background-color: #f8fafc;
      border: 1px solid #e2e8f0;
      padding: 12px;
      font-family: Consolas, 'Courier New', monospace;
      font-size: 9.5pt;
      border-radius: 6px;
      overflow-x: auto;
    }
    code {
      font-family: Consolas, 'Courier New', monospace;
      background-color: #f1f5f9;
      padding: 2px 4px;
      border-radius: 4px;
      font-size: 9.5pt;
    }
    .badge {
      display: inline-block;
      padding: 3px 8px;
      background-color: #06b6d4;
      color: #ffffff;
      font-weight: bold;
      border-radius: 4px;
      font-size: 9pt;
    }
  </style>
</head>
<body>
  <div style="text-align: center; margin-bottom: 30px;">
    <h1 style="border: none; margin-bottom: 4px;">TotalRecalls Documentation Suite</h1>
    <p style="color: #64748b; font-size: 10pt;">Local AI Chat Downloader, Vector Search & RAG SQL • totalrecalls.app</p>
  </div>
  ${markdownToHtml(markdown)}
</body>
</html>
  `;

  const blob = new Blob([htmlContent], { type: 'application/msword;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
};

function markdownToHtml(md: string): string {
  let html = md
    .replace(/^### (.*$)/gim, '<h3>$1</h3>')
    .replace(/^## (.*$)/gim, '<h2>$1</h2>')
    .replace(/^# (.*$)/gim, '<h1>$1</h1>')
    .replace(/\*\*(.*?)\*\*/gim, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/gim, '<em>$1</em>')
    .replace(/`([^`]+)`/gim, '<code>$1</code>')
    .replace(/```([\s\S]*?)```/gim, '<pre><code>$1</code></pre>')
    .replace(/\n\n/gim, '<p></p>')
    .replace(/\n/gim, '<br />');

  return html;
}

// Named alias for convenience across packaging studio and other components
export const downloadManualDocx = downloadManualWordDocx;

