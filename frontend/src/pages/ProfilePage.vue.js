/// <reference types="../../node_modules/.vue-global-types/vue_3.5_false.d.ts" />
import { defineComponent, ref, onMounted } from "vue";
export default defineComponent({
    name: "ProfilePage",
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
        const passwordData = ref({
            old_password: "",
            new_password: "",
            confirm_password: "",
        });
        const passwordMessage = ref("");
        const passwordLoading = ref(false);
        const fetchUserData = async () => {
            try {
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
                else {
                    message.value = `Failed to fetch user data: ${userResponse.statusText}`;
                }
                const hobbiesResponse = await fetch("/api/hobbies/", {
                    credentials: "include",
                });
                if (hobbiesResponse.ok) {
                    const data = await hobbiesResponse.json();
                    availableHobbies.value = data.hobbies || [];
                }
                else {
                    message.value = `Failed to fetch hobbies: ${hobbiesResponse.statusText}`;
                }
            }
            catch (error) {
                message.value = "Error fetching data. Please try again later.";
                console.error("Fetch error:", error);
            }
        };
        const saveProfile = async () => {
            try {
                loading.value = true;
                const csrfToken = getCookie("csrftoken");
                if (!csrfToken)
                    throw new Error("CSRF token not found.");
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
                message.value = "Error saving profile.";
                console.error("Save error:", error);
            }
            finally {
                loading.value = false;
            }
        };
        const changePassword = async () => {
            try {
                passwordLoading.value = true;
                const csrfToken = getCookie("csrftoken");
                if (!csrfToken)
                    throw new Error("CSRF token not found.");
                const response = await fetch("/api/change-password/", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": csrfToken,
                    },
                    body: JSON.stringify(passwordData.value),
                });
                if (response.ok) {
                    passwordMessage.value = "Password updated successfully!";
                    passwordData.value = { old_password: "", new_password: "", confirm_password: "" };
                }
                else {
                    const errorData = await response.json();
                    passwordMessage.value = errorData.error || "Failed to change password.";
                }
            }
            catch (error) {
                passwordMessage.value = "Error changing password.";
                console.error("Password error:", error);
            }
            finally {
                passwordLoading.value = false;
            }
        };
        const getCookie = (name) => {
            const value = `; ${document.cookie}`;
            const parts = value.split(`; ${name}=`);
            if (parts.length === 2)
                return parts.pop()?.split(";").shift() || null;
            return null;
        };
        onMounted(fetchUserData);
        return {
            profileData,
            availableHobbies,
            saveProfile,
            message,
            loading,
            passwordData,
            changePassword,
            passwordMessage,
            passwordLoading,
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
            for: ((`hobby-${hobby.id}`)),
        });
        __VLS_elementAsFunction(__VLS_intrinsicElements.input)({
            type: ("checkbox"),
            id: ((`hobby-${hobby.id}`)),
            value: ((hobby.id)),
        });
        (__VLS_ctx.profileData.hobbies);
        (hobby.name);
    }
    __VLS_elementAsFunction(__VLS_intrinsicElements.button, __VLS_intrinsicElements.button)({
        type: ("submit"),
        disabled: ((__VLS_ctx.loading)),
    });
    __VLS_elementAsFunction(__VLS_intrinsicElements.h2, __VLS_intrinsicElements.h2)({});
    __VLS_elementAsFunction(__VLS_intrinsicElements.form, __VLS_intrinsicElements.form)({
        ...{ onSubmit: (__VLS_ctx.changePassword) },
    });
    __VLS_elementAsFunction(__VLS_intrinsicElements.label, __VLS_intrinsicElements.label)({
        for: ("old_password"),
    });
    __VLS_elementAsFunction(__VLS_intrinsicElements.input)({
        id: ("old_password"),
        type: ("password"),
        required: (true),
    });
    (__VLS_ctx.passwordData.old_password);
    __VLS_elementAsFunction(__VLS_intrinsicElements.label, __VLS_intrinsicElements.label)({
        for: ("new_password"),
    });
    __VLS_elementAsFunction(__VLS_intrinsicElements.input)({
        id: ("new_password"),
        type: ("password"),
        required: (true),
    });
    (__VLS_ctx.passwordData.new_password);
    __VLS_elementAsFunction(__VLS_intrinsicElements.label, __VLS_intrinsicElements.label)({
        for: ("confirm_password"),
    });
    __VLS_elementAsFunction(__VLS_intrinsicElements.input)({
        id: ("confirm_password"),
        type: ("password"),
        required: (true),
    });
    (__VLS_ctx.passwordData.confirm_password);
    __VLS_elementAsFunction(__VLS_intrinsicElements.button, __VLS_intrinsicElements.button)({
        type: ("submit"),
        disabled: ((__VLS_ctx.passwordLoading)),
    });
    if (__VLS_ctx.loading) {
        __VLS_elementAsFunction(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({});
    }
    if (__VLS_ctx.message) {
        __VLS_elementAsFunction(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({
            ...{ class: ("success-message") },
        });
        (__VLS_ctx.message);
    }
    if (__VLS_ctx.passwordMessage) {
        __VLS_elementAsFunction(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({
            ...{ class: ("error-message") },
        });
        (__VLS_ctx.passwordMessage);
    }
    ['hobby-checkbox', 'success-message', 'error-message',];
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
