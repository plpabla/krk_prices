import {
  HeatingType,
  StateType,
  MarketType,
  OwnershipType,
  AdType,
} from "./enums";

export interface FormData {
  name: string;
  area: string;
  rooms: string;
  heating: HeatingType;
  floor: string;
  rent: string;
  state: StateType;
  market: MarketType;
  ownership: OwnershipType;
  available: string;
  ad_type: AdType;
  extra_info: string;
}

export const defaultFormData: FormData = {
  name: "",
  area: "",
  rooms: "",
  heating: HeatingType.DISTRICT,
  floor: "",
  rent: "",
  state: StateType.READY_TO_MOVE,
  market: MarketType.SECONDARY,
  ownership: OwnershipType.OWNERSHIP,
  available: "",
  ad_type: AdType.PRIVATE,
  extra_info: "",
};
