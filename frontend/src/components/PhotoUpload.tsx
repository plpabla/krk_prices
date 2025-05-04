export default function PhotoUpload() {
  return (
    <div>
      <h1>Wczytaj zdjęcie</h1>
      <input type="file" accept="image/*" />
      <button type="submit">Wczytaj</button>
    </div>
  );
}
