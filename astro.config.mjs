// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import mdx from '@astrojs/mdx';
import tailwindcss from '@tailwindcss/vite';
import { SITE_URL } from './site.config.mjs';

export default defineConfig({
  site: SITE_URL,
  trailingSlash: 'never',
  output: 'static',

  integrations: [
    mdx(),
    sitemap({
      // Cloudflare Pages sert /projets/one-zone/ sous /projets/one-zone.
      // Le sitemap doit annoncer exactement la meme forme que la canonique.
      serialize(item) {
        const sansBarre = item.url.replace(/\/$/, '');
        // La racine conserve sa barre oblique, comme la canonique correspondante.
        item.url = sansBarre === SITE_URL.replace(/\/$/, '') ? `${SITE_URL}/` : sansBarre;
        return item;
      },
    }),
  ],

  vite: {
    plugins: [tailwindcss()],
  },

  image: {
    // Formats modernes generes au build, avec repli automatique.
    responsiveStyles: true,
  },

  build: {
    inlineStylesheets: 'auto',
  },

  prefetch: {
    prefetchAll: true,
    defaultStrategy: 'hover',
  },
});
