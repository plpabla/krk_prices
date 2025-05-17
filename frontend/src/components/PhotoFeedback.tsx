export interface PhotoFeedbackProps {
  luxuryLevel: number;
  type: string;
  pros: string[];
  to_fix: string[];
}

export const defaultPhotoFeedbackProps: PhotoFeedbackProps = {
  luxuryLevel: 0,
  type: "unknown",
  pros: [],
  to_fix: [],
};

export default function PhotoFeedback({ luxuryLevel }: PhotoFeedbackProps) {
  return <h2>Analiza zdjęcia - poziom luksusu: {luxuryLevel}/10</h2>;
}
