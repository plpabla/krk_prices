# Running in dev environment

## Installation

1. Make sure you have Node.js 18+ installed on your system
2. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
3. Install dependencies using npm:
   ```bash
   npm install
   ```

## Run

To start the development server:

```bash
npm run dev
```

The application will be available at `http://localhost:5173` by default.

## Building and Deployment

### Local Build

To create a production build:

1. Create the build:

   ```bash
   npm run build
   ```

   This will generate the `dist` directory with optimized production files.

2. To preview the production build locally:
   ```bash
   npm run preview
   ```
   The preview server will start at `http://localhost:4173` by default.

### Deployment

The application is built using Vite and can be deployed to any static hosting service. Here are the general steps:

1. Create a production build as described above
2. Upload the contents of the `dist` directory to your hosting service
3. Configure your hosting service to:
   - Serve the `index.html` for all routes (for SPA support)
   - Set appropriate cache headers for static assets
   - Enable HTTPS (recommended)

Common hosting options include:

- Netlify
- Vercel
- GitHub Pages
- AWS S3 + CloudFront
- Firebase Hosting
