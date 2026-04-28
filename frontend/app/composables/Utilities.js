import now from '~build/time';
import { version } from "~build/package";

/** This is a utility that returns clean App Version Information. */
export function useAppVersion() {
    const release = ref({ date: "Released On: July 10, 2025", time: "(11:59pm)" });
    const num = ref("Version " + version);

    onMounted(() => {
        release.value.date = ("Released On: " + useDateFormat(now, "MMMM Do, YYYY").value);
        release.value.time = ("(" + useDateFormat(now, "h:mm A").value + ")");
    });
    return { release, num }
}

/**
 * This utility sets the necessary event listeners to enable any HTML element to use the pulse loop animation.
 * @param {import('vue').ShallowRef<HTMLElement>} container This is the main container to which the utility will apply to.
 */
export function usePulseLoopAnimation(container = null) {
    /** @type {MutationObserver} */
    var observer = null;

    /** @type {AbortController} */
    var controller = null;

    const enabled = ref(false);
    const numElements = ref(0);

    /** This function enables the pulse loop HTML Attribute. */
    async function enable() {
        if(enabled.value || container.value == null) { return; }
        await setEventListeners();
        
        if(observer == null) { observer = new MutationObserver(() => { setEventListeners(); }); }
        observer.observe(container.value, { childList: true, subtree: true })
        enabled.value = true;
    }

    /** This function disables the pulse loop HTML Attribute. */
    function disable() {
        if(!enabled.value) { return; }
        if(controller != null) { controller.abort(); }

        controller = null;
        observer.disconnect();
        numElements.value = 0;
        enabled.value = false;
    }

    /** This function runs the disable and then the enable function. Useful for if new elements are added. */
    async function reset() {
        disable();
        await enable();
    }

    /** This is a practical copy of {@link setPulseLoopAnimation}. */
    function animate(event) {
        if(event.type === "pointerenter" && event.pointerType === "mouse") {
            if(event.target.classList.contains('animate__animated')) { return; }
            event.target.classList.add('animate__animated', 'animate__pulse', 'animate__infinite');
        } else {
            if(!event.target.classList.contains('animate__pulse')) { return; }
            event.target.classList.remove('animate__animated', 'animate__pulse', 'animate__infinite');
        }
    }

    /** This function sets the necessary event listeners for those with the pulse-loop HTML Attribute. */
    async function setEventListeners() {
        if(controller != null) { controller.abort(); }
        controller = new AbortController();

        await nextTick();
        if(!container.value) { return; }

        const signal = controller.signal;
        const elements = container.value.querySelectorAll('[pulse-loop]');
        numElements.value = elements.length;

        if(container.value.hasAttribute("pulse-loop")) {
            container.value.addEventListener("pointerenter", (event) => { animate(event); }, { signal });
            container.value.addEventListener("mouseleave", (event) => { animate(event); }, { signal });
        }
        elements.forEach((element) => {
            element.addEventListener("pointerenter", (event) => { animate(event); }, { signal });
            element.addEventListener("mouseleave", (event) => { animate(event); }, { signal });
        });
    }

    onMounted(async() => { await enable(); });
    onBeforeUnmount(() => { disable(); });
    watch(container, () => { reset() });
    return { enabled, numElements, enable, disable, reset, animate }
}