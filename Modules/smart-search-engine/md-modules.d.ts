/**
 * esbuild inlines markdown with `--loader:.md=text` (see tools/package_sse.py).
 * This declaration lets editors and tsc see those imports as strings.
 */
declare module '*.md' {
  const content: string;
  export default content;
}
