import "@fortawesome/fontawesome-svg-core/styles.css";

import { library, config } from '@fortawesome/fontawesome-svg-core';
import { fas } from '@fortawesome/free-solid-svg-icons';
import { faGithub, faGitAlt } from '@fortawesome/free-brands-svg-icons';
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";

config.autoAddCss = false;
library.add(fas, faGithub, faGitAlt);

export default defineNuxtPlugin((nuxtApp) => {
    nuxtApp.vueApp.component('font-awesome-icon', FontAwesomeIcon);
});