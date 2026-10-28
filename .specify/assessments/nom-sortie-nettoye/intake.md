# Idea Intake: Sortie nommée d'après l'entrée (`<titre>-nettoye`)

- **Slug**: nom-sortie-nettoye
- **Created**: 2026-10-05
- **Source**: pasted text (demande utilisateur dans la session CLI) ; pointeur
  codebase : `md_cleaner/cli.py`, `md_cleaner/sortie.py`
- **Type**: improvement

## Idea (as captured)

> Est-il possible de changer le titre par défaut du document de sortie ? je
> souhaiterais, à la place de "nettoye", avoir le titre du document d'input (les
> 20 premiers caractères) avec "-nettoye" après. Remplacer les espaces par "_".
>
> exemple :
>
> - input : "retry-failed-records.md"
> - output : "retry-failed-records-nettoye.md"

## Restated

L'utilisateur propose que le fichier nettoyé produit par l'outil soit nommé
d'après le document d'entrée (tronqué à 20 caractères, espaces remplacées par
`_`), suivi du suffixe `-nettoye`, au lieu du nom fixe actuel `nettoye.md`.

## Origin & Context

- **Raised by**: l'utilisateur du projet (propriétaire du dépôt), via la session
  CLI du 2026-10-05.
- **Trigger**: insatisfaction face au nom générique `nettoye.md` en sortie ;
  souhait de retrouver le document source dans le nom du fichier produit.
- **Codebase concerné (observation à la prise de note)** : la CLI écrit
  aujourd'hui `nettoye.md` (et `nettoye-pagine.md`, `cartographie.json`,
  `suggestion.json`, `rapport-dry-run.md`) dans un sous-dossier de run créé par
  `creer_dossier_run` (`md_cleaner/sortie.py`) — numéroté séquentiellement par
  défaut, ou slug du titre via `--nom-titre`.

## First-Glance Unknowns

- [NEEDS CLARIFICATION: « titre du document d'input » désigne-t-il le nom de
  fichier (stem, comme dans l'exemple) ou le premier titre `#` du contenu ?]
- [NEEDS CLARIFICATION: la demande porte-t-elle uniquement sur `nettoye.md`, ou
  aussi sur les autres sorties (`nettoye-pagine.md`, `rapport-dry-run.md`,
  `cartographie.json`) ?]
- [NEEDS CLARIFICATION: comportement attendu au-delà de 20 caractères —
  troncature brute, troncature au dernier mot entier, autre ?]
- [NEEDS CLARIFICATION: caractères autres que les espaces (accents, ponctuation,
  `/`, `\`, `:`) — faut-il les normaliser, et comment gérer les collisions de
  noms après troncature ?]
- [NEEDS CLARIFICATION: interaction avec le nommage actuel du dossier de run
  (`--nom-titre`) — le suffixe `-nettoye` s'applique-t-il au nom de fichier dans
  le dossier, ou remplace-t-il la logique de nommage du dossier ?]
- [NEEDS CLARIFICATION: option ou comportement par défaut ? le nommage actuel
  doit-il rester accessible ?]
