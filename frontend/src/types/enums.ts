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
  PRIMARY = "pierwotny",
  SECONDARY = "wtorny",
}

export enum OwnershipType {
  OWNERSHIP = "wlasnosc",
  COOPERATIVE = "spoldzielcze",
  OTHER = "inne",
}

export enum AdType {
  PRIVATE = "prywatny",
  AGENCY = "biuro",
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
export const OwnershipDict = convertEnumToDict(OwnershipType);
