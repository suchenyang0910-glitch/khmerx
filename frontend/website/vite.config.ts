import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tsconfigPaths from "vite-tsconfig-paths";
import { traeBadgePlugin } from 'vite-plugin-trae-solo-badge';

// https://vite.dev/config/
export default defineConfig({
  build: {
    sourcemap: 'hidden',
    rollupOptions: {
      input: {
        root: 'index.html',

        km_home: 'km/index.html',
        km_borrow: 'km/borrow/index.html',
        km_fees: 'km/fees/index.html',
        km_faq: 'km/faq/index.html',
        km_contact: 'km/contact/index.html',

        en_home: 'en/index.html',
        en_borrow: 'en/borrow/index.html',
        en_fees: 'en/fees/index.html',
        en_faq: 'en/faq/index.html',
        en_contact: 'en/contact/index.html',

        zh_home: 'zh/index.html',
        zh_borrow: 'zh/borrow/index.html',
        zh_fees: 'zh/fees/index.html',
        zh_faq: 'zh/faq/index.html',
        zh_contact: 'zh/contact/index.html',
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
      autoThemeTarget: 'body'
    }), 
    tsconfigPaths()
  ],
})
