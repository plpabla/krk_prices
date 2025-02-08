import React from "react";
import { TextField, Grid } from "@mui/material";
import { FormData } from "@/types/form";

interface RoomDetailsProps {
  formData: FormData;
  onNumberChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
}

const RoomDetails: React.FC<RoomDetailsProps> = ({
  formData,
  onNumberChange,
}) => {
  return (
    <>
      <Grid item xs={12} sm={6}>
        <TextField
          fullWidth
          label="Liczba pokoi"
          name="rooms"
          type="number"
          value={formData.rooms ?? ""}
          onChange={onNumberChange}
        />
      </Grid>

      <Grid item xs={12} sm={6}>
        <TextField
          fullWidth
          label="Piętro"
          name="floor"
          type="number"
          value={formData.floor ?? ""}
          onChange={onNumberChange}
        />
      </Grid>
    </>
  );
};

export default RoomDetails;
