import { defineConfig } from 'astro/config';
import netlify from '@astrojs/netlify';

import expressiveCode from 'astro-expressive-code';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
import spectre from './package/src';

import { spectreDark } from './src/ec-theme';

// https://astro.build/config
export default defineConfig({
  site: 'https://abhipatel.netlify.app/',
  output: 'static',
  integrations: [
    expressiveCode({
      themes: [spectreDark],
    }),
    mdx(),
    sitemap(),
    spectre({
      name: 'Abhi Patel',
      openGraph: {
        home: {
          title: 'Abhi Patel',
          description: 'Portfolio Site + Blog'
        },
        blog: {
          title: 'Bits & Giggles',
          description: 'Blog where I write about stuff'
        },
        projects: {
          title: 'Projects'
        }
      },
      // giscus: {
      //   repository: 'louisescher/spectre',
      //   repositoryId: 'R_kgDONjm3ig',
      //   category: 'General',
      //   categoryId: 'DIC_kwDONjm3is4ClmBF',
      //   mapping: 'pathname',
      //   strict: true,
      //   reactionsEnabled: true,
      //   emitMetadata: false,
      //   lang: 'en',
      // }
    })
  ],
  adapter: netlify(),
});