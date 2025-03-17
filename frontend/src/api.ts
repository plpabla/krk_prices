import { FormData } from "@/types/form";

export async function getCities(): Promise<string[]> {
  await new Promise((resolve) => setTimeout(resolve, 1000));
  const response: { [key: string]: string[] } = {
    cities: ["Kraków", "Warszawa", "Wrocław", "Poznań", "Gdańsk", "Łódź"],
  };
  return response.cities;
}

export async function getDistricts(city: string): Promise<string[]> {
  await new Promise((resolve) => setTimeout(resolve, 1000));
  const response = {
    Kraków: ["Stare Miasto", "Nowa Huta", "Krowodrza", "Podgórze"],
    Warszawa: ["Śródmieście", "Mokotów", "Ursynów", "Wola"],
    Wrocław: ["Stare Miasto", "Krzyki", "Fabryczna", "Psie Pole"],
    Poznań: ["Stare Miasto", "Jeżyce", "Wilda", "Grunwald"],
    Gdańsk: ["Stare Miasto", "Wrzeszcz", "Orunia", "Jasień"],
    Łódź: ["Bałuty", "Polesie", "Widzew", "Górna"],
  };
  // @ts-ignore
  return city in response ? response[city] : [];
}

export async function getPriceEstimate(data: FormData): Promise<number> {
  await new Promise((resolve) => setTimeout(resolve, 1000));
  alert(JSON.stringify(data, null, 2));
  return Math.floor(Math.random() * 1000000);
}
