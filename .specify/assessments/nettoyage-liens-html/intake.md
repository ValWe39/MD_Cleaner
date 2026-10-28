# Idea Intake: Nettoyage optionnel des balises HTML dans le document de sortie

- **Slug**: nettoyage-liens-html
- **Created**: 2026-10-02
- **Source**: pasted text + repo path `output/004/nettoye.md`
- **Type**: improvement

## Idea (as captured)

> Est-il possible d'ajouter à l'outil une commande optionnelle, paramétrée activée
> par défaut, pour "nettoyer" les balises html du document de sortie : exemple :
> "(</fr/publications/lunion-departementale-des-associations-familiales-des-bouches-du-rhone>)"
> et "(</publications?f%5B1%5D=thematic%3A17182>)" ? sans toucher le reste du
> texte des lignes concernées.

Contexte observé dans `output/004/nettoye.md` : après nettoyage, il reste des
destinations de liens Markdown inline sous la forme `(</fr/publications/...>)`
ou `(</publications?f%5B1%5D=thematic%3A17182>)`, collées au texte des lignes
(titres et libellés de rubriques thématiques), par exemple :

```markdown
[Famille, handicap, sport et jeunesse](</publications?f%5B1%5D=...>) -
```

## Restated

Ajouter à MD_Cleaner une option de nettoyage, activée par défaut mais
désactivable, qui supprime du document de sortie les balises/destinations de
liens HTML résiduelles (de la forme `(</...>)`), en laissant le reste du texte
des lignes concernées inchangé.

## Origin & Context

- **Raised by**: l'utilisateur du dépôt (via /speckit-assess-intake) [NEEDS
  CLARIFICATION: identité exacte du demandeur]
- **Trigger**: constat de balises HTML résiduelles dans le fichier de sortie
  `output/004/nettoye.md` (nettoyage 004), notamment les destinations de liens
  inline de la source Cour des comptes.

## First-Glance Unknowns

- [NEEDS CLARIFICATION: périmètre exact de "balises html" — uniquement les
  destinations de liens inline `(</...>)`, ou aussi d'autres balises/attributs
  HTML éventuels dans les documents ?]
- [NEEDS CLARIFICATION: faut-il supprimer uniquement la destination `(</...>)`
  ou aussi les crochets du lien Markdown `[texte]`, en gardant le libellé du
  lien ?]
- [NEEDS CLARIFICATION: nom et forme du paramètre (ex. `--balises-html` /
  `--no-...`), cohérent avec les options existantes de l'outil]
- [NEEDS CLARIFICATION: à quelle étape du pipeline le nettoyage s'applique-t-il
  (règle de nettoyage dédiée, post-traitement, option de la feature 004 ?)]
- [NEEDS CLARIFICATION: comportement attendu quand la destination contient des
  caractères encodés (`%5B`, `%3A`) — supprimer telle quelle sans décodage ?]
