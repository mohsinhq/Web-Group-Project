/// <reference types="../../node_modules/.vue-global-types/vue_3.5_false.d.ts" />
import { defineComponent, ref, onMounted } from "vue";
export default defineComponent({
    setup() {
        const friends = ref([]);
        const fetchFriends = async () => {
            try {
                const response = await fetch("/api/friends-list/", { credentials: "include" }); // Update endpoint if needed
                if (response.ok) {
                    const data = await response.json();
                    friends.value = data.friends;
                }
                else {
                    console.error("Failed to fetch friends", await response.text());
                }
            }
            catch (error) {
                console.error("Error fetching friends:", error);
            }
        };
        const removeFriend = async (friendId) => {
            try {
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
                    alert("Friend removed!");
                    // Update the UI by filtering out the removed friend
                    friends.value = friends.value.filter(friend => friend.id !== friendId);
                }
                else {
                    console.error("Failed to remove friend:", await response.text());
                }
            }
            catch (error) {
                console.error("Error removing friend:", error);
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
        return { friends, removeFriend };
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
