import { defineConfig } from 'vitepress'

let links = require('./links.json')

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "Wiki",
  description: "A personal wiki",
  srcDir: "./wiki",
  base: "/wiki/",
  themeConfig: {
    sidebar: links,
    socialLinks: [
      { icon: 'github', link: 'https://github.com/bastantoine' },
    ],
    footer: {
      message: 'Built using <a href="https://github.com/vuejs/vitepress">VitePress</a>. Released under the MIT License.',
      copyright: 'Copyright © 2019-present Bastien ANTOINE'
    },
    editLink: {
      pattern: 'https://github.com/bastantoine/wiki/edit/main/:path'
    }
  }
})
