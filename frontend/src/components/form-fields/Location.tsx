import React from "react";
import { TextField, Grid, Select, MenuItem } from "@mui/material";
import { FormData } from "@/types/form";
import { useState, useEffect } from "react";
import { getCities, getDistricts } from "@/api";

interface LocationProps {
  formValues: FormData;
  handleChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
}

function ResponsiveLabel({ text }: { text: string }) {
  return (
    <Grid
      item
      xs={12}
      sm={2}
      container
      alignItems="center"
      justifyContent={{ xs: "flex-start", sm: "flex-end" }}
    >
      {text}
    </Grid>
  );
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

export default function Location({ handleChange, formValues }: LocationProps) {
  const [cities, setCities] = useState<string[]>([]);
  const [districts, setDistricts] = useState<string[]>([]);

  useEffect(() => {
    getCities().then((cities) => {
      setCities(cities);
      formValues.city = cities[0];
    });
  }, []);

  useEffect(() => {
    getDistricts(formValues.city).then((cities) => {
      setDistricts(cities);
      formValues.district = cities[0];
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
        />
      </Grid>
    </Grid>
  );
}
