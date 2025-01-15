/// <reference types="../../node_modules/.vue-global-types/vue_3.5_false.d.ts" />
import { defineComponent, ref, onMounted } from "vue";
export default defineComponent({
    setup() {
        const profileData = ref({
            name: "",
            email: "",
            date_of_birth: "",
            hobbies: [],
        });
        const availableHobbies = ref([]);
        const message = ref("");
        const loading = ref(false);
        onMounted(async () => {
            try {
                // Fetch user profile data
                const userResponse = await fetch("/api/user-data/", {
                    credentials: "include",
                });
                if (userResponse.ok) {
                    const userData = await userResponse.json();
                    profileData.value = {
                        name: userData.name || "",
                        email: userData.email || "",
                        date_of_birth: userData.date_of_birth || "",
                        hobbies: Array.isArray(userData.hobbies)
                            ? userData.hobbies.map((hobby) => hobby.id)
                            : [],
                    };
                }
                // Fetch available hobbies
                const hobbiesResponse = await fetch("/api/hobbies/", {
                    credentials: "include",
                });
                if (hobbiesResponse.ok) {
                    const data = await hobbiesResponse.json();
                    availableHobbies.value = data.hobbies || [];
                }
            }
            catch (error) {
                console.error("Error fetching data:", error);
                message.value = "Failed to fetch data.";
            }
        });
        const saveProfile = async () => {
            try {
                loading.value = true;
                const csrfToken = getCookie("csrftoken") || "";
                const response = await fetch("/api/profile/", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": csrfToken,
                    },
                    body: JSON.stringify(profileData.value),
                });
                if (response.ok) {
                    message.value = "Profile updated successfully!";
                }
                else {
                    const errorData = await response.json();
                    message.value = errorData.error || "Failed to update profile.";
                }
            }
            catch (error) {
                console.error("Error saving profile:", error);
                message.value = "An error occurred.";
            }
            finally {
                loading.value = false;
            }
        };
        // Helper function to get CSRF token
        const getCookie = (name) => {
            const value = `; ${document.cookie}`;
            const parts = value.split(`; ${name}=`);
            if (parts.length === 2)
                return parts.pop()?.split(";").shift();
        };
        return { profileData, availableHobbies, saveProfile, message, loading };
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
    __VLS_elementAsFunction(__VLS_intrinsicElements.form, __VLS_intrinsicElements.form)({
        ...{ onSubmit: (__VLS_ctx.saveProfile) },
    });
    __VLS_elementAsFunction(__VLS_intrinsicElements.label, __VLS_intrinsicElements.label)({
        for: ("name"),
    });
    __VLS_elementAsFunction(__VLS_intrinsicElements.input)({
        value: ((__VLS_ctx.profileData.name)),
        id: ("name"),
        type: ("text"),
        required: (true),
    });
    __VLS_elementAsFunction(__VLS_intrinsicElements.label, __VLS_intrinsicElements.label)({
        for: ("email"),
    });
    __VLS_elementAsFunction(__VLS_intrinsicElements.input)({
        id: ("email"),
        type: ("email"),
        required: (true),
    });
    (__VLS_ctx.profileData.email);
    __VLS_elementAsFunction(__VLS_intrinsicElements.label, __VLS_intrinsicElements.label)({
        for: ("dob"),
    });
    __VLS_elementAsFunction(__VLS_intrinsicElements.input)({
        id: ("dob"),
        type: ("date"),
        required: (true),
    });
    (__VLS_ctx.profileData.date_of_birth);
    __VLS_elementAsFunction(__VLS_intrinsicElements.label, __VLS_intrinsicElements.label)({
        for: ("hobbies"),
    });
    __VLS_elementAsFunction(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({});
    for (const [hobby] of __VLS_getVForSourceType((__VLS_ctx.availableHobbies))) {
        __VLS_elementAsFunction(__VLS_intrinsicElements.label, __VLS_intrinsicElements.label)({
            key: ((hobby.id)),
            ...{ class: ("hobby-checkbox") },
        });
        __VLS_elementAsFunction(__VLS_intrinsicElements.input)({
            type: ("checkbox"),
            value: ((hobby.id)),
        });
        (__VLS_ctx.profileData.hobbies);
        (hobby.name);
    }
    __VLS_elementAsFunction(__VLS_intrinsicElements.button, __VLS_intrinsicElements.button)({
        type: ("submit"),
        disabled: ((__VLS_ctx.loading)),
    });
    if (__VLS_ctx.loading) {
        __VLS_elementAsFunction(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({});
    }
    if (__VLS_ctx.message) {
        __VLS_elementAsFunction(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({});
        (__VLS_ctx.message);
    }
    ['hobby-checkbox',];
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
