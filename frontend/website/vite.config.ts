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
        km_products: 'km/products/index.html',
        km_trust: 'km/trust/index.html',
        km_borrow: 'km/borrow/index.html',
        km_fees: 'km/fees/index.html',
        km_faq: 'km/faq/index.html',
        km_contact: 'km/contact/index.html',
        km_risk: 'km/risk/index.html',
        km_privacy: 'km/privacy/index.html',
        km_terms: 'km/terms/index.html',
        km_blog: 'km/blog/index.html',
        km_blog_aba: 'km/blog/article/index.html',

        en_home: 'en/index.html',
        en_products: 'en/products/index.html',
        en_trust: 'en/trust/index.html',
        en_borrow: 'en/borrow/index.html',
        en_fees: 'en/fees/index.html',
        en_faq: 'en/faq/index.html',
        en_contact: 'en/contact/index.html',
        en_risk: 'en/risk/index.html',
        en_privacy: 'en/privacy/index.html',
        en_terms: 'en/terms/index.html',
        en_blog: 'en/blog/index.html',
        en_blog_aba: 'en/blog/article/index.html',

        zh_home: 'zh/index.html',
        zh_products: 'zh/products/index.html',
        zh_trust: 'zh/trust/index.html',
        zh_borrow: 'zh/borrow/index.html',
        zh_fees: 'zh/fees/index.html',
        zh_faq: 'zh/faq/index.html',
        zh_contact: 'zh/contact/index.html',
        zh_risk: 'zh/risk/index.html',
        zh_privacy: 'zh/privacy/index.html',
        zh_terms: 'zh/terms/index.html',
        zh_blog: 'zh/blog/index.html',
        zh_blog_aba: 'zh/blog/article/index.html',
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
