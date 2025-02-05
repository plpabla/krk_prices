import React, { useState } from "react";
import {
  Box,
  TextField,
  Button,
  Typography,
  Container,
  Grid,
  FormControl,
  FormControlLabel,
  Radio,
  RadioGroup,
  MenuItem,
  InputAdornment,
} from "@mui/material";

interface FormData {
  name: string;
  price: string;
  area: string;
  rooms: string;
  heating: string;
  floor: string;
  rent: string;
  state: string;
  market: string;
  ownership: string;
  available: string;
  ad_type: string;
  extra_info: string;
}

const FlatEstimationForm: React.FC = () => {
  const [formData, setFormData] = useState<FormData>({
    name: "",
    price: "",
    area: "",
    rooms: "",
    heating: "",
    floor: "",
    rent: "",
    state: "",
    market: "",
    ownership: "",
    available: "",
    ad_type: "",
    extra_info: "",
  });

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = event.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    console.log(formData);
    // Here you would typically send the data to your backend
  };

  return (
    <Container maxWidth="md">
      <Box component="form" onSubmit={handleSubmit} sx={{ mt: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom align="center">
          Darmowa wycena mieszkania
        </Typography>

        <Grid container spacing={3}>
          <Grid item xs={12}>
            <TextField
              fullWidth
              label="Nazwa ogłoszenia"
              name="name"
              value={formData.name}
              onChange={handleChange}
            />
          </Grid>

          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="Cena"
              name="price"
              type="number"
              value={formData.price}
              onChange={handleChange}
              InputProps={{
                endAdornment: (
                  <InputAdornment position="end">zł</InputAdornment>
                ),
              }}
            />
          </Grid>

          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="Powierzchnia"
              name="area"
              type="number"
              value={formData.area}
              onChange={handleChange}
              InputProps={{
                endAdornment: (
                  <InputAdornment position="end">m²</InputAdornment>
                ),
              }}
            />
          </Grid>

          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="Liczba pokoi"
              name="rooms"
              type="number"
              value={formData.rooms}
              onChange={handleChange}
            />
          </Grid>

          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              select
              label="Ogrzewanie"
              name="heating"
              value={formData.heating}
              onChange={handleChange}
            >
              <MenuItem value="miejskie">Miejskie</MenuItem>
              <MenuItem value="gazowe">Gazowe</MenuItem>
              <MenuItem value="elektryczne">Elektryczne</MenuItem>
              <MenuItem value="inne">Inne</MenuItem>
            </TextField>
          </Grid>

          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="Piętro"
              name="floor"
              type="number"
              value={formData.floor}
              onChange={handleChange}
            />
          </Grid>

          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="Czynsz"
              name="rent"
              type="number"
              value={formData.rent}
              onChange={handleChange}
              InputProps={{
                endAdornment: (
                  <InputAdornment position="end">zł</InputAdornment>
                ),
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
              onChange={handleChange}
            >
              <MenuItem value="do_remontu">Do remontu</MenuItem>
              <MenuItem value="do_zamieszkania">Do zamieszkania</MenuItem>
              <MenuItem value="do_wykonczenia">Do wykończenia</MenuItem>
            </TextField>
          </Grid>

          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              select
              label="Rynek"
              name="market"
              value={formData.market}
              onChange={handleChange}
            >
              <MenuItem value="pierwotny">Pierwotny</MenuItem>
              <MenuItem value="wtorny">Wtórny</MenuItem>
            </TextField>
          </Grid>

          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              select
              label="Forma własności"
              name="ownership"
              value={formData.ownership}
              onChange={handleChange}
            >
              <MenuItem value="wlasnosc">Własność</MenuItem>
              <MenuItem value="spoldzielcze">
                Spółdzielcze własnościowe
              </MenuItem>
              <MenuItem value="inne">Inne</MenuItem>
            </TextField>
          </Grid>

          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="Dostępne od"
              name="available"
              type="date"
              value={formData.available}
              onChange={handleChange}
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
                onChange={handleChange}
              >
                <FormControlLabel
                  value="prywatny"
                  control={<Radio />}
                  label="Prywatny"
                />
                <FormControlLabel
                  value="biuro"
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
              onChange={handleChange}
            />
          </Grid>

          <Grid item xs={12}>
            <Button
              type="submit"
              variant="contained"
              fullWidth
              size="large"
              sx={{ mt: 2 }}
              color="primary"
            >
              Wyceniam
            </Button>
          </Grid>
        </Grid>
      </Box>
    </Container>
  );
};

export default FlatEstimationForm;
