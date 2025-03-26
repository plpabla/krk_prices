export enum HeatingType {
  DISTRICT = "miejskie",
  GAS = "gazowe",
  ELECTRIC = "elektryczne",
  OTHER = "inne",
}

export enum StateType {
  READY_TO_MOVE = "Do zamieszkania",
  NEEDS_RENOVATION = "Do remontu",
  NEEDS_FINISHING = "Do wykończenia",
}

export enum MarketType {
  PRIMARY = "Pierwotny",
  SECONDARY = "Wtórny",
}

export enum OwnershipType {
  OWNERSHIP = "Własnościowe",
  COOPERATIVE = "Spoldzielcze",
  OTHER = "Inne",
}

export enum AdType {
  PRIVATE = "prywatny",
  AGENCY = "biuro",
}

export enum AvailableType {
  NOW = "od zaraz",
  Y2025 = "2025",
  Y2026 = "2026",
  Y2027 = "2027",
  Y2028 = "2028+",
}

function convertEnumToDict<T extends { [key: string]: string }>(
  enumObj: T
): { [key: string]: keyof T } {
  const dict: { [key: string]: string } = {};

  Object.entries(enumObj).forEach(([key, value]) => {
    dict[key] = value;
  });

  return dict;
}

export const HeatingDict = convertEnumToDict(HeatingType);
export const StateDict = convertEnumToDict(StateType);
export const MarketDict = convertEnumToDict(MarketType);
export const OwnershipDict = convertEnumToDict(OwnershipType);
export const AdDict = convertEnumToDict(AdType);
export const AvailableDict = convertEnumToDict(AvailableType);
