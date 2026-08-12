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
    /*
     * Une page par fichier, et non un dossier par page.
     *
     * En `directory`, Astro ecrit `projets/index.html`, et Cloudflare ne sert
     * cette adresse que sous `/projets/`, avec une barre oblique finale. Il
     * repondait donc 308 sur `/projets`, l'adresse meme que le sitemap declare
     * et que la canonique revendique : le moteur etait renvoye vers une page
     * qui le renvoyait aussitot d'ou il venait.
     *
     * En `file`, Astro ecrit `projets.html`, servi tel quel sur `/projets`.
     * Les adresses redeviennent celles qu'on annonce.
     *
     * Ne pas corriger cela en passant `trailingSlash` a `always` : les
     * identifiants JSON-LD des projets derivent de l'adresse, ils changeraient
     * tous, et c'est precisement ce qui ne doit jamais arriver.
     */
    format: 'file',
    inlineStylesheets: 'auto',
  },

  prefetch: {
    prefetchAll: true,
    defaultStrategy: 'hover',
  },
});
