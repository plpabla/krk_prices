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
  floor: number | null;
  floorsInBuilding: number | null;

  balcony: boolean;
  separate_kitchen: boolean;

  state: StateType;
  market: MarketType;
  ad_type: AdType;
  ownership: OwnershipType;

  heating: HeatingType;
  rent: number | null;
  available: string;
  extra_info: string;
}

export const defaultFormData: FormData = {
  location: "",
  city: "",
  district: "",

  area: null,
  rooms: null,
  floor: null,
  floorsInBuilding: null,

  balcony: false,
  separate_kitchen: false,

  heating: HeatingType.DISTRICT,
  rent: null,
  state: StateType.READY_TO_MOVE,
  market: MarketType.SECONDARY,
  ownership: OwnershipType.OWNERSHIP,
  available: "",
  ad_type: AdType.PRIVATE,
  extra_info: "",
};
