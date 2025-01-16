/// <reference types="../../node_modules/.vue-global-types/vue_3.5_false.d.ts" />
import { ref, onMounted } from "vue";
export default (await import('vue')).defineComponent({
    setup() {
        const usersWithSimilarities = ref([]); // List of users with their similar users
        const currentPage = ref(1); // Current page number
        const totalPages = ref(1); // Total number of pages
        const minAge = ref(null);
        const maxAge = ref(null);
        // Fetch users with optional age filters
        const fetchUsers = async (page = 1) => {
            let url = `http://localhost:8000/api/users/?page=${page}&per_page=10`;
            // Add age filters to the URL if set
            if (minAge.value !== null) {
                url += `&min_age=${minAge.value}`;
            }
            if (maxAge.value !== null) {
                url += `&max_age=${maxAge.value}`;
            }
            try {
                const response = await fetch(url);
                if (!response.ok) {
                    throw new Error("Failed to fetch users.");
                }
                const data = await response.json();
                console.log("API Response:", data);
                usersWithSimilarities.value = data.users; // Update with user data and similar users
                currentPage.value = data.current_page;
                totalPages.value = data.total_pages;
            }
            catch (error) {
                console.error("Error fetching users:", error);
            }
        };
        const sendFriendRequest = async (userId) => {
            try {
                const response = await fetch(`http://localhost:8000/api/send_friend_request/${userId}/`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value, // CSRF token
                    },
                });
                if (response.ok) {
                    alert("Friend request sent successfully!");
                }
                else {
                    const data = await response.json();
                    alert(data.error || "Failed to send friend request");
                }
            }
            catch (error) {
                console.error("Error sending friend request:", error);
            }
        };
        const acceptFriendRequest = async (requestId) => {
            try {
                const response = await fetch(`http://localhost:8000/api/accept_friend_request/${requestId}/`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value, // CSRF token
                    },
                });
                if (response.ok) {
                    alert("Friend request accepted!");
                }
                else {
                    const data = await response.json();
                    alert(data.error || "Failed to accept friend request");
                }
            }
            catch (error) {
                console.error("Error accepting friend request:", error);
            }
        };
        const isFriendRequestSent = (userId) => {
            // Logic to check if a request has been sent
            return usersWithSimilarities.value.some(user => user.user.id === userId && user.sent_request);
        };
        // Handle age filter button click
        const filterByAge = () => {
            fetchUsers(); // Fetch users with the new filter parameters
        };
        const changePage = (page) => {
            if (page >= 1 && page <= totalPages.value) {
                fetchUsers(page);
            }
        };
        onMounted(() => {
            fetchUsers(); // Fetch users on component mount
        });
        return {
            usersWithSimilarities,
            currentPage,
            totalPages,
            minAge,
            maxAge,
            filterByAge,
            changePage,
            sendFriendRequest,
            acceptFriendRequest,
            isFriendRequestSent,
        };
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
    __VLS_elementAsFunction(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
        ...{ class: ("age-filter") },
    });
    __VLS_elementAsFunction(__VLS_intrinsicElements.label, __VLS_intrinsicElements.label)({
        for: ("min-age"),
    });
    __VLS_elementAsFunction(__VLS_intrinsicElements.input)({
        type: ("number"),
        id: ("min-age"),
        placeholder: ("Min Age"),
        min: ("0"),
    });
    (__VLS_ctx.minAge);
    __VLS_elementAsFunction(__VLS_intrinsicElements.label, __VLS_intrinsicElements.label)({
        for: ("max-age"),
    });
    __VLS_elementAsFunction(__VLS_intrinsicElements.input)({
        type: ("number"),
        id: ("max-age"),
        placeholder: ("Max Age"),
        min: ("0"),
    });
    (__VLS_ctx.maxAge);
    __VLS_elementAsFunction(__VLS_intrinsicElements.button, __VLS_intrinsicElements.button)({
        ...{ onClick: (__VLS_ctx.filterByAge) },
    });
    __VLS_elementAsFunction(__VLS_intrinsicElements.table, __VLS_intrinsicElements.table)({
        ...{ class: ("table") },
    });
    __VLS_elementAsFunction(__VLS_intrinsicElements.thead, __VLS_intrinsicElements.thead)({});
    __VLS_elementAsFunction(__VLS_intrinsicElements.tr, __VLS_intrinsicElements.tr)({});
    __VLS_elementAsFunction(__VLS_intrinsicElements.th, __VLS_intrinsicElements.th)({});
    __VLS_elementAsFunction(__VLS_intrinsicElements.th, __VLS_intrinsicElements.th)({});
    __VLS_elementAsFunction(__VLS_intrinsicElements.th, __VLS_intrinsicElements.th)({});
    __VLS_elementAsFunction(__VLS_intrinsicElements.th, __VLS_intrinsicElements.th)({});
    __VLS_elementAsFunction(__VLS_intrinsicElements.th, __VLS_intrinsicElements.th)({});
    __VLS_elementAsFunction(__VLS_intrinsicElements.tbody, __VLS_intrinsicElements.tbody)({});
    for (const [userData, userIndex] of __VLS_getVForSourceType((__VLS_ctx.usersWithSimilarities))) {
        __VLS_elementAsFunction(__VLS_intrinsicElements.tr, __VLS_intrinsicElements.tr)({
            key: ((userData.user.id)),
        });
        __VLS_elementAsFunction(__VLS_intrinsicElements.td, __VLS_intrinsicElements.td)({});
        (userData.user.name);
        __VLS_elementAsFunction(__VLS_intrinsicElements.td, __VLS_intrinsicElements.td)({});
        (userData.user.email);
        __VLS_elementAsFunction(__VLS_intrinsicElements.td, __VLS_intrinsicElements.td)({});
        (userData.user.date_of_birth);
        __VLS_elementAsFunction(__VLS_intrinsicElements.td, __VLS_intrinsicElements.td)({});
        for (const [hobby, hobbyIndex] of __VLS_getVForSourceType((userData.user.hobbies))) {
            __VLS_elementAsFunction(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({
                key: ((hobbyIndex)),
            });
            (hobby);
            if (hobbyIndex < userData.user.hobbies.length - 1) {
                __VLS_elementAsFunction(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({});
            }
        }
        __VLS_elementAsFunction(__VLS_intrinsicElements.td, __VLS_intrinsicElements.td)({});
        if (!__VLS_ctx.isFriendRequestSent(userData.user.id)) {
            __VLS_elementAsFunction(__VLS_intrinsicElements.button, __VLS_intrinsicElements.button)({
                ...{ onClick: (...[$event]) => {
                        if (!((!__VLS_ctx.isFriendRequestSent(userData.user.id))))
                            return;
                        __VLS_ctx.sendFriendRequest(userData.user.id);
                    } },
            });
        }
        if (__VLS_ctx.isFriendRequestSent(userData.user.id)) {
            __VLS_elementAsFunction(__VLS_intrinsicElements.button, __VLS_intrinsicElements.button)({
                ...{ onClick: (...[$event]) => {
                        if (!((__VLS_ctx.isFriendRequestSent(userData.user.id))))
                            return;
                        __VLS_ctx.acceptFriendRequest(userData.user.id);
                    } },
            });
        }
    }
    __VLS_elementAsFunction(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({});
    __VLS_elementAsFunction(__VLS_intrinsicElements.button, __VLS_intrinsicElements.button)({
        ...{ onClick: (...[$event]) => {
                __VLS_ctx.changePage(__VLS_ctx.currentPage - 1);
            } },
        disabled: ((__VLS_ctx.currentPage <= 1)),
    });
    __VLS_elementAsFunction(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({});
    (__VLS_ctx.currentPage);
    (__VLS_ctx.totalPages);
    __VLS_elementAsFunction(__VLS_intrinsicElements.button, __VLS_intrinsicElements.button)({
        ...{ onClick: (...[$event]) => {
                __VLS_ctx.changePage(__VLS_ctx.currentPage + 1);
            } },
        disabled: ((__VLS_ctx.currentPage >= __VLS_ctx.totalPages)),
    });
    ['age-filter', 'table',];
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
