import React from "react";
import {
  TextField,
  Grid,
  FormControl,
  FormControlLabel,
  Radio,
  RadioGroup,
  Typography,
  MenuItem,
  InputAdornment,
} from "@mui/material";
import { FormData } from "@/types/form";
import {
  HeatingType,
  StateType,
  MarketType,
  OwnershipType,
  AdType,
} from "@/types/enums";

interface FormFieldsProps {
  formData: FormData;
  onChange: (name: string, value: string | number | null) => void;
}

const FormFields: React.FC<FormFieldsProps> = ({ formData, onChange }) => {
  const handleTextChange = (
    event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    onChange(event.target.name, event.target.value);
  };

  const handleNumberChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = event.target;
    const numericValue = value === "" ? null : Number(value);
    onChange(name, numericValue);
  };

  const handleSelectChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    onChange(event.target.name, event.target.value);
  };

  return (
    <Grid container spacing={3}>
      <Grid item xs={12}>
        <TextField
          fullWidth
          label="Nazwa ogłoszenia"
          name="name"
          value={formData.name}
          onChange={handleTextChange}
        />
      </Grid>

      <Grid item xs={12} sm={6}>
        <TextField
          fullWidth
          label="Powierzchnia"
          name="area"
          type="number"
          value={formData.area ?? ""}
          onChange={handleNumberChange}
          InputProps={{
            endAdornment: <InputAdornment position="end">m²</InputAdornment>,
          }}
        />
      </Grid>

      <Grid item xs={12} sm={6}>
        <TextField
          fullWidth
          label="Liczba pokoi"
          name="rooms"
          type="number"
          value={formData.rooms ?? ""}
          onChange={handleNumberChange}
        />
      </Grid>

      <Grid item xs={12} sm={6}>
        <TextField
          fullWidth
          select
          label="Ogrzewanie"
          name="heating"
          value={formData.heating}
          onChange={handleSelectChange}
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
          label="Piętro"
          name="floor"
          type="number"
          value={formData.floor ?? ""}
          onChange={handleNumberChange}
        />
      </Grid>

      <Grid item xs={12} sm={6}>
        <TextField
          fullWidth
          label="Czynsz"
          name="rent"
          type="number"
          value={formData.rent ?? ""}
          onChange={handleNumberChange}
          InputProps={{
            endAdornment: <InputAdornment position="end">zł</InputAdornment>,
          }}
        />
      </Grid>

      <Grid item xs={12} sm={6}>
        <TextField
          fullWidth
          select
          label="Stan wykończenia"
          name="state"
          value={formData.state}
          onChange={handleSelectChange}
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
          onChange={handleSelectChange}
        >
          <MenuItem value={MarketType.PRIMARY}>Pierwotny</MenuItem>
          <MenuItem value={MarketType.SECONDARY}>Wtórny</MenuItem>
        </TextField>
      </Grid>

      <Grid item xs={12} sm={6}>
        <TextField
          fullWidth
          select
          label="Forma własności"
          name="ownership"
          value={formData.ownership}
          onChange={handleSelectChange}
        >
          <MenuItem value={OwnershipType.OWNERSHIP}>Własność</MenuItem>
          <MenuItem value={OwnershipType.COOPERATIVE}>
            Spółdzielcze własnościowe
          </MenuItem>
          <MenuItem value={OwnershipType.OTHER}>Inne</MenuItem>
        </TextField>
      </Grid>

      <Grid item xs={12} sm={6}>
        <TextField
          fullWidth
          label="Dostępne od"
          name="available"
          type="date"
          value={formData.available}
          onChange={handleTextChange}
          InputLabelProps={{
            shrink: true,
          }}
        />
      </Grid>

      <Grid item xs={12} sm={6}>
        <FormControl component="fieldset">
          <Typography variant="subtitle1" gutterBottom>
            Typ ogłoszeniodawcy
          </Typography>
          <RadioGroup
            name="ad_type"
            value={formData.ad_type}
            onChange={handleSelectChange}
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

      <Grid item xs={12}>
        <TextField
          fullWidth
          label="Informacje dodatkowe"
          name="extra_info"
          multiline
          rows={4}
          value={formData.extra_info}
          onChange={handleTextChange}
        />
      </Grid>
    </Grid>
  );
};

export default FormFields;
