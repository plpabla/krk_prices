import { create } from "zustand";

type PriceState = {
  price: number;
  setPrice: (price: number) => void;
};

export const usePriceStore = create<PriceState>((set) => ({
  price: 0,
  setPrice: (price: number) => set({ price }),
}));
