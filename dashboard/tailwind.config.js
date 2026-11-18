/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        rr: {
          navy: '#070d1e',
          dark: '#0c1630',
          card: '#121e3f',
          border: '#1f305c',
          pink: '#ea0089',
          pinkHover: '#ff1f9e',
          cyan: '#00f0ff',
          blue: '#2563eb',
          gold: '#fbbf24',
          gray: '#94a3b8'
        }
      }
    },
  },
  plugins: [],
}

