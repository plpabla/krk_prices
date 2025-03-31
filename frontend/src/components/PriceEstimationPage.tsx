import { Link } from "react-router-dom";

import { usePriceStore } from "@/state/price";

export default function PriceEstimationPage() {
  const { price } = usePriceStore();

  return (
    <>
      <div>
        <h1>Estymowana wycena: {price} PLN</h1>
      </div>
      <Link to="/">Powrót</Link>
    </>
  );
}
