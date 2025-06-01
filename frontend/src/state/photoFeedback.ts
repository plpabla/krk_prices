import { create } from "zustand";

export type PhotoFeedback = {
  luxuryLevel: number;
  luxuryReason: string;
  pros: string[];
  toFix: string[];
  description: string;
};

type PhotoFeedbackState = {
  feedback: PhotoFeedback;
  setFeedback: (data: PhotoFeedback) => void;
};

export const defaultPhotoFeedback: PhotoFeedback = {
  luxuryLevel: 0,
  luxuryReason: "",
  pros: [],
  toFix: [],
  description: "",
};

export const usePhotoFeedback = create<PhotoFeedbackState>((set) => ({
  feedback: defaultPhotoFeedback,
  setFeedback: (feedback: PhotoFeedback) => set({ feedback }),
}));
