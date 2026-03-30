# Future Enhancements (Pull Request Ideas)

Local workflow integrations to consider upstream:

- **Component accessibility audit** — Scan ERB partials for common a11y issues (missing alt text, insufficient contrast in dark mode, missing aria-labels); auto-suggest fixes based on Tailwind best practices; integrate into `github-pr-writer` to flag accessibility concerns in PR reviews.

- **Dark mode validation across component library** — Automatically test all component partials with both light and dark mode enabled; warn if dark-mode pairs are missing (e.g., `dark:bg-gray-950` without `bg-white`); log uncovered components to mmlog for systematic hardening.

- **Responsive breakpoint consistency checking** — Analyze component partials and detect inconsistent breakpoint usage (some use `sm:`, others use `md:` for same feature); suggest standardization on workspace-wide breakpoint strategy and auto-refactor variants.

- **Component usage tracking and cleanup** — Track which partials are actually used in views; flag unused components in `references/components.md` for removal; log component lifecycle (creation, usage growth, deprecation) to ontology for visibility into design system health.

- **Tailwind class deduplication and compression** — Analyze all views for repeated class patterns and suggest extracting to reusable Tailwind `@apply` rules in global CSS or component utilities; estimate byte savings and suggest prioritization (pairs with `openclaw-token-optimizer` for context reduction if components moved to CSS).

Status: Prototype in local workspace; ready for contribution when time permits.
