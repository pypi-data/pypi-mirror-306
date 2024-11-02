<template>
  <div v-if="isOpen" class="order-modal">
    <div class="order-modal-wrapper">
      <div ref="target" class="order-modal-container">
        <div class="order-modal-body">
          <OrderForm add-default-classes>
            <template #header>
              <div class="header w-full flex justify-between">
                <div class="text-[1.25rem] font-medium text-grey-1000">
                  Send Client Quote via Email
                </div>
                <button @click.stop="emit('modal-close')">
                  <img
                    width="12"
                    height="12"
                    src="../../assets/icons/cross.svg"
                    alt="delete"
                    class="close"
                  />
                </button>
              </div>
            </template>
            <template #content>
              <ScrollBar>
                <div class="form-body-wrapper">
                  <SelectField
                    v-model="selectedOptions"
                    label-text="Recepients"
                    label="display"
                    :options="organisationPeople ?? []"
                    :multiple="true"
                  ></SelectField>
                  <Label label-text="From" :required="false"></Label>
                  <div class="mb-4">john.doe@aml.global</div>
                  <InputField
                    v-model="subject"
                    class="w-full"
                    :is-validation-dirty="v$?.form?.$dirty"
                    :errors="v$?.form?.jobs?.job_title?.$errors"
                    label-text="Subject"
                    placeholder="Please enter subject"
                  />
                  <TextareaField
                    v-model="body"
                    class="w-full"
                    :is-validation-dirty="v$?.form?.$dirty"
                    :errors="v$?.form?.jobs?.job_title?.$errors"
                    label-text="Body Text"
                    placeholder="Please enter body text"
                  />
                </div>
              </ScrollBar>
            </template>
          </OrderForm>
        </div>
        <div class="order-modal-footer">
          <button class="modal-button cancel" @click.stop="emit('modal-close')">Cancel</button>
          <button class="modal-button submit" @click.stop="onValidate()">Submit</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, watch } from 'vue';
import OrderForm from '@/components/forms/OrderForm.vue';
import { usePersonFormStore } from '@/stores/usePersonFormStore';
import { personRules } from '@/utils/rulesForForms';
import useVuelidate from '@vuelidate/core';
import InputField from '../forms/fields/InputField.vue';
import { storeToRefs } from 'pinia';
import { useFetch } from 'shared/composables';
import OrderReferences from '@/services/order/order-references';
import { notify } from '@/helpers/toast';
import Label from '../forms/Label.vue';
import TextareaField from '../forms/fields/TextareaField.vue';
import type { IPerson } from '@/types/order/order-reference.types';
import SelectField from '../forms/fields/SelectField.vue';
import ScrollBar from '../forms/ScrollBar.vue';

const props = defineProps({
  isOpen: Boolean,
  organisationId: {
    type: Number,
    default: 0
  }
});

const emit = defineEmits(['modal-close', 'modal-submit']);

const selectedOptions = ref([]);

const target = ref(null);

const personFormStore = usePersonFormStore();

const { formModel } = storeToRefs(personFormStore);

const validationModel = ref({ form: formModel });

const v$ = ref(useVuelidate(personRules(), validationModel));

const subject = ref('');
const body = ref('');
// onClickOutside(target, () => emit('modal-close'))

const onValidate = async () => {
  const isValid = await v$?.value?.$validate();
  if (!isValid) {
    return notify('Error while submitting, form is not valid!', 'error');
  } else {
    emit('modal-submit');
    emit('modal-close');
  }
};

const { data: organisationPeople, callFetch: fetchOrganisationPeople } = useFetch<IPerson[]>(
  async (id: number) => {
    const data = await OrderReferences.fetchOrganisationPeople(id as number);
    return data;
  }
);

watch(
  () => props.organisationId,
  (value: any) => {
    fetchOrganisationPeople(value);
  }
);
</script>
