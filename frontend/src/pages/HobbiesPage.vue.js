/// <reference types="../../node_modules/.vue-global-types/vue_3.5_false.d.ts" />
import { defineComponent, ref } from "vue";
export default defineComponent({
    setup() {
        const users = ref([]);
        const pagination = ref({ currentPage: 1, hasNext: false, hasPrevious: false });
        const filters = ref({
            minAge: null,
            maxAge: null,
        });
        const fetchUsers = async (page = 1) => {
            try {
                const params = new URLSearchParams({
                    page: page.toString(),
                    ...(filters.value.minAge ? { min_age: filters.value.minAge } : {}),
                    ...(filters.value.maxAge ? { max_age: filters.value.maxAge } : {}),
                });
                const response = await fetch(`/api/similar-users/?${params.toString()}`, { credentials: "include" });
                if (response.ok) {
                    const data = await response.json();
                    users.value = data.users;
                    pagination.value = {
                        currentPage: data.current_page,
                        hasNext: data.has_next,
                        hasPrevious: data.has_previous,
                    };
                }
                else {
                    console.error("Failed to fetch users");
                }
            }
            catch (error) {
                console.error("Error fetching users:", error);
            }
        };
        const sendFriendRequest = async (userId) => {
            try {
                const csrfToken = getCsrfToken(); // Fetch the CSRF token
                const response = await fetch(`/api/send-friend-request/`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": csrfToken, // Include the CSRF token
                    },
                    credentials: "include",
                    body: JSON.stringify({ user_id: userId }),
                });
                if (response.ok) {
                    alert("Friend request sent!");
                }
                else {
                    const errorData = await response.json();
                    console.error("Error sending friend request:", errorData);
                }
            }
            catch (error) {
                console.error("Error:", error);
            }
        };
        // Helper function to retrieve CSRF token from cookies
        const getCsrfToken = () => {
            const name = "csrftoken";
            const value = `; ${document.cookie}`;
            const parts = value.split(`; ${name}=`);
            if (parts.length === 2)
                return parts.pop()?.split(";").shift() || "";
            return "";
        };
        const changePage = (newPage) => {
            fetchUsers(newPage);
        };
        // Fetch users on page load
        fetchUsers();
        return { users, filters, fetchUsers, sendFriendRequest, pagination, changePage };
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
    __VLS_elementAsFunction(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({});
    __VLS_elementAsFunction(__VLS_intrinsicElements.label, __VLS_intrinsicElements.label)({
        for: ("min-age"),
    });
    __VLS_elementAsFunction(__VLS_intrinsicElements.input)({
        id: ("min-age"),
        type: ("number"),
        placeholder: ("Min Age"),
    });
    (__VLS_ctx.filters.minAge);
    __VLS_elementAsFunction(__VLS_intrinsicElements.label, __VLS_intrinsicElements.label)({
        for: ("max-age"),
    });
    __VLS_elementAsFunction(__VLS_intrinsicElements.input)({
        id: ("max-age"),
        type: ("number"),
        placeholder: ("Max Age"),
    });
    (__VLS_ctx.filters.maxAge);
    __VLS_elementAsFunction(__VLS_intrinsicElements.button, __VLS_intrinsicElements.button)({
        ...{ onClick: (() => __VLS_ctx.fetchUsers()) },
    });
    if (__VLS_ctx.users.length) {
        __VLS_elementAsFunction(__VLS_intrinsicElements.ul, __VLS_intrinsicElements.ul)({});
        for (const [user] of __VLS_getVForSourceType((__VLS_ctx.users))) {
            __VLS_elementAsFunction(__VLS_intrinsicElements.li, __VLS_intrinsicElements.li)({
                key: ((user.id)),
            });
            __VLS_elementAsFunction(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({});
            __VLS_elementAsFunction(__VLS_intrinsicElements.strong, __VLS_intrinsicElements.strong)({});
            (user.name);
            __VLS_elementAsFunction(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({});
            __VLS_elementAsFunction(__VLS_intrinsicElements.strong, __VLS_intrinsicElements.strong)({});
            (user.age);
            __VLS_elementAsFunction(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({});
            __VLS_elementAsFunction(__VLS_intrinsicElements.strong, __VLS_intrinsicElements.strong)({});
            (user.hobby_count);
            __VLS_elementAsFunction(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({});
            __VLS_elementAsFunction(__VLS_intrinsicElements.strong, __VLS_intrinsicElements.strong)({});
            (user.hobbies.map(h => h.name).join(', '));
            __VLS_elementAsFunction(__VLS_intrinsicElements.button, __VLS_intrinsicElements.button)({
                ...{ onClick: (() => __VLS_ctx.sendFriendRequest(user.id)) },
            });
        }
    }
    else {
        __VLS_elementAsFunction(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({});
        __VLS_elementAsFunction(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({});
    }
    __VLS_elementAsFunction(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
        ...{ class: ("pagination") },
    });
    __VLS_elementAsFunction(__VLS_intrinsicElements.button, __VLS_intrinsicElements.button)({
        ...{ onClick: (() => __VLS_ctx.changePage(__VLS_ctx.pagination.currentPage - 1)) },
        disabled: ((!__VLS_ctx.pagination.hasPrevious)),
    });
    __VLS_elementAsFunction(__VLS_intrinsicElements.button, __VLS_intrinsicElements.button)({
        ...{ onClick: (() => __VLS_ctx.changePage(__VLS_ctx.pagination.currentPage + 1)) },
        disabled: ((!__VLS_ctx.pagination.hasNext)),
    });
    ['pagination',];
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
