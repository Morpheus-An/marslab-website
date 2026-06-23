<style lang="less">
	header {
		a {
			position: relative;
			display: inline-block;

			p {
				padding: 5px 14px;
				font-size: 1.1rem;
				text-align: center;
				letter-spacing: 0.015em;
				color: var(--primary-color);
				background-color: transparent;
				border-radius: 7px;
				transition: color 0.2s ease, background 0.2s ease, box-shadow 0.2s ease;
			}

			/* Filled "Mars-gold" pill on hover and for the active section — a deep,
			   textured amber gradient (accent → accent-deep) with a soft top sheen and
			   a warm drop shadow so it reads premium rather than a flat block. */
			&:hover p,
			&.location p {
				color: #fff8ee;
				background: linear-gradient(150deg, var(--accent) 0%, var(--accent-deep) 100%);
				box-shadow:
					inset 0 1px 0 rgba(255, 244, 224, 0.28),
					inset 0 -1px 2px rgba(74, 31, 4, 0.30),
					0 2px 8px rgba(138, 61, 7, 0.30);
			}

			&.location p {
				font-weight: 600;
				/* slightly deeper + a touch more lift for the current page */
				background: linear-gradient(150deg, var(--accent-deep) 0%, #6f3005 100%);
				box-shadow:
					inset 0 1px 0 rgba(255, 244, 224, 0.30),
					inset 0 -1px 2px rgba(60, 24, 2, 0.35),
					0 3px 10px rgba(110, 48, 5, 0.34);
			}
	}
}

@media screen and (max-width: 640px) {
		nav {
			header {
				a {
					display: flex;
					gap: 0.5rem;

					p {
						padding: 0px;
							font-size: 1.1rem;
						white-space: nowrap;

						clip-path: none;
						color: var(--primary-color);
						background-color: var(--background-color);
					}

					&.location {
						font-weight: bold;
					}
				}
			}
		}
	}
</style>

<!-- svelte-ignore a11y_interactive_supports_focus -->
<!-- svelte-ignore a11y_click_events_have_key_events -->
<div role="button" onclick={() => (menu = false)} class:pointer-events-none={!menu} class:bg-transparent={!menu} class="fixed top-0 left-0 w-screen h-screen pointer-events-auto bg-#aaaaaa88 transition-background-color sm:hidden"></div>

<nav bind:this={navigator} class:transform-translate-x-full={!menu} class="fixed top-0 right-0 flex flex-col justify-between items-start gap-5 p-5 bg-background h-full sm:contents overflow-hidden transition-transform">
    <header class="grid gap-5 c-secondary grid-rows-[repeat(5,1fr)] sm:(grid-rows-none grid-cols-[repeat(4,1fr)])">
		<button onclick={() => (menu = false)} class="sm:hidden">{@render close()}</button>

		<a href={getUrl("/")} class:location={norm(route) === norm(getUrl("/")) || norm(route).startsWith(norm(getUrl("/preface")))}>
			<p>{t("navigation.home")}</p>
		</a>
        <a href={getUrl("/publications")} class:location={norm(route).startsWith(norm(getUrl("/publications")))}>
            <p>{t("navigation.publications") || "Publications"}</p>
        </a>
        <a href={getUrl("/people")} class:location={norm(route).startsWith(norm(getUrl("/people")))}>
            <p>{t("navigation.people")}</p>
        </a>
        <a href={getUrl("/contact")} class:location={norm(route).startsWith(norm(getUrl("/contact")))}>
			<p>{t("navigation.join") || "Contact"}</p>
		</a>
	</header>

	<footer class="flex flex-col gap-2 sm:gap-5 sm:(flex-row gap-7)">
	</footer>
</nav>

<button onclick={() => (menu = true)} class="sm:hidden">{@render bars()}</button>

<script lang="ts">
	import { i18n } from "astro:config/client";
	import { getRelativeLocaleUrl } from "astro:i18n";
	import { onMount, type Snippet } from "svelte";
	import i18nit from "$i18n";

	let { locale, route, baseUrl = '', home, note, jotting, people, about, sun, moon, bars, close }: { locale: string; route: string; baseUrl?: string } & { [key: string]: Snippet } = $props();

	const t = i18nit(locale);
	
	// Helper to construct full URL with base path and locale
	const getUrl = (path: string) => {
		// For home page (empty or "/"), use getRelativeLocaleUrl without path argument
		if (path === "/" || path === "") {
			return getRelativeLocaleUrl(locale);
		}
		// For other pages, use getRelativeLocaleUrl with the path
		return getRelativeLocaleUrl(locale, path);
	};

	// Normalise a path for comparison: drop a single trailing slash (GitHub Pages serves the home
	// and section pages WITH a trailing slash even though trailingSlash:never, so a raw `==` against
	// the slash-less href fails — that left the active highlight inconsistent between Home and the
	// other tabs). Comparing normalised paths makes all four nav items detect "active" identically.
	const norm = (s: string) => (s.length > 1 && s.endsWith("/") ? s.slice(0, -1) : s);

	// Control mobile menu visibility state
	let menu: boolean = $state(false);
	let navigator: HTMLElement | undefined = $state();

	onMount(() => {
		// Close mobile menu when any navigation link is clicked
		for (const link of navigator!.getElementsByTagName("a")) {
			link.addEventListener("click", () => (menu = false));
		}

		// Set up route tracking for page navigation with Swup integration
		const update_route = () => (route = window.location.pathname);
		if (window.swup) {
			// Register route update hook if Swup is already available.
			// Use page:view (fires after content replace + history/URL update, on every
			// actual visit incl. back/forward) — not page:load, which fires during fetch/
			// preload when window.location is stale and skips cached navigations, leaving
			// the active underline stuck on the previous page.
			window.swup.hooks.on("page:view", update_route);
		} else {
			// Wait for Swup to be enabled and then register the hook
			document.addEventListener("swup:enable", () => window.swup?.hooks.on("page:view", update_route));
		}
	});
</script>
