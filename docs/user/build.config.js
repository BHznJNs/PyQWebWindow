/** @type {import("basb-cli/types").SiteConfig} */
export default {
    homepage: "https://bhznjns.github.io/PyQWebWindow/",
    title: "PyQWebWindow Documentation",
    description: "The documentation for the Python GUI library PyQWebWindow.",
    footer: "::Powered by [BaSB](https://github.com/BHznJNs/BaSB)::",
    language: "en",
    pageSize: 20,

    preview: {
        port: 3030,
        liveReload: true,
    },

    catalog: {
        enable: true
    },
    fab: {
        enable: true,
        buttons: [
            "catalogSwitcher",
            "downsizeText",
            "enlargeText",
            "backToParent",
            "backToTop",
        ],
    },
    search: {
        enable: true,
        pageThreshold: 30000
    },

    echartsOptions: {
        tooltip: {
            show: true,
            backgroundColor: "rgb(255,255,255,.9)"
        }
    },

    qrcodeOptions: {
        width: 256,
        height: 256,
    }
}
