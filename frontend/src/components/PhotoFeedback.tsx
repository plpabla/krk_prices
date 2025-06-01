import { PhotoFeedback as PhotoFeedbackProps } from "@/state/photoFeedback";

export default function PhotoFeedback({
  luxuryLevel,
  luxuryReason,
  pros,
  toFix,
  description,
}: PhotoFeedbackProps) {
  return (
    <>
      <h2>Analiza zdjęcia - poziom atrakcyjności: {luxuryLevel}/10</h2>
      <p>{luxuryReason}</p>
      <div>
        <h3>Co jest dobrze?</h3>
        <ul>
          {pros.map((item, index) => (
            <li key={index}>{item}</li>
          ))}
        </ul>
        <h3>Co można poprawić?</h3>
        <ul>
          {toFix.map((item, index) => (
            <li key={index}>{item}</li>
          ))}
        </ul>

        {description && (
          <div>
            <h3>Sugerowany opis</h3>
            <p>{description}</p>
          </div>
        )}
      </div>
    </>
  );
}
