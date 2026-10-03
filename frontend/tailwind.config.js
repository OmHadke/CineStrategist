/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        studio: {
          900: '#090a0f',
          800: '#12141d',
          700: '#1a1d29',
          600: '#262a3b',
          500: '#383d54',
          accent: '#e50914', // Cinematic Crimson (Netflix / Red Chillies red)
          gold: '#e5a93c',
          emerald: '#10b981',
          cyan: '#06b6d4',
        }
      }
    },
  },
  plugins: [],
}
