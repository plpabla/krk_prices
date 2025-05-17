export interface PhotoFeedbackProps {
  luxuryLevel: number;
}

export const defaultPhotoFeedbackProps: PhotoFeedbackProps = {
  luxuryLevel: 0,
};

export default function PhotoFeedback({ luxuryLevel }: PhotoFeedbackProps) {
  return <h2>Analiza zdjęcia - poziom luksusu: {luxuryLevel}/10</h2>;
}
