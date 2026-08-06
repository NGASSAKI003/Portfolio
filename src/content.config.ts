import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

/**
 * Un fichier Markdown par projet, valide au build.
 * Chaque entree produit une vraie page, sa propre canonique, son entree de
 * sitemap et son bloc JSON-LD. Ajouter un projet est un fichier, pas un chantier.
 */
const projets = defineCollection({
  loader: glob({ base: './src/content/projets', pattern: '**/*.{md,mdx}' }),
  schema: ({ image }) =>
    z.object({
      titre: z.string(),
      sousTitre: z.string(),
      // Sert de meta description et de resume OpenGraph : borne a la longueur utile.
      resume: z.string().min(70).max(185),
      role: z.string(),
      annee: z.number().int().min(2020).max(2100),
      periode: z.string().optional(),
      statut: z.enum(['en-ligne', 'en-cours', 'finaliste', 'archive']),
      vedette: z.boolean().default(false),
      ordre: z.number().int().default(99),

      pile: z.array(z.string()).min(1),
      domaines: z.array(z.string()).min(1),

      lienDemo: z.string().url().optional(),
      lienCode: z.string().url().optional(),
      lienDocument: z.string().optional(),

      couverture: image(),
      couvertureAlt: z.string().min(10),

      // Captures reelles du produit. Elles valent mieux que n'importe quelle
      // illustration : elles prouvent que la chose existe et fonctionne.
      galerie: z
        .array(
          z.object({
            image: image(),
            alt: z.string().min(10),
            legende: z.string().min(10),
          }),
        )
        .default([]),

      // Piece justificative : certificat, attestation, capture de resultat.
      // Une preuve visible vaut mieux qu'une affirmation.
      preuve: z
        .object({
          image: image(),
          alt: z.string().min(10),
          legende: z.string().min(10),
        })
        .optional(),

      chiffres: z
        .array(
          z.object({
            valeur: z.string(),
            libelle: z.string(),
            source: z.string().optional(),
          }),
        )
        .default([]),

      // Pilote le type d'entite declare a Google.
      typeSchema: z.enum(['SoftwareApplication', 'WebApplication', 'CreativeWork']),
      categorieApplication: z.string().optional(),
      systemeExploitation: z.string().optional(),
      datePublication: z.string().optional(),
      dateModification: z.string().optional(),
    }),
});

export const collections = { projets };
