import { TextField, Grid, Select, MenuItem } from "@mui/material";
import { useState, useEffect } from "react";
import { ResponsiveLabel } from "@/components/form-fields/Common";
import { FormData } from "@/types/form";

import { getCities, getDistricts } from "@/api";

interface LocationProps {
  formValues: FormData;
  handleChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  defaultDistrict: string | null;
}

function ListItems({
  label,
  items,
  formValue,
  handleChange,
}: {
  label: string;
  items: string[];
  formValue: string;
  handleChange: any;
}) {
  return (
    <Grid item xs={12} sm={4}>
      <Select
        label={label}
        id={label}
        name={label}
        value={formValue}
        onChange={handleChange}
        sx={{ width: "100%" }}
      >
        {items.map((item) => (
          <MenuItem key={item} value={item}>
            {item}
          </MenuItem>
        ))}
      </Select>
    </Grid>
  );
}

export default function Location({
  handleChange,
  formValues,
  defaultDistrict = null,
}: LocationProps) {
  const [cities, setCities] = useState<string[]>([]);
  const [districts, setDistricts] = useState<string[]>([]);
  const [touched, setTouched] = useState<boolean>(false);

  useEffect(() => {
    getCities().then((cities) => {
      setCities(cities);
      formValues.city = cities[0];
    });
  }, []);

  useEffect(() => {
    getDistricts(formValues.city).then((cities) => {
      setDistricts(cities);
      formValues.district = defaultDistrict || cities[0];
    });
  }, [formValues.city]);

  return (
    <Grid container spacing={2}>
      <ResponsiveLabel text="Miasto" />
      <ListItems
        label="city"
        items={cities}
        formValue={formValues.city}
        handleChange={handleChange}
      />

      <ResponsiveLabel text="Dzielnica" />
      <ListItems
        label="district"
        items={districts}
        formValue={formValues.district}
        handleChange={handleChange}
      />

      <Grid item xs={12}>
        <TextField
          fullWidth
          label="Pełny adres"
          name="location"
          onChange={handleChange}
          value={formValues.location}
          required
          error={touched && !formValues.location}
          helperText={
            touched && !formValues.location ? "To pole jest wymagane" : ""
          }
          onBlur={() => {
            if (!touched) {
              setTouched(true);
            }
          }}
        />
      </Grid>
    </Grid>
  );
}
