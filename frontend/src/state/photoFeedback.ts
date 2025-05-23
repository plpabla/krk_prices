import { create } from "zustand";

type PhotoFeedback = {
  luxuryLevel: number;
};

type PhotoFeedbackState = {
  feedback: PhotoFeedback;
  setFeedback: (data: PhotoFeedback) => void;
};

const defaultPhotoFeedback: PhotoFeedback = {
  luxuryLevel: 0,
};

export const usePhotoFeedback = create<PhotoFeedbackState>((set) => ({
  feedback: defaultPhotoFeedback,
  setFeedback: (feedback: PhotoFeedback) => set({ feedback }),
}));
