import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'
import tsconfigPaths from "vite-tsconfig-paths";
import { traeBadgePlugin } from 'vite-plugin-trae-solo-badge';

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  const authTarget = env.VITE_AUTH_BASE_URL || 'http://localhost:8081'
  const riskTarget = env.VITE_RISK_BASE_URL || 'http://localhost:8082'

  return {
  build: {
    sourcemap: 'hidden',
  },
  server: {
    proxy: {
      '/api-auth': {
        target: authTarget,
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api-auth/, ''),
      },
      '/api-risk': {
        target: riskTarget,
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api-risk/, ''),
      },
    },
  },
  plugins: [
    react({
      babel: {
        plugins: [
          'react-dev-locator',
        ],
      },
    }),
    traeBadgePlugin({
      variant: 'dark',
      position: 'bottom-right',
      prodOnly: true,
      clickable: true,
      clickUrl: 'https://www.trae.ai/solo?showJoin=1',
      autoTheme: true,
      autoThemeTarget: '#root'
    }), 
    tsconfigPaths()
  ],
  }
})
