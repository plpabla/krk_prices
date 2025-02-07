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

# Building and Deployment

## Local Build

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

## Deployment

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

# Project structure

```
frontend/
├── src/                    # Source code directory
│   ├── assets/            # Static assets (images, fonts, etc.)
│   ├── components/        # React components
│   │   ├── form-fields/   # Form field components
│   │   ├── FormFields.tsx # Form fields container
│   │   ├── FlatEstimationForm.tsx # Main form component
│   │   └── Footer.tsx     # Footer component
│   ├── types/             # TypeScript type definitions
│   │   ├── form.ts        # Form-related types
│   │   └── enums.ts       # Enum definitions
│   ├── App.tsx            # Root application component
│   └── main.tsx           # Application entry point
├── public/                # Public static files
├── index.html            # HTML entry point
├── vite.config.ts        # Vite configuration
├── tsconfig.json         # TypeScript configuration
└── package.json          # Project dependencies and scripts
```

## Key Components

- `FlatEstimationForm`: Main form component for flat estimation
- `FormFields`: Container component managing form field sections
- `form-fields/`: Directory containing individual form field components:
  - `BasicInformation`: Basic property details
  - `RoomDetails`: Room-specific information
  - `AdditionalDetails`: Additional property features
  - `OwnershipDetails`: Property ownership information

## Type System

The application uses TypeScript with two main type definition files:

- `types/form.ts`: Contains form-related interfaces and types
- `types/enums.ts`: Contains enumerated types used throughout the application
