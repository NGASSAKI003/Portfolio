/**
 * Retire de `dist` les fichiers qu'aucune page ne demande.
 *
 * Astro recopie dans `_astro/` les images d'origine des collections de contenu,
 * en plus des variantes webp qu'il en tire. Les variantes sont servies, les
 * originaux non : ils representaient 6,8 des 12,1 Mo de la construction, soit
 * plus de la moitie du poids televerse a chaque mise en ligne, pour rien.
 *
 * Le principe est volontairement bete et verifiable : on lit tout ce qui est
 * texte dans `dist`, on note les noms de fichiers qui y apparaissent, et on
 * supprime ceux de `_astro/` qui n'y sont jamais cites.
 *
 * Trois garde-fous, parce qu'une suppression ne se rattrape pas :
 *   on ne sort jamais de `dist/_astro/` ;
 *   on ne touche qu'aux images, jamais au code ni aux polices ;
 *   un nom cite une seule fois, ou qu'il soit, suffit a proteger le fichier.
 *
 * Lance automatiquement apres `npm run build`, via le script `postbuild`.
 */

import { readdir, readFile, stat, unlink } from 'node:fs/promises';
import { join, extname, relative } from 'node:path';
import { fileURLToPath } from 'node:url';

const RACINE = fileURLToPath(new URL('..', import.meta.url));
const DIST = join(RACINE, 'dist');
const ASTRO = join(DIST, '_astro');

// Ce qui peut etre supprime : uniquement des images. Le code, les polices et
// les fichiers de configuration restent, quoi qu'il arrive.
const IMAGES = new Set(['.png', '.jpg', '.jpeg', '.webp', '.avif', '.gif']);

// Ce qui est lu a la recherche de references.
const TEXTES = new Set(['.html', '.css', '.js', '.mjs', '.xml', '.txt', '.json', '.webmanifest', '']);

async function parcourir(dossier) {
  const entrees = await readdir(dossier, { withFileTypes: true });
  const fichiers = [];
  for (const e of entrees) {
    const chemin = join(dossier, e.name);
    if (e.isDirectory()) fichiers.push(...(await parcourir(chemin)));
    else fichiers.push(chemin);
  }
  return fichiers;
}

async function principal() {
  let fichiers;
  try {
    fichiers = await parcourir(DIST);
  } catch {
    console.log('  alleger-dist : pas de dossier dist, rien a faire');
    return;
  }

  // Tout le texte livre, concatene une seule fois.
  let references = '';
  for (const f of fichiers) {
    if (!TEXTES.has(extname(f).toLowerCase())) continue;
    references += await readFile(f, 'utf8');
  }

  let retires = 0;
  let octets = 0;
  for (const f of fichiers) {
    if (!f.startsWith(ASTRO)) continue;
    if (!IMAGES.has(extname(f).toLowerCase())) continue;
    const nom = f.split(/[\\/]/).pop();
    if (references.includes(nom)) continue;
    octets += (await stat(f)).size;
    await unlink(f);
    retires += 1;
  }

  if (retires === 0) {
    console.log('  alleger-dist : rien a retirer');
    return;
  }
  console.log(
    `  alleger-dist : ${retires} image(s) jamais demandee(s) retiree(s), ` +
      `${(octets / 1024 / 1024).toFixed(1)} Mo economises au televersement`,
  );
}

await principal();
