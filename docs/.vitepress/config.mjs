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
    search: {
      provider:"local",
      options: {
        translations: {
          button:{
            buttonText: "搜索文档",
            buttonAriaLabel:"搜索文档",
          },
          modal: {
            noResultsText:"无法找到相关结果",
            resetButtonTitle:"清除查询条件",
            footer: {
              selectText:"选择",
              navigateText:"切换",
            },
          },
        },
      },
    },
    footer: {
      copyright: "此网站由 wangzc2012 开发，感谢 TzzlStudio 大力支持。",
    },

  }
})