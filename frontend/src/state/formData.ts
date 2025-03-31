import { create } from "zustand";

import { defaultFormData } from "@/types/form";
import { FormData } from "@/types/form";

type FormDataState = {
  formData: FormData;
  setFormData: (data: FormData) => void;
};

export const useFormStore = create<FormDataState>((set) => ({
  formData: defaultFormData,
  setFormData: (data: FormData) => set({ formData: { ...data } }),
}));
