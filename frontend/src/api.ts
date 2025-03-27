import { FormData } from "@/types/form";
import { City } from "@/types/backend";
import { PriceEstimate } from "@/types/backend";
import { usePriceStore } from "@/state/price";

// TODO: maybe better read it form env variable so I can have different API_URL for production and development
const API_URL = "http://localhost:8001";

export async function getCities(): Promise<string[]> {
  try {
    const response = await fetch(`${API_URL}/cities`);
    const data = await response.json();
    return data.map((item: City) => item.name);
  } catch (error) {
    console.error(error);
    return [];
  }
}

export async function getDistricts(city: string): Promise<string[]> {
  try {
    const response = await fetch(`${API_URL}/cities/${city}`);
    const data = await response.json();
    return data.map((item: City) => item.name);
  } catch (error) {
    console.error(error);
    return [];
  }
}

export async function getPriceEstimate(data: FormData): Promise<void> {
  const { setPrice } = usePriceStore.getState();

  const response = await fetch(`${API_URL}/estimate`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  const res: PriceEstimate = await response.json();

  setPrice(res.price);
}
