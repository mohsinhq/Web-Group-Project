/// <reference types="../../node_modules/.vue-global-types/vue_3.5_false.d.ts" />
import { defineComponent, ref, onMounted } from "vue";
export default defineComponent({
    name: "MainPage", // Adding a component name for better debugging
    setup() {
        const userData = ref(null);
        const loading = ref(true);
        const error = ref(null);
        const fetchUserData = async () => {
            try {
                const response = await fetch("/api/user-data/", { credentials: "include" }); // Correct API path
                if (response.ok) {
                    const data = await response.json();
                    userData.value = data;
                }
                else if (response.status === 401) {
                    error.value = "You are not logged in. Please log in to view your data.";
                }
                else {
                    error.value = `Failed to fetch user data: ${response.status} ${response.statusText}`;
                    console.error("Error details:", await response.text());
                }
            }
            catch (err) {
                error.value = "An unexpected error occurred while fetching user data.";
                console.error("Error fetching user data:", err);
            }
            finally {
                loading.value = false;
            }
        };
        onMounted(fetchUserData);
        return { userData, loading, error };
    },
});
; /* PartiallyEnd: #3632/script.vue */
function __VLS_template() {
    const __VLS_ctx = {};
    let __VLS_components;
    let __VLS_directives;
    // CSS variable injection 
    // CSS variable injection end 
    __VLS_elementAsFunction(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({});
    __VLS_elementAsFunction(__VLS_intrinsicElements.h1, __VLS_intrinsicElements.h1)({});
    if (__VLS_ctx.loading) {
        __VLS_elementAsFunction(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({});
    }
    else if (__VLS_ctx.error) {
        __VLS_elementAsFunction(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({
            ...{ class: ("error-message") },
        });
        (__VLS_ctx.error);
    }
    else {
        __VLS_elementAsFunction(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({});
        (__VLS_ctx.userData?.name);
    }
    ['error-message',];
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
