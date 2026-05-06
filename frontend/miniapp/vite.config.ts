import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'
import tsconfigPaths from "vite-tsconfig-paths";

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "")
  const target = (env.VITE_DEV_PROXY_TARGET || "http://127.0.0.1:3040").trim()

  return {
    server: {
      proxy: {
        "/auth": { target, changeOrigin: true },
        "/risk": { target, changeOrigin: true },
        "/p2p": { target, changeOrigin: true },
        "/api": { target, changeOrigin: true },
        "/proofs": { target, changeOrigin: true },
      },
    },
    build: {
      sourcemap: "hidden",
    },
    plugins: [
      react({
        babel: {
          plugins: ["react-dev-locator"],
        },
      }),
      tsconfigPaths(),
    ],
  }
})
