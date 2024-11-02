<template>
  <div
    class="order-sidebar flex bg-white rounded-md"
    :class="{ 'is-sidebar-closed': isSidebarClosed }"
  >
    <AddNoteModal
      ref="noteInput"
      :is-open="isModalOpened"
      name="note-modal"
      @modal-close="isModalOpened = false"
      @modal-submit.prevent=""
    />
    <div class="order-sidebar-content w-full flex flex-col">
      <div
        class="order-sidebar-content-header px-[0.75rem] py-[0.5rem] flex justify-between items-center"
      >
        {{ activeTab.name }}
        <Button
          v-if="activeTab.name === 'Notes'"
          class="button flex items-center gap-2"
          @click="isModalOpened = true"
        >
          <img src="../../assets/icons/plus.svg" alt="add" />
          Add Note
        </Button>
      </div>
      <ScrollBar class="my-[0.75rem] grow">
        <div
          v-if="activeTab.name === 'Notes'"
          class="order-sidebar-content-data px-[0.75rem] flex flex-col gap-3 max-h-full"
        >
          <div
            v-for="note in orderNotes"
            :key="note.id"
            class="order-sidebar-content-data-note border-0 rounded-lg p-[0.5rem] flex flex-col"
          >
            <div class="note-header">
              <div class="note-header-info flex gap-2 pb-2">
                <Avatar
                  :first-name="note.created_by?.details?.first_name"
                  :last-name="note.created_by?.details?.last_name"
                />
                <div class="note-header-info-wrap">
                  <div class="note-header-info-name">{{ note.created_by?.details?.full_name }}</div>
                  <div class="note-header-info-date">{{ toNoteTime(note.created_at) }}</div>
                </div>
              </div>
              <div class="note-header-actions"></div>
            </div>
            <div class="note-content flex">{{ note.content }}</div>
          </div>
        </div>
        <div v-else-if="activeTab.name === 'Chat'" class="order-sidebar-content-data"></div>
        <div v-else-if="activeTab.name === 'Activity'" class="order-sidebar-content-data">
          <ActivityLog />
        </div>
        <div v-else class="order-sidebar-content-data">No tab</div>
      </ScrollBar>
    </div>
    <div class="order-sidebar-menu w-2/12 py-[1rem] px-[0.75rem] flex flex-col gap-4">
      <div
        v-for="el in sidebar"
        :key="el.name"
        class="order-sidebar-menu-el flex flex-col items-center"
        :class="{ active: activeTab.name === el.name }"
        @click="changeTab(el)"
      >
        <div class="img-wrap flex items-center justify-center p-[0.5rem] border-0 rounded-lg">
          <img :src="getImageUrl(`assets/icons/${el.icon}.svg`)" :alt="el.icon" />
        </div>
        {{ el.name }}
      </div>

      <div
        class="close-sidebar img-wrap cursor-pointer flex items-center justify-center p-[0.5rem]"
        :class="{ 'is-closed': isSidebarClosed }"
        @click="changeSidebar"
      >
        <img src="../../assets/icons/sidebar-close.svg" alt="sidebar_close" />
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { type PropType, ref, watch } from 'vue';
import type { BaseValidation } from '@vuelidate/core';
import { Button } from 'shared/components';
import { useFetch } from '@/composables/useFetch';
import OrderReferences from '@/services/order/order-references';
import { getImageUrl } from '@/helpers';
import { toNoteTime } from '@/helpers/order';
import { ActivityLog } from '../datacomponent';
import Avatar from '../forms/Avatar.vue';
import ScrollBar from '../forms/ScrollBar.vue';
import AddNoteModal from '../modals/AddNoteModal.vue';

import type { IOrder, IOrderNote } from '@/types/order/order.types';

const props = defineProps({
  validationInfo: {
    type: Object as PropType<BaseValidation>,
    default: () => null
  },
  isLoading: {
    type: Boolean as PropType<boolean>,
    default: false
  },
  order: {
    type: Object as PropType<IOrder>,
    default: null
  }
});

const sidebar = ref([
  { name: 'Notes', icon: 'notes' },
  { name: 'Chat', icon: 'chat' },
  { name: 'Activity', icon: 'activity' }
]);

const activeTab = ref(sidebar.value[0]);
const isSidebarClosed = ref(true);

const isModalOpened = ref(false);

const { data: orderNotes, callFetch: fetchOrderNotes } = useFetch<
  IOrderNote[],
  (order: IOrder) => Promise<IOrderNote[]>
>(async (order: IOrder) => {
  return await OrderReferences.fetchOrderNotes(order!.id!);
});

function changeTab(el: any) {
  if (activeTab.value === el) {
    isSidebarClosed.value = !isSidebarClosed.value;
  } else {
    isSidebarClosed.value = false;
  }
  activeTab.value = el;
}

const changeSidebar = () => {
  isSidebarClosed.value = !isSidebarClosed.value;
};

watch(
  () => props.order,
  (order: IOrder) => {
    fetchOrderNotes(order);
  }
);
</script>

<style lang="scss">
.button {
  background-color: rgba(81, 93, 138, 1) !important;
  color: white !important;
  font-weight: 500 !important;
  font-size: 16px !important;
  @apply flex shrink-0 focus:shadow-none mb-0 mt-0 p-[0.5rem] px-4 rounded-xl #{!important};
}

.order-sidebar {
  justify-content: flex-end;
  width: 35%;

  &-content {
    &-header {
      font-size: 18px;
      font-weight: 600;
      color: theme('colors.main');
      border-bottom: 1px solid theme('colors.dark-background');
      min-height: 3.5rem;
    }

    &-data {
      height: 100%;
      max-height: 460px;
      // overflow-y: auto;

      &-note {
        background-color: rgba(255, 161, 0, 0.1);

        .note-header {
          &-info {
            &-name {
              font-size: 14px;
              font-weight: 600;
              color: rgba(39, 44, 63, 1);
            }

            &-date {
              font-size: 12px;
              font-weight: 400;
              color: rgba(82, 90, 122, 1);
            }
          }
        }

        .note-content {
          font-size: 15px;
          font-weight: 400;
          color: rgba(39, 44, 63, 1);
        }
      }

      &-activity {
        &:first-of-type {
          .order-activity-info-side {
            padding-top: 12px;
          }

          .line-top {
            display: none;
          }
        }

        &:last-of-type {
          .line-bottom {
            display: none;
          }
        }

        .order-activity-info {
          position: relative;

          &-name {
            color: rgba(39, 44, 63, 1);
            font-weight: 600;
            font-size: 14px;
          }

          &-date {
            color: rgba(133, 141, 173, 1);
            font-weight: 400;
            font-size: 12px;
          }

          &-side {
            .circle {
              height: 8px;
              width: 8px;
              background-color: rgba(255, 255, 255, 1);
              border: 2px solid rgba(125, 148, 231, 1);
              border-radius: 50%;
              left: -1rem;
            }

            .line-bottom {
              width: 1px;
              background-color: rgba(223, 226, 236, 1);
              border: 1px solid rgba(223, 226, 236, 1);
              height: 100%;
              top: 6px;
              left: 1.5px;
            }

            .line-top {
              width: 1px;
              background-color: rgba(223, 226, 236, 1);
              border: 1px solid rgba(223, 226, 236, 1);
              height: 12px;
              top: 6px;
              left: 1.5px;
            }
          }
        }

        .order-activity-data {
          color: rgba(39, 44, 63, 1);
          font-weight: 400;
          font-size: 15px;
        }
      }
    }
  }

  &.is-sidebar-closed {
    width: 73px;

    .order-sidebar-content {
      display: none;
      transition: 0.5s;
    }

    .order-sidebar-menu {
      width: 100%;
    }
  }

  &-menu {
    position: relative;
    border-left: 1px solid theme('colors.dark-background');
    max-width: 73px;

    &-el {
      color: theme('colors.main');
      font-size: 14px;
      font-weight: 500;
      cursor: pointer;

      .img-wrap {
        width: 40px !important;
        height: 40px !important;
      }

      img {
        width: 20px !important;
        height: 20px !important;
      }

      &.active {
        color: rgba(81, 93, 138, 1);

        .img-wrap {
          background-color: rgba(125, 148, 231, 0.1);
        }
      }
    }

    .close-sidebar {
      position: absolute;
      width: 100%;
      bottom: 1rem;
      left: 0;

      &.is-closed {
        transform: rotate(180deg);
      }
    }
  }
}
</style>
