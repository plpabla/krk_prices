import { useRef, useState } from "react";
import { Formik, Form, FormikHelpers } from "formik";

import { uploadPhoto } from "@/api";

interface FormValues {
  file: File | null;
}

export default function PhotoUpload() {
  const [imgSrc, setImgSrc] = useState<string>("");
  const fileRef = useRef<HTMLInputElement>(null);

  const displayFile = (file: File) => {
    const reader = new FileReader();
    reader.onloadend = () => {
      setImgSrc(reader.result as string);
    };
    reader.readAsDataURL(file);
  };

  const initialValues: FormValues = {
    file: null,
  };

  const handleSubmit = (
    values: FormValues,
    { setSubmitting }: FormikHelpers<FormValues>
  ) => {
    if (values.file) {
      const formData = new FormData();
      formData.append("file", values.file);

      uploadPhoto(values.file)
        .then((res) => {
          alert(`Zdjęcie (${res.filename}) zostało przesłane pomyślnie!`);
          console.log(res);
          setImgSrc("");
          if (fileRef.current) {
            fileRef.current.value = "";
          }
        })
        .catch((error) => {
          console.error("Error uploading photo:", error);
          alert("Wystąpił błąd podczas przesyłania zdjęcia.");
        })
        .finally(() => {
          setSubmitting(false);
        });
    }
  };

  return (
    <div>
      <h1>Wczytaj zdjęcie</h1>
      <Formik initialValues={initialValues} onSubmit={handleSubmit}>
        {({ setFieldValue, isSubmitting }) => (
          <Form>
            <input
              id="file"
              name="file"
              type="file"
              accept="image/*"
              ref={fileRef}
              onChange={(e) => {
                if (e.target.files) {
                  const file = e.target.files[0];
                  setFieldValue("file", file);
                  displayFile(file);
                }
              }}
            />
            <div>{imgSrc && <img src={imgSrc} alt="Preview" />}</div>
            <button type="submit" disabled={isSubmitting}>
              {isSubmitting ? "Wysyłanie..." : "Wyślij"}
            </button>
          </Form>
        )}
      </Formik>
    </div>
  );
}
