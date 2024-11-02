import { type Ref, ref, shallowRef } from 'vue';
import { useDebounceFn } from '@vueuse/core';
import { defineStore } from 'pinia';
import { useFetch } from 'shared/composables';
import {
  useFetchOrderPricing,
  useFetchProceedCompliance,
  useFetchSupplyFuel
} from '@/services/order/fetchers';
import OrderReferences from '@/services/order/order-references';
import { useUpdateOrderPricing, useUpdateOrderRoi } from '@/services/order/updaters';
import { notify } from '@/helpers/toast';
import { DEFAULT_ORDER_ROI, DEFAULT_ORDER_ROI_DAYS } from '@/constants/order.constants';
import { useOrderStore } from './useOrderStore';

import type { IFuelPricingObj, SelectedSupplierInfo } from 'shared/types';
import type { IOrder } from '@/types/order/order.types';
import type { IOrderRoi, IRoiDays } from '@/types/order/order-reference.types';

export const useOrderReferenceStore = defineStore('OrderReference', () => {
  const orderStore = useOrderStore();
  const selectedSupplierIndex = shallowRef<number | null>(null);
  const selectedSupplierInfo = shallowRef<SelectedSupplierInfo | null>(null);
  const orderPricing: Ref<IFuelPricingObj | null> = ref(null);
  const orderRoi: Ref<IOrderRoi> = ref(DEFAULT_ORDER_ROI);
  const orderRoiDays: Ref<IRoiDays> = ref(DEFAULT_ORDER_ROI_DAYS);
  const wasOrderApprovalMessageShown = shallowRef(false);

  const { callFetch: fetchQuoteButton, data: quoteButton } = useFetch(
    OrderReferences.fetchOrderQuoteButton.bind(OrderReferences)
  );

  const proceedComplianceQuery = useFetchProceedCompliance({
    onSuccess: (data) => {
      const shouldNotify =
        data.order_approval.messages?.length && wasOrderApprovalMessageShown.value === false;

      if (shouldNotify) {
        notify(data.order_approval.messages.join('\n'), 'error');
        wasOrderApprovalMessageShown.value = true;
      }
    }
  });

  const {
    data: supplyFuel,
    callFetch: fetchSupplierFuel,
    loading: isLoadingSupplyFuel
  } = useFetchSupplyFuel();

  const { callFetch: fetchOrderPricing, loading: isLoadingOrderPricing } = useFetchOrderPricing({
    onSuccess: (data: IFuelPricingObj) => {
      orderPricing.value = data;
      const supplierIndex =
        supplyFuel.value?.results?.findIndex(
          (supplier: any) => supplier.supplier.pk === data.supplier_id
        ) ?? null;

      if (supplierIndex !== -1) {
        selectedSupplierIndex.value = supplierIndex;

        if (supplierIndex !== null && supplyFuel.value) {
          selectedSupplierInfo.value = {
            supplierId: supplyFuel.value?.id,
            detailsId: Number(supplyFuel.value?.results[supplierIndex]?.key)
          };
        }
      }

      orderRoiDays.value.client_days = data.terms_days?.client_terms_days;
      orderRoiDays.value.supplier_days = data.terms_days?.supplier_terms_days;
      if (
        orderStore?.order?.id &&
        orderRoiDays.value.client_days &&
        orderRoiDays.value.supplier_days
      ) {
        updateOrderRoi(orderStore.order.id);
      }
    }
  });

  const { callFetch: updateOrderPricing, loading: isLoadingUpdateOrderPricing } =
    useUpdateOrderPricing({
      orderPricing,
      orderRoiDays
    });

  const { callFetch: updateOrderRoi, loading: isLoadingUpdateOrderRoi } = useUpdateOrderRoi({
    order: orderStore.order,
    orderRoi,
    orderRoiDays,
    orderPricing
  });

  const onSelectSupplier = (supplierInfo: SelectedSupplierInfo) => {
    selectedSupplierInfo.value = supplierInfo;
  };

  const onRoiChange = useDebounceFn((nextValue: string, isClient) => {
    const numValue = parseInt(nextValue);
    if (isClient) {
      orderRoiDays.value.client_days = numValue;
    } else {
      orderRoiDays.value.supplier_days = numValue;
    }
    if (nextValue && orderStore.order?.id) {
      updateOrderRoi(orderStore.order.id);
    }
  }, 200);

  const initiateReferenceStore = async (
    orderId: number,
    orderPricingCalculationRecord: IOrder['pricing_calculation_record']
  ) => {
    await Promise.allSettled([
      fetchQuoteButton(orderId),
      fetchSupplierFuel(orderPricingCalculationRecord)
    ]);
  };

  return {
    fetchOrderPricing,
    fetchSupplierFuel,
    initiateReferenceStore,
    isLoadingSupplyFuel,
    isLoadingOrderPricing,
    isLoadingUpdateOrderPricing,
    isLoadingUpdateOrderRoi,
    onRoiChange,
    onSelectSupplier,
    orderPricing,
    orderRoi,
    orderRoiDays,
    proceedComplianceQuery,
    quoteButton,
    selectedSupplierIndex,
    selectedSupplierInfo,
    supplyFuel,
    updateOrderPricing,
    updateOrderRoi
  };
});
