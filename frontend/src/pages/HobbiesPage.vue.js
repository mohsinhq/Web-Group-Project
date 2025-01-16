/// <reference types="../../node_modules/.vue-global-types/vue_3.5_false.d.ts" />
import { defineComponent, ref, onMounted } from "vue";
export default defineComponent({
    setup() {
        const hobbies = ref([]);
        const loading = ref(true);
        const error = ref(null);
        onMounted(async () => {
            try {
                const response = await fetch("/api/hobbies/", { credentials: "include" }); // Ensure the correct API path
                if (response.ok && response.headers.get("Content-Type")?.includes("application/json")) {
                    const data = await response.json();
                    hobbies.value = data.hobbies || [];
                }
                else if (response.status === 401) {
                    error.value = "You are not logged in. Please log in to view hobbies.";
                }
                else {
                    error.value = `Failed to fetch hobbies: ${response.statusText}`;
                }
            }
            catch (err) {
                error.value = "An unexpected error occurred while fetching hobbies.";
                console.error("Error fetching hobbies:", err);
            }
            finally {
                loading.value = false;
            }
        });
        return { hobbies, loading, error };
    },
});
; /* PartiallyEnd: #3632/script.vue */
function __VLS_template() {
    const __VLS_ctx = {};
    let __VLS_components;
    let __VLS_directives;
    __VLS_elementAsFunction(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({});
    __VLS_elementAsFunction(__VLS_intrinsicElements.h1, __VLS_intrinsicElements.h1)({});
    if (__VLS_ctx.loading) {
        __VLS_elementAsFunction(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({});
    }
    else if (__VLS_ctx.error) {
        __VLS_elementAsFunction(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({});
        (__VLS_ctx.error);
    }
    else if (__VLS_ctx.hobbies.length === 0) {
        __VLS_elementAsFunction(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({});
    }
    else {
        __VLS_elementAsFunction(__VLS_intrinsicElements.ul, __VLS_intrinsicElements.ul)({});
        for (const [hobby] of __VLS_getVForSourceType((__VLS_ctx.hobbies))) {
            __VLS_elementAsFunction(__VLS_intrinsicElements.li, __VLS_intrinsicElements.li)({
                key: ((hobby.id)),
            });
            (hobby.name);
        }
    }
    var __VLS_slots;
    var $slots;
    let __VLS_inheritedAttrs;
    var $attrs;
    const __VLS_refs = {};
    var $refs;
    var $el;
    return {
        attrs: {},
        slots: __VLS_slots,
        refs: $refs,
        rootEl: $el,
    };
}
;
let __VLS_self;
