import { fileURLToPath } from "node:url";
import { addComponent } from "@nuxt/kit";

// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
    compatibilityDate: '2025-07-15',
    devtools: { enabled: false },
    app: { baseURL: "/", },
    devServer: { port: 5075, host: "localhost" },
    ssr: false,
    modules: [
        '@pinia/nuxt', '@nuxt/fonts', '@vueuse/nuxt', 'unplugin-info/nuxt',
        (_, nuxt) => {
            addComponent({
                name: 'FontAwesomeIcon',
                export: 'FontAwesomeIcon',
                filePath: "@fortawesome/vue-fontawesome"
            })
        }
    ],
    fonts: {
        families: [
            { name: "Poppins", provider: "fontsource" }
        ]
    },
    nitro: {
        output: {
            dir: ".output",
            publicDir: '.output/public'
        }
    },
    build: { transpile: ['pyodide'] },
    vite: { optimizeDeps: { exclude: ['pyodide'] } },
    experimental: { payloadExtraction: 'client' },
    alias: { '@scripts': fileURLToPath(new URL('./scripts', import.meta.url)) }
});