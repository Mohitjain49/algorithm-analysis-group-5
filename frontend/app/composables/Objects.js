import { faDiamond } from '@fortawesome/free-solid-svg-icons';

export const PROJECT_WEBSITE_LINK = "https://tictactoe.mohit-jain.com/";
export const PROJECT_GITHUB_LINK = "https://github.com/Mohitjain49/algorithm-analysis-group-5/";

/**
 * @type {Ref<import('@tsparticles/engine').IOptions>}
 * Refer to the tsParticles docs: https://particles.js.org/docs/
 * Refer to the tsParticles docs: https://particles.js.org/docs/documents/tsParticles_Engine.Options_Particles_Shape.html
 */
export const GREEN_BACKGROUND = ref({
    background: { color: "rgb(0, 125, 0)" },
    fullScreen: { enable: true },
    fpsLimit: 40,
    particles: {
        // color: { value: ["rgb(144, 238, 144)"] },
        move: {
            direction: "none",
            enable: true,
            outModes: { default: "out" },
            speed: 0.75,
            straight: false,
        },
        number: {
            density: { enable: true, area: 1200 },
            value: 400
        },
        opacity: {
            value: { min: 0.1, max: 0.75 },
            animation: { enable: true, speed: 1.5, sync: false },
        },
        shape: {
            type: "image",
            options: {
                image: [
                    { src: getFontAwesomeSvg(faDiamond, "rgb(144, 255, 144)"), width: 100, height: 100 },
                ]
            }
        },
        size: {
            value: { min: 5, max: 6 },
        },
    },
    detectRetina: true,
    tRetina: true,
});