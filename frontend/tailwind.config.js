/** @type {import('tailwindcss').Config} */
export default {
  darkMode: ["class"],
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Medical blue theme
        primary: {
          DEFAULT: "#0066CC",
          50: "#E5F2FF",
          100: "#CCE5FF",
          200: "#99CCFF",
          300: "#66B2FF",
          400: "#3399FF",
          500: "#0066CC", // Main medical blue
          600: "#0052A3",
          700: "#003D7A",
          800: "#002952",
          900: "#001429",
        },
        secondary: {
          DEFAULT: "#4CAF50",
          50: "#E8F5E9",
          100: "#C8E6C9",
          200: "#A5D6A7",
          300: "#81C784",
          400: "#66BB6A",
          500: "#4CAF50", // Health green
          600: "#43A047",
          700: "#388E3C",
          800: "#2E7D32",
          900: "#1B5E20",
        },
        keto: {
          DEFAULT: "#8B4789",
          50: "#F3E5F3",
          100: "#E1BEE7",
          200: "#CE93D8",
          300: "#BA68C8",
          400: "#AB47BC",
          500: "#8B4789", // Purple for keto
          600: "#7B1FA2",
          700: "#6A1B9A",
          800: "#4A148C",
          900: "#311B92",
        },
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
}
