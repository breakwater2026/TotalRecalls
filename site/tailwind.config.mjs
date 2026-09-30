/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        background: 'hsl(var(--background, 0 0% 100%))',
        foreground: 'hsl(var(--foreground, 222.2 84% 4.9%))',
        card: {
          DEFAULT: 'hsl(var(--card, 0 0% 100%))',
          foreground: 'hsl(var(--card-foreground, 222.2 84% 4.9%))',
        },
        primary: {
          DEFAULT: '#2F7BFF',
          foreground: '#FFFFFF',
        },
        /* Brand Style Guide v1.0 (Jasper rewrite) */
        'tr-obsidian': 'var(--tr-obsidian)',
        'tr-graphite': 'var(--tr-graphite)',
        'tr-slate': 'var(--tr-slate)',
        'tr-paper': 'var(--tr-paper)',
        'tr-mist': 'var(--tr-mist)',
        'tr-dust': 'var(--tr-dust)',
        'tr-amber': {
          DEFAULT: 'var(--tr-amber)',
          hover: 'var(--tr-amber-hover)',
          press: 'var(--tr-amber-press)',
        },
        'tr-green': 'var(--tr-green)',
        'tr-steel': 'var(--tr-steel)',
        'tr-error': 'var(--tr-error)',
        muted: {
          DEFAULT: 'hsl(var(--muted, 210 40% 96.1%))',
          foreground: 'hsl(var(--muted-foreground, 215.4 16.3% 46.9%))',
        },
        destructive: {
          DEFAULT: '#DC2626',
          foreground: '#FFFFFF',
        },
        border: 'hsl(var(--border, 214.3 31.8% 91.4%))',
      },
      borderRadius: {
        chip: '6px',
        btn: '8px',
        card: '12px',
      },
      fontFamily: {
        mono: ['"IBM Plex Mono"', 'monospace'],
        heading: ['Inter', 'sans-serif'],
        body: ['Inter', 'sans-serif'],
      },
    },
  },
  plugins: [],
};
