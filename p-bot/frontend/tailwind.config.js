/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      typography: {
        DEFAULT: {
          css: {
            maxWidth: '100%',
          },
        },
      },
      colors: {
        'issue-agent': {
          light: '#e1f5fe',
          DEFAULT: '#03a9f4',
          dark: '#0277bd',
        },
        'tenancy-agent': {
          light: '#e8f5e9',
          DEFAULT: '#4caf50',
          dark: '#2e7d32',
        },
      },
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
    require('@tailwindcss/forms'),
  ],
} 