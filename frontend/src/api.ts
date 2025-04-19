import { FormData } from "@/types/form";
import { City } from "@/types/backend";
import { PriceEstimate } from "@/types/backend";
import { usePriceStore } from "@/state/price";

export async function getCities(): Promise<string[]> {
  try {
    const response = await fetch(`/api/cities/`);
    const data = await response.json();
    return data.map((item: City) => item.name);
  } catch (error) {
    console.error(error);
    return [];
  }
}

export async function getDistricts(city: string): Promise<string[]> {
  try {
    const response = await fetch(`/api/cities/${city}`);
    const data = await response.json();
    return data.map((item: City) => item.name);
  } catch (error) {
    console.error(error);
    return [];
  }
}

export async function getPriceEstimate(data: FormData): Promise<void> {
  const { setPrice } = usePriceStore.getState();

  const response = await fetch(`/api/estimate`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  const res: PriceEstimate = await response.json();

  setPrice(res.price);
}
