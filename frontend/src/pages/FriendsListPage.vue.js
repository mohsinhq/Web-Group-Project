/// <reference types="../../node_modules/.vue-global-types/vue_3.5_false.d.ts" />
import { defineComponent, ref, onMounted } from "vue";
import { useToast } from "vue-toastification";
export default defineComponent({
    setup() {
        const friends = ref([]);
        const loading = ref(false); // Track loading state for the remove button
        const toast = useToast(); // Initialize toast notifications
        const fetchFriends = async () => {
            try {
                const response = await fetch("/api/friends-list/", { credentials: "include" });
                if (response.ok) {
                    const data = await response.json();
                    friends.value = data.friends;
                }
                else {
                    toast.error("Failed to fetch friends."); // Show error toast
                    console.error("Failed to fetch friends:", await response.text());
                }
            }
            catch (error) {
                toast.error("Error fetching friends."); // Show error toast
                console.error("Error fetching friends:", error);
            }
        };
        const removeFriend = async (friendId) => {
            try {
                loading.value = true; // Set loading state
                const response = await fetch("/api/remove-friend/", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": getCsrfToken(),
                    },
                    credentials: "include",
                    body: JSON.stringify({ friend_id: friendId }),
                });
                if (response.ok) {
                    toast.success("Friend removed successfully!"); // Show success toast
                    // Update the UI by filtering out the removed friend
                    friends.value = friends.value.filter((friend) => friend.id !== friendId);
                }
                else {
                    const errorData = await response.json();
                    toast.error(errorData.message || "Failed to remove friend."); // Show error toast
                    console.error("Failed to remove friend:", errorData);
                }
            }
            catch (error) {
                toast.error("Error removing friend."); // Show error toast
                console.error("Error removing friend:", error);
            }
            finally {
                loading.value = false; // Reset loading state
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
        onMounted(fetchFriends);
        return { friends, removeFriend, loading };
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
    if (__VLS_ctx.friends.length) {
        __VLS_elementAsFunction(__VLS_intrinsicElements.ul, __VLS_intrinsicElements.ul)({});
        for (const [friend] of __VLS_getVForSourceType((__VLS_ctx.friends))) {
            __VLS_elementAsFunction(__VLS_intrinsicElements.li, __VLS_intrinsicElements.li)({
                key: ((friend.id)),
            });
            __VLS_elementAsFunction(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({});
            (friend.name);
            __VLS_elementAsFunction(__VLS_intrinsicElements.button, __VLS_intrinsicElements.button)({
                ...{ onClick: (...[$event]) => {
                        if (!((__VLS_ctx.friends.length)))
                            return;
                        __VLS_ctx.removeFriend(friend.id);
                    } },
                disabled: ((__VLS_ctx.loading)),
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
