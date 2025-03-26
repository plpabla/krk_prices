import {
  HeatingType,
  StateType,
  MarketType,
  OwnershipType,
  AdType,
  AvailableDict,
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
  available: string;

  garage: boolean;
  elevator: boolean;
  basement: boolean;

  rent: number | null;
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
  available: AvailableDict.NOW,
  ad_type: AdType.PRIVATE,

  garage: false,
  elevator: false,
  basement: false,
};
