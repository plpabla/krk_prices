import {
  HeatingType,
  StateType,
  MarketType,
  OwnershipType,
  AdType,
} from "./enums";

export interface FormData {
  location: string;
  city: string;
  district: string;

  area: number | null;
  rooms: number | null;
  heating: HeatingType;
  floor: number | null;
  rent: number | null;
  state: StateType;
  market: MarketType;
  ownership: OwnershipType;
  available: string;
  ad_type: AdType;
  extra_info: string;
}

export const defaultFormData: FormData = {
  location: "",
  city: "",
  district: "",
  area: null,
  rooms: null,
  heating: HeatingType.DISTRICT,
  floor: null,
  rent: null,
  state: StateType.READY_TO_MOVE,
  market: MarketType.SECONDARY,
  ownership: OwnershipType.OWNERSHIP,
  available: "",
  ad_type: AdType.PRIVATE,
  extra_info: "",
};
