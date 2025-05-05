import { useRef, useState } from "react";

export default function PhotoUpload() {
  const [imgSrc, setImgSrc] = useState<string>("");
  const fileEl = useRef<HTMLInputElement>(null);

  const displayFile = (file: File) => {
    const reader = new FileReader();
    reader.onloadend = () => {
      setImgSrc(reader.result as string);
    };
    reader.readAsDataURL(file);
  };

  const submit = (e: React.FormEvent) => {
    e.preventDefault();
    if (fileEl.current && fileEl.current.files) {
      const file = fileEl.current.files[0];
      const formData = new FormData();
      formData.append("file", file);

      fetch("http://localhost:8000/upload", {
        method: "POST",
        body: formData,
      })
        .then((response) => response.json())
        .then((data) => {
          console.log(data);
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    }
  };

  return (
    <div>
      <h1>Wczytaj zdjęcie</h1>
      <form onSubmit={submit}>
        <input
          type="file"
          accept="image/*"
          ref={fileEl}
          onChange={(e) => {
            if (e.target.files) {
              displayFile(e.target.files[0]);
            }
          }}
        />
        <div>
          <img src={imgSrc} />
        </div>
        <button type="submit">Wyślij</button>
      </form>
    </div>
  );
}
