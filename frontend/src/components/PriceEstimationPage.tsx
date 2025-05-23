import { Link } from "react-router-dom";

import { usePriceStore } from "@/state/price";
import { usePhotoFeedback } from "@/state/photoFeedback";

export default function PriceEstimationPage() {
  const { price } = usePriceStore();
  const { feedback } = usePhotoFeedback();
  const luxuryLevel = feedback.luxuryLevel;

  return (
    <>
      <div>
        <h1>Estymowana wycena: {price} PLN</h1>
        <h2>Poziom luksusu: {luxuryLevel}</h2>
      </div>
      <Link to="/">Powrót</Link>
    </>
  );
}
