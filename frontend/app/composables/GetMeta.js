import og_img from "/Personal_Icon_Green_Expanded_Rounded.png";
export const WEBSITE_TITLE = "Tic-Tac-Toe | Algorithm Analysis Group 5 | CS 4306";
export const WEBSITE_DESC = "Tic-Tac-Toe";

/**
 * This function returns the meta tags for the website for Search Engine Optimization.
 * @param {String} pageTitle The document page title.
 * @param {String} pageRoute The link to the route.
 * @param {String} pageDesc The document meta description.
 * @param {String} bgColor This is the default background color for the webpage.
 * @param { "default" | "resume-extra" | "gamepad-extra" } type The type of webpage. Used if a page needs custom head tags compared to the default ones.
 */
export function getMeta(pageTitle = WEBSITE_TITLE, pageRoute = "", pageDesc = WEBSITE_DESC, bgColor = "rgb(0, 125, 0)") {
    const WEBSITE_PATH = (PROJECT_WEBSITE_LINK + pageRoute);
    
    /** @type {import("@unhead/vue").UseHeadInput} The resulting meta tags for the heading. */
    const output = {
        title: pageTitle,
        link: [
            { rel: 'icon', href: og_img },
            { rel: 'canonical', href: WEBSITE_PATH }
        ],
        htmlAttrs: { style: ("background-color: " + bgColor) },

        meta: [
            { name: 'description', content: pageDesc },
            { name: 'author', content: "Mohit Jain" },
            { name: 'robots', content: 'index, follow' },

            { property: 'og:site:name', content: "Mohit Jain" },
            { property: 'og:type', content: 'website' },
            { property: 'og:url', content: WEBSITE_PATH },
            { property: 'og:title', content: pageTitle },
            { property: 'og:description', content: pageDesc },
            { property: 'og:image', content: og_img },

            { property: 'twitter:card', content: "summary" },
            { property: 'twitter:url', content: WEBSITE_PATH },
            { property: 'twitter:title', content: pageTitle },
            { property: 'twitter:description', content: pageDesc },
            { property: 'twitter:image', content: og_img },
        ],
    }
    return output;
}

/**
 * This function returns the meta tags for the website for Search Engine Optimization.
 * This function is diferrent as the link is not predefined.
 * @param {String} pageTitle The document page title.
 * @param {String} pageLink The link to the website page.
 * @param {String} pageDesc The document meta description.
 */
export function getMetaWithLink(pageTitle = WEBSITE_TITLE, pageLink = PROJECT_WEBSITE_LINK, pageDesc = WEBSITE_DESC) {
    return {
        title: pageTitle,
        link: [{ rel: 'icon', href: og_img }],
        htmlAttrs: { style: "background-color: rgb(0, 125, 0)" },

        meta: [
            { name: 'description', content: pageDesc },
            { name: 'author', content: "Mohit Jain" },

            { "http-equiv": 'refresh', content: ("0; url=" + pageLink) },
            { name: 'robots', content: 'noindex, nofollow' },

            { property: 'og:site:name', content: "Mohit Jain" },
            { property: 'og:type', content: 'website' },
            { property: 'og:url', content: pageLink },
            { property: 'og:title', content: pageTitle },
            { property: 'og:description', content: pageDesc },
            { property: 'og:image', content: og_img },

            { property: 'twitter:card', content: "summary" },
            { property: 'twitter:url', content: pageLink },
            { property: 'twitter:title', content: pageTitle },
            { property: 'twitter:description', content: pageDesc },
            { property: 'twitter:image', content: og_img },
        ],
    };
}