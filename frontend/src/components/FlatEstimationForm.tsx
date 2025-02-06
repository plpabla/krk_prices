import React, { useState } from "react";
import { Box, Button, Typography, Container, Grid } from "@mui/material";
import { FormData, defaultFormData } from "@/types/form";
import Footer from "./Footer";
import FormFields from "./FormFields";

const FlatEstimationForm: React.FC = () => {
  const [formData, setFormData] = useState<FormData>(defaultFormData);

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

        <FormFields formData={formData} onChange={handleChange} />

        <Grid container>
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
      <Box sx={{ mb: 8 }} />
      <Footer />
    </Container>
  );
};

export default FlatEstimationForm;
