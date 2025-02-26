export async function getCities(): Promise<string[]> {
  await new Promise((resolve) => setTimeout(resolve, 1000));
  const response: { [key: string]: string[] } = {
    cities: ["Kraków", "Warszawa", "Wrocław", "Poznań", "Gdańsk"],
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
  };
  // @ts-ignore
  return city in response ? response[city] : [];
}
