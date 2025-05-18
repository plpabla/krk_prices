export interface PhotoFeedbackProps {
  luxuryLevel: number;
  pros: string[];
  to_fix: string[];
  description: string;
}

export const defaultPhotoFeedbackProps: PhotoFeedbackProps = {
  luxuryLevel: 0,
  pros: [],
  to_fix: [],
  description: "",
};

export default function PhotoFeedback({
  luxuryLevel,
  pros,
  to_fix,
  description,
}: PhotoFeedbackProps) {
  return (
    <>
      <h2>Analiza zdjęcia - poziom luksusu: {luxuryLevel}/10</h2>
      <div>
        <h3>Co jest dobrze?</h3>
        <ul>
          {pros.map((item, index) => (
            <li key={index}>{item}</li>
          ))}
        </ul>
        <h3>Co można poprawić?</h3>
        <ul>
          {to_fix.map((item, index) => (
            <li key={index}>{item}</li>
          ))}
        </ul>

        {description && (
          <div>
            <h3>Opis:</h3>
            <p>{description}</p>
          </div>
        )}
      </div>
    </>
  );
}
