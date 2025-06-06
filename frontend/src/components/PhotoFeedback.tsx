import { PhotoFeedback as PhotoFeedbackProps } from "@/state/photoFeedback";

export default function PhotoFeedback({
  luxuryLevel,
  luxuryReason,
  pros,
  toFix,
  description,
}: PhotoFeedbackProps) {
  const photosFeedback = luxuryLevel != 0;

  return (
    <>
      <h2>
        {photosFeedback
          ? `Analiza zdjęcia - poziom atrakcyjności: ${luxuryLevel}/10`
          : ""}
      </h2>
      {photosFeedback && (
        <>
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
          </div>
        </>
      )}

      {description && (
        <div>
          <h3>Sugerowany opis</h3>
          <p>{description}</p>
        </div>
      )}
    </>
  );
}
