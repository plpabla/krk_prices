import { Link } from "react-router-dom";

import { usePriceStore } from "@/state/price";
import { usePhotoFeedback } from "@/state/photoFeedback";
import PhotoFeedback from "@/components/PhotoFeedback";

export default function PriceEstimationPage() {
  const { price } = usePriceStore();
  const { feedback } = usePhotoFeedback();

  if (price === -1) {
    return (
      <div>
        <h1>Wprowadzono niepoprawny adres</h1>
        <Link to="/">Powrót</Link>
      </div>
    );
  }

  return (
    <>
      <div>
        <h1>Estymowana wycena: {price} PLN</h1>
        <PhotoFeedback {...feedback} />
      </div>
      <Link to="/">Powrót</Link>
    </>
  );
}
