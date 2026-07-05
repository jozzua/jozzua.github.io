# Repository Guidelines

## Project Structure & Module Organization

This repository is a small static GitHub Pages site for a personal online business card.

- `index.html` is the primary rendered page.
- `index.md`, `README.md`, and `params.json` contain legacy or GitHub Pages metadata/content.
- `stylesheets/` contains site CSS, including the main stylesheet and syntax highlighting styles.
- `javascripts/` contains small browser scripts such as `scale.fix.js` and analytics-related code.
- `CNAME` configures the custom GitHub Pages domain.

There is no dedicated application source tree, test directory, or asset pipeline. Keep new files close to their role: CSS in `stylesheets/`, JavaScript in `javascripts/`, and root-level metadata only when GitHub Pages expects it.

## Build, Test, and Development Commands

No package manager or build system is currently configured.

- `open index.html` previews the site locally in a browser on macOS.
- `python3 -m http.server 8000` serves the repository locally if browser security behavior requires HTTP.
- `git status --short --branch` checks pending changes before committing.

If adding tooling, document the exact command here and commit the relevant lockfile/configuration.

## Coding Style & Naming Conventions

Use plain HTML, CSS, and JavaScript. Match the existing compact style unless touching a larger block, then prefer readable indentation:

- HTML: two-space indentation for nested elements.
- CSS: one declaration per line in larger rules.
- JavaScript: keep scripts small and dependency-free unless a build step is introduced.
- Filenames: lowercase names are preferred for web assets, e.g. `stylesheets/site.css`.

Avoid unrelated rewrites or formatting churn in this repository.

## Testing Guidelines

There is no automated test framework. For changes, manually verify:

- `index.html` renders without console errors.
- Layout works at narrow and desktop widths.
- Links, custom domain behavior, and external resources still load.

For visual changes, include a before/after screenshot in the pull request when practical.

## Commit & Pull Request Guidelines

Recent commit history is informal, using short messages such as `Update Readme`. Prefer clearer imperative messages, for example:

- `Update landing page copy`
- `Adjust business card styling`
- `Document repository workflow`

Pull requests should include a short summary, the reason for the change, any manual verification performed, and screenshots for visible UI changes. Link related issues when one exists.
