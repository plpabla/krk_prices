import { City, PriceEstimate, ResPhoto } from "@/types/backend";
import { usePriceStore } from "@/state/price";
import { FormData as MyFormData } from "@/types/form";

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

export async function getPriceEstimate(data: MyFormData): Promise<void> {
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

  const response2 = await uploadPhotos(data.files, JSON.stringify(data));
  // TODO: handle the response2
  console.log(">>>>>> Photo response:", response2);
}

export async function uploadPhoto(file: File): Promise<ResPhoto> {
  const data = new FormData();
  data.append("file", file);

  const response = await fetch(`/api/upload`, {
    method: "POST",
    body: data,
  });

  if (!response.ok) {
    throw new Error("Failed to upload photo");
  }

  return await response.json();
}

export async function uploadPhotos(
  files: File[],
  form_data: string
): Promise<ResPhoto> {
  const data = new FormData();
  data.append("parameters", form_data);
  files.forEach((file) => {
    data.append("files", file);
  });

  const response = await fetch(`/api/upload`, {
    method: "POST",
    body: data,
  });

  if (!response.ok) {
    throw new Error("Failed to upload photos");
  }

  return await response.json();
}
