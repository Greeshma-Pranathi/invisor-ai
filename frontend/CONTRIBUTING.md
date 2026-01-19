# Contributing to Invisor Frontend

## ⚛️ React Best Practices
-   **Functional Components**: Use functional components with hooks.
-   **Prop Types**: Use PropTypes or TypeScript interfaces (if TS is adopted) for type checking.
-   **Custom Hooks**: Extract reusable logic into custom hooks.

## 🎨 Styling Guidelines (Tailwind CSS)
-   **Utility First**: Use utility classes for layout and spacing.
-   **Theme Variables**: Use the defined CSS variables (`--color-primary-gold`, etc.) via Tailwind's theme config.
-   **Directives**: Use `@apply` in `index.css` for complex, reusable component styles (e.g., `.btn-gold`).

## 📁 File Naming
-   **Components**: PascalCase (e.g., `Navbar.jsx`, `KPICard.jsx`).
-   **Utilities**: camelCase (e.g., `formatDate.js`).
-   **Styles**: kebab-case (if using CSS modules, though we primarily use Tailwind).

## 🧹 Code Quality
-   Run `npm run lint` before committing.
-   Ensure no console logs are left in production code.
-   Use `Prettier` for consistent formatting.
