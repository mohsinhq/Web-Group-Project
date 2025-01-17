/// <reference types="../../node_modules/.vue-global-types/vue_3.5_false.d.ts" />
import { defineComponent, ref, onMounted } from "vue";
import { useToast } from "vue-toastification";
export default defineComponent({
    setup() {
        const requests = ref([]);
        const loading = ref({}); // Track loading state per request
        const toast = useToast();
        const fetchRequests = async () => {
            try {
                const response = await fetch("/api/friend-requests/", { credentials: "include" });
                if (response.ok) {
                    const data = await response.json();
                    requests.value = data.requests;
                }
                else {
                    toast.error("Failed to fetch friend requests.");
                    console.error("Failed to fetch friend requests:", await response.text());
                }
            }
            catch (error) {
                toast.error("Error fetching friend requests.");
                console.error("Error fetching friend requests:", error);
            }
        };
        const respondToRequest = async (requestId, action) => {
            try {
                loading.value[requestId] = true; // Set loading state for the specific request
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
                    toast.success(`Friend request ${action}ed!`);
                    // Update requests array to remove the handled request
                    requests.value = requests.value.filter((req) => req.id !== requestId);
                }
                else {
                    const errorData = await response.json();
                    toast.error(errorData.message || "Error responding to friend request.");
                    console.error("Error responding to friend request:", errorData);
                }
            }
            catch (error) {
                toast.error("Error responding to friend request.");
                console.error("Error:", error);
            }
            finally {
                loading.value[requestId] = false; // Reset loading state for the specific request
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
        return { requests, respondToRequest, loading };
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
                disabled: ((__VLS_ctx.loading[request.id])),
            });
            __VLS_elementAsFunction(__VLS_intrinsicElements.button, __VLS_intrinsicElements.button)({
                ...{ onClick: (...[$event]) => {
                        if (!((__VLS_ctx.requests.length)))
                            return;
                        __VLS_ctx.respondToRequest(request.id, 'reject');
                    } },
                disabled: ((__VLS_ctx.loading[request.id])),
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
