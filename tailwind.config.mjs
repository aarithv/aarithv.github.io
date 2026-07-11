/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        cream: '#FBF6EE',
        'cream-dark': '#F3EAD9',
        ink: '#2A2420',
        'ink-soft': '#6B5F56',
        terracotta: {
          DEFAULT: '#C1613C',
          dark: '#A14D2E',
        },
        sage: {
          DEFAULT: '#7C8B6F',
          dark: '#63705A',
        },
      },
      fontFamily: {
        serif: ['Fraunces', 'ui-serif', 'Georgia', 'serif'],
        sans: ['Inter', 'ui-sans-serif', 'system-ui', 'sans-serif'],
      },
    },
  },
};
