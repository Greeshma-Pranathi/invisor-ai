# Invisor.ai Frontend

The modern, responsive user interface for the Invisor.ai customer intelligence platform. Built with React, Vite, and Tailwind CSS.

## 🛠️ Tech Stack

-   **Framework**: [React](https://react.dev/) + [Vite](https://vitejs.dev/)
-   **Styling**: [Tailwind CSS v4](https://tailwindcss.com/)
-   **Routing**: [React Router v6](https://reactrouter.com/)
-   **Charts**: [Recharts](https://recharts.org/)
-   **Icons**: [Lucide React](https://lucide.dev/)
-   **Animations**: [Framer Motion](https://www.framer.com/motion/)
-   **HTTP Client**: [Axios](https://axios-http.com/)

## 🚀 Getting Started

### Prerequisites
-   Node.js v18 or higher
-   npm or yarn

### Installation

1.  Navigate to the frontend directory:
    ```bash
    cd frontend
    ```

2.  Install dependencies:
    ```bash
    npm install
    ```

3.  Start the development server:
    ```bash
    npm run dev
    ```
    The app will run at `http://localhost:5173`.

## 📁 Project Structure

```
src/
├── 📂 api/          # API client and endpoints
├── 📂 components/   # Reusable UI components (Navbar, Cards)
├── 📂 pages/        # Page components (Dashboard, Upload, Analysis)
├── 📂 utils/        # Helper functions
├── 📄 App.jsx       # Main application component & Routing
├── 📄 main.jsx      # Entry point
└── 📄 index.css     # Global styles & Tailwind directives
```

## 🎨 Theme & Design

The application uses a custom "Void" theme with Golden and Purple accents.
-   **Background**: Deep Black (`#050505`) with radial glows.
-   **Primary**: Amber/Gold (`#FFAA00`)
-   **Accent**: Purple (`#A855F7`)
-   **Glassmorphism**: Used for cards and panels (`bg-white/5 backdrop-blur-sm`).

## 🧪 Scripts

-   `npm run dev`: Start dev server
-   `npm run build`: Build for production
-   `npm run preview`: Preview production build
-   `npm run lint`: Lint code with ESLint

## 🤝 Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for coding standards and guidelines.
