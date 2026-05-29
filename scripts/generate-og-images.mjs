import fs from 'node:fs/promises';
import path from 'node:path';
import sharp from 'sharp';

const ROOT = process.cwd();
const BLOG_DIR = path.join(ROOT, 'src/content/blog');
const OUT_DIR = path.join(ROOT, 'public/og/blog');
const DEFAULT_OUT = path.join(ROOT, 'public/og/default.png');
const WIDTH = 1200;
const HEIGHT = 630;

function escapeHtml(value) {
	return String(value)
		.replaceAll('&', '&amp;')
		.replaceAll('<', '&lt;')
		.replaceAll('>', '&gt;')
		.replaceAll('"', '&quot;')
		.replaceAll("'", '&#39;');
}

function parseFrontmatter(markdown) {
	const match = markdown.match(/^---\n([\s\S]*?)\n---/);
	if (!match) return {};

	const data = {};
	let currentKey = null;
	for (const rawLine of match[1].split('\n')) {
		const line = rawLine.replace(/\r$/, '');
		const keyValue = line.match(/^([A-Za-z0-9_-]+):\s*(.*)$/);
		if (keyValue) {
			currentKey = keyValue[1];
			const rawValue = keyValue[2].trim();
			if (rawValue === '') {
				data[currentKey] = '';
				continue;
			}
			data[currentKey] = rawValue.replace(/^['"]|['"]$/g, '');
			continue;
		}

		// Ignore nested arrays/objects: OG only needs scalar title/draft here.
		if (/^\s+-\s+/.test(line) || /^\s+[A-Za-z0-9_-]+:/.test(line)) {
			currentKey = currentKey;
		}
	}
	return data;
}

function wrapText(text, maxChars = 28, maxLines = 4) {
	const words = text.split(/\s+/).filter(Boolean);
	const lines = [];
	let line = '';

	for (const word of words) {
		const next = line ? `${line} ${word}` : word;
		if (next.length > maxChars && line) {
			lines.push(line);
			line = word;
		} else {
			line = next;
		}
	}
	if (line) lines.push(line);

	if (lines.length > maxLines) {
		const kept = lines.slice(0, maxLines);
		kept[maxLines - 1] = `${kept[maxLines - 1].replace(/[.…]+$/, '')}…`;
		return kept;
	}
	return lines;
}

function svgTemplate({ title, kicker = 'Labo IA Locale', subtitle = 'IA locale · open-source · self-hosting', isDefault = false }) {
	const lines = wrapText(title, isDefault ? 24 : 30, isDefault ? 2 : 4);
	const titleY = isDefault ? 272 : 210;
	const lineHeight = isDefault ? 86 : 74;
	const fontSize = isDefault ? 76 : 64;
	const titleSpans = lines
		.map((line, index) => `<tspan x="96" y="${titleY + index * lineHeight}">${escapeHtml(line)}</tspan>`)
		.join('');

	return `
<svg width="${WIDTH}" height="${HEIGHT}" viewBox="0 0 ${WIDTH} ${HEIGHT}" fill="none" xmlns="http://www.w3.org/2000/svg">
	<defs>
		<linearGradient id="bg" x1="0" y1="0" x2="1200" y2="630" gradientUnits="userSpaceOnUse">
			<stop stop-color="#061726"/>
			<stop offset="0.58" stop-color="#073042"/>
			<stop offset="1" stop-color="#0F766E"/>
		</linearGradient>
		<radialGradient id="glow" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate(895 140) rotate(135) scale(520 360)">
			<stop stop-color="#5EEAD4" stop-opacity="0.55"/>
			<stop offset="1" stop-color="#5EEAD4" stop-opacity="0"/>
		</radialGradient>
		<filter id="shadow" x="-20%" y="-20%" width="140%" height="140%" color-interpolation-filters="sRGB">
			<feDropShadow dx="0" dy="18" stdDeviation="24" flood-color="#020617" flood-opacity="0.28"/>
		</filter>
	</defs>
	<rect width="1200" height="630" fill="url(#bg)"/>
	<rect width="1200" height="630" fill="url(#glow)"/>
	<path d="M774 72C920 128 1010 262 1128 236" stroke="#99F6E4" stroke-opacity="0.26" stroke-width="2"/>
	<path d="M728 552C844 466 1002 456 1118 346" stroke="#CCFBF1" stroke-opacity="0.18" stroke-width="2"/>
	<g opacity="0.18">
		<circle cx="1006" cy="142" r="5" fill="#CCFBF1"/>
		<circle cx="1048" cy="222" r="4" fill="#CCFBF1"/>
		<circle cx="908" cy="512" r="5" fill="#CCFBF1"/>
		<circle cx="222" cy="520" r="4" fill="#CCFBF1"/>
	</g>
	<rect x="58" y="54" width="1084" height="522" rx="44" fill="#F8FAFC" fill-opacity="0.07" stroke="#CCFBF1" stroke-opacity="0.22" filter="url(#shadow)"/>
	<text x="96" y="128" fill="#99F6E4" font-family="Inter, Atkinson Hyperlegible, Arial, sans-serif" font-size="30" font-weight="700" letter-spacing="5">${escapeHtml(kicker.toUpperCase())}</text>
	<text fill="#F8FAFC" font-family="Inter, Atkinson Hyperlegible, Arial, sans-serif" font-size="${fontSize}" font-weight="800" letter-spacing="-2">${titleSpans}</text>
	<text x="96" y="512" fill="#CCFBF1" font-family="Inter, Atkinson Hyperlegible, Arial, sans-serif" font-size="30" font-weight="600">${escapeHtml(subtitle)}</text>
	<rect x="96" y="538" width="238" height="8" rx="4" fill="#2DD4BF"/>
</svg>`;
}

async function renderPng(svg, outputPath) {
	await fs.mkdir(path.dirname(outputPath), { recursive: true });
	await sharp(Buffer.from(svg)).png({ compressionLevel: 9 }).resize(WIDTH, HEIGHT).toFile(outputPath);
}

async function main() {
	await renderPng(
		svgTemplate({ title: 'Labo IA Locale', subtitle: 'Guides, tests et veille pour faire tourner l’IA chez soi', isDefault: true }),
		DEFAULT_OUT,
	);

	const entries = await fs.readdir(BLOG_DIR, { withFileTypes: true });
	let generated = 0;
	for (const entry of entries) {
		if (!entry.isFile() || !/\.mdx?$/.test(entry.name)) continue;

		const filePath = path.join(BLOG_DIR, entry.name);
		const markdown = await fs.readFile(filePath, 'utf8');
		const frontmatter = parseFrontmatter(markdown);
		if (String(frontmatter.draft).trim() === 'true') continue;

		const slug = entry.name.replace(/\.mdx?$/, '');
		const title = frontmatter.title || slug.replaceAll('-', ' ');
		await renderPng(svgTemplate({ title }), path.join(OUT_DIR, `${slug}.png`));
		generated += 1;
	}

	console.log(`Generated ${generated} article OG images and 1 default OG image.`);
}

main().catch((error) => {
	console.error(error);
	process.exit(1);
});
