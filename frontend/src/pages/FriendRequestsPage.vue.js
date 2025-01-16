/// <reference types="../../node_modules/.vue-global-types/vue_3.5_false.d.ts" />
import { defineComponent, ref, onMounted } from "vue";
export default defineComponent({
    setup() {
        const requests = ref([]);
        const fetchRequests = async () => {
            try {
                const response = await fetch("/api/friend-requests/", { credentials: "include" });
                if (response.ok) {
                    const data = await response.json();
                    requests.value = data.requests;
                }
                else {
                    console.error("Failed to fetch friend requests");
                }
            }
            catch (error) {
                console.error("Error fetching friend requests:", error);
            }
        };
        const respondToRequest = async (requestId, action) => {
            try {
                const response = await fetch("/api/respond-friend-request/", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": getCsrfToken(),
                    },
                    credentials: "include",
                    body: JSON.stringify({ request_id: requestId, action }),
                });
                if (response.ok) {
                    alert(`Friend request ${action}ed!`);
                    fetchRequests();
                }
                else {
                    console.error("Error responding to friend request");
                }
            }
            catch (error) {
                console.error("Error:", error);
            }
        };
        const getCsrfToken = () => {
            const name = "csrftoken";
            const value = `; ${document.cookie}`;
            const parts = value.split(`; ${name}=`);
            if (parts.length === 2)
                return parts.pop()?.split(";").shift() || "";
            return "";
        };
        onMounted(fetchRequests);
        return { requests, respondToRequest };
    },
});
; /* PartiallyEnd: #3632/script.vue */
function __VLS_template() {
    const __VLS_ctx = {};
    let __VLS_components;
    let __VLS_directives;
    __VLS_elementAsFunction(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({});
    __VLS_elementAsFunction(__VLS_intrinsicElements.h2, __VLS_intrinsicElements.h2)({});
    if (__VLS_ctx.requests.length) {
        __VLS_elementAsFunction(__VLS_intrinsicElements.ul, __VLS_intrinsicElements.ul)({});
        for (const [request] of __VLS_getVForSourceType((__VLS_ctx.requests))) {
            __VLS_elementAsFunction(__VLS_intrinsicElements.li, __VLS_intrinsicElements.li)({
                key: ((request.id)),
            });
            __VLS_elementAsFunction(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({});
            __VLS_elementAsFunction(__VLS_intrinsicElements.strong, __VLS_intrinsicElements.strong)({});
            (request.from_user.name);
            __VLS_elementAsFunction(__VLS_intrinsicElements.button, __VLS_intrinsicElements.button)({
                ...{ onClick: (...[$event]) => {
                        if (!((__VLS_ctx.requests.length)))
                            return;
                        __VLS_ctx.respondToRequest(request.id, 'accept');
                    } },
            });
            __VLS_elementAsFunction(__VLS_intrinsicElements.button, __VLS_intrinsicElements.button)({
                ...{ onClick: (...[$event]) => {
                        if (!((__VLS_ctx.requests.length)))
                            return;
                        __VLS_ctx.respondToRequest(request.id, 'reject');
                    } },
            });
        }
    }
    else {
        __VLS_elementAsFunction(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({});
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
