import React from "react";
import {
  TextField,
  Grid,
  MenuItem,
  FormControl,
  FormControlLabel,
  Radio,
  RadioGroup,
  Typography,
} from "@mui/material";
import { FormData } from "@/types/form";
import { OwnershipType, AdType } from "@/types/enums";

interface OwnershipDetailsProps {
  formData: FormData;
  onSelectChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
}

const OwnershipDetails: React.FC<OwnershipDetailsProps> = ({
  formData,
  onSelectChange,
}) => {
  return (
    <>
      <Grid item xs={12} sm={6}>
        <TextField
          fullWidth
          select
          label="Forma własności"
          name="ownership"
          value={formData.ownership}
          onChange={onSelectChange}
        >
          <MenuItem value={OwnershipType.OWNERSHIP}>Własność</MenuItem>
          <MenuItem value={OwnershipType.COOPERATIVE}>
            Spółdzielcze własnościowe
          </MenuItem>
          <MenuItem value={OwnershipType.OTHER}>Inne</MenuItem>
        </TextField>
      </Grid>

      <Grid item xs={12} sm={6}>
        <FormControl component="fieldset">
          <Typography variant="subtitle1" gutterBottom>
            Typ ogłoszeniodawcy
          </Typography>
          <RadioGroup
            name="ad_type"
            value={formData.ad_type}
            onChange={onSelectChange}
          >
            <FormControlLabel
              value={AdType.PRIVATE}
              control={<Radio />}
              label="Prywatny"
            />
            <FormControlLabel
              value={AdType.AGENCY}
              control={<Radio />}
              label="Biuro nieruchomości"
            />
          </RadioGroup>
        </FormControl>
      </Grid>
    </>
  );
};

export default OwnershipDetails;
