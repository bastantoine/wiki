import { defineConfig } from "vitepress";
import { withMermaid } from "vitepress-plugin-mermaid";

let links = require("./links.json");

// https://vitepress.dev/reference/site-config
export default withMermaid(
  defineConfig({
    title: "Wiki",
    description: "A personal wiki",
    srcDir: "./build",
    base: "/wiki/",
    themeConfig: {
      sidebar: links,
      socialLinks: [{ icon: "github", link: "https://github.com/bastantoine" }],
      footer: {
        message:
          'Built using <a href="https://github.com/vuejs/vitepress">VitePress</a>. Released under the MIT License.',
        copyright: "Copyright © 2019-present Bastien ANTOINE",
      },
      outline: "deep",
    },
    markdown: {
      config(md) {
        // Fix to ensure proper rendering of inline code blocks
        // when they contain Vue template syntax, such as '{{ foo }}'
        // https://github.com/vuejs/vitepress/discussions/3724
        const defaultCodeInline = md.renderer.rules.code_inline!;
        md.renderer.rules.code_inline = (tokens, idx, options, env, self) => {
          tokens[idx].attrSet("v-pre", "");
          return defaultCodeInline(tokens, idx, options, env, self);
        };
      },
    },
    mermaidPlugin: {
      // https://emersonbottero.github.io/vitepress-plugin-mermaid/
      class: "mermaid",
    },
  })
);
