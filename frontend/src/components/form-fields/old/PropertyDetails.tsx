import React from "react";
import { TextField, Grid, MenuItem } from "@mui/material";
import { FormData } from "@/types/form";
import { HeatingType, StateType, MarketType } from "@/types/enums";

interface PropertyDetailsProps {
  formData: FormData;
  onSelectChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
}

const PropertyDetails: React.FC<PropertyDetailsProps> = ({
  formData,
  onSelectChange,
}) => {
  return (
    <>
      <Grid item xs={12} sm={6}>
        <TextField
          fullWidth
          select
          label="Ogrzewanie"
          name="heating"
          value={formData.heating}
          onChange={onSelectChange}
        >
          <MenuItem value={HeatingType.DISTRICT}>Miejskie</MenuItem>
          <MenuItem value={HeatingType.GAS}>Gazowe</MenuItem>
          <MenuItem value={HeatingType.ELECTRIC}>Elektryczne</MenuItem>
          <MenuItem value={HeatingType.OTHER}>Inne</MenuItem>
        </TextField>
      </Grid>

      <Grid item xs={12} sm={6}>
        <TextField
          fullWidth
          select
          label="Stan wykończenia"
          name="state"
          value={formData.state}
          onChange={onSelectChange}
        >
          <MenuItem value={StateType.NEEDS_RENOVATION}>Do remontu</MenuItem>
          <MenuItem value={StateType.READY_TO_MOVE}>Do zamieszkania</MenuItem>
          <MenuItem value={StateType.NEEDS_FINISHING}>Do wykończenia</MenuItem>
        </TextField>
      </Grid>

      <Grid item xs={12} sm={6}>
        <TextField
          fullWidth
          select
          label="Rynek"
          name="market"
          value={formData.market}
          onChange={onSelectChange}
        >
          <MenuItem value={MarketType.PRIMARY}>Pierwotny</MenuItem>
          <MenuItem value={MarketType.SECONDARY}>Wtórny</MenuItem>
        </TextField>
      </Grid>
    </>
  );
};

export default PropertyDetails;
