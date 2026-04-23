import { addComponent } from "@nuxt/kit";
import Info from "unplugin-info/vite";

// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
    compatibilityDate: '2025-07-15',
    devtools: { enabled: false },
    app: { baseURL: "/" },
    devServer: { port: 5075, host: "localhost" },
    ssr: false,
    modules: [
        '@pinia/nuxt', '@nuxt/fonts', '@vueuse/nuxt',
        (_, nuxt) => {
            addComponent({
                name: 'FontAwesomeIcon',
                export: 'FontAwesomeIcon',
                filePath: "@fortawesome/vue-fontawesome"
            })
        }
    ],
    vite: { plugins: [Info()] }
})