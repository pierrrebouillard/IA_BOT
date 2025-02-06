import type { Config } from "tailwindcss";

export default {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        'violet': '#06003B',
        'claire': '#7440F4',
        'foncé': '#1E194B',
        background: "var(--background)",
        foreground: "var(--foreground)",
      },
    },
  },
  plugins: [require("@tailwindcss/forms")],
} satisfies Config;
