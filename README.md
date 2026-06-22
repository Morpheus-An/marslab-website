# MARS Lab Website

Source for the website of the **Multimodal embodied AI and Robotic Systems (MARS) Lab** at Nanyang Technological University (NTU), Singapore, led by [Prof. Jianfei Yang](https://marsyang.site/).

🌐 Live: **https://marslab.tech**

## Development

```sh
npm install
npm run dev     # local dev server at http://localhost:4321
npm run build   # static build → dist/
```

Content lives in `src/content/` (homepage, publications) and `src/data/people.ts` (members); profile images in `public/people/`. Built with [Astro](https://astro.build) and deployed to GitHub Pages via Actions on every push to `main`.

## Copyright & License

© 2026 MARS Lab @ NTU. Contact: jianfei.yang@ntu.edu.sg

- **Content** — all text, research descriptions, member photos, the MARS Lab name and logo, and other site content are **© MARS Lab** and licensed under **[CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/)** (Attribution · NonCommercial · NoDerivatives). Our content may **not** be reused commercially or in modified form, and must be credited. **Please do not clone this site as-is for another group** — reach out if you'd like to reuse something.
- **Code** — the underlying site template derives from the `thought` Astro theme and remains under **[GPL-3.0](LICENSE)**. Any reuse of the code must comply with GPL-3.0 (stay open-source and retain attribution).
