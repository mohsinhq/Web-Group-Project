/// <reference types=".vue-global-types/vue_3.5_false.d.ts" />
import { ref, onMounted } from 'vue';
const { defineProps, defineSlots, defineEmits, defineExpose, defineModel, defineOptions, withDefaults, } = await import('vue');
const hobbies = ref([]);
const newHobby = ref("");
const fetchHobbies = async () => {
    const response = await fetch("/hobbies/");
    const data = await response.json();
    hobbies.value = data.hobbies;
};
const addHobby = async () => {
    if (!newHobby.value)
        return;
    const response = await fetch("/hobbies/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: newHobby.value }),
    });
    if (response.ok) {
        await fetchHobbies();
        newHobby.value = "";
    }
};
onMounted(fetchHobbies);
const __VLS_fnComponent = (await import('vue')).defineComponent({});
;
let __VLS_functionalComponentProps;
function __VLS_template() {
    const __VLS_ctx = {};
    const __VLS_localComponents = {
        ...{},
        ...{},
        ...__VLS_ctx,
    };
    let __VLS_components;
    const __VLS_localDirectives = {
        ...{},
        ...__VLS_ctx,
    };
    let __VLS_directives;
    let __VLS_styleScopedClasses;
    let __VLS_resolvedLocalAndGlobalComponents;
    __VLS_elementAsFunction(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({});
    __VLS_elementAsFunction(__VLS_intrinsicElements.h1, __VLS_intrinsicElements.h1)({});
    __VLS_elementAsFunction(__VLS_intrinsicElements.form, __VLS_intrinsicElements.form)({ ...{ onSubmit: (__VLS_ctx.addHobby) }, });
    __VLS_elementAsFunction(__VLS_intrinsicElements.input)({ placeholder: ("Add a hobby"), });
    (__VLS_ctx.newHobby);
    __VLS_elementAsFunction(__VLS_intrinsicElements.button, __VLS_intrinsicElements.button)({ type: ("submit"), });
    __VLS_elementAsFunction(__VLS_intrinsicElements.ul, __VLS_intrinsicElements.ul)({});
    for (const [hobby] of __VLS_getVForSourceType((__VLS_ctx.hobbies))) {
        __VLS_elementAsFunction(__VLS_intrinsicElements.li, __VLS_intrinsicElements.li)({ key: ((hobby.id)), });
        (hobby.name);
    }
    var __VLS_slots;
    var __VLS_inheritedAttrs;
    const __VLS_refs = {};
    var $refs;
    return {
        slots: __VLS_slots,
        refs: $refs,
        attrs: {},
    };
}
;
const __VLS_self = (await import('vue')).defineComponent({
    setup() {
        return {
            hobbies: hobbies,
            newHobby: newHobby,
            addHobby: addHobby,
        };
    },
});
export default (await import('vue')).defineComponent({
    setup() {
        return {};
    },
});
;
