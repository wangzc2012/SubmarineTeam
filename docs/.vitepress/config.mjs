import { defineConfig } from 'vitepress'

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "SubmarineTeam",
  description: "SubmarineTeam",
  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    nav: [
      { text: 'Home', link: '/' },
    ],

    socialLinks: [
      { icon: 'github', link: 'https://github.com/wangzc2012/SubmarineTeam' }
    ],

    footer: {
      copyright: "此网站由 wangzc2012 开发，TzzlStudio 大力支持",
    },

  }
})
