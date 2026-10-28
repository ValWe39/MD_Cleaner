# Idea Intake: Nettoyage par défaut des balises et liens sans chevrons

- **Slug**: nettoyage-balises
- **Created**: 2026-10-27
- **Source**: pasted text (demande utilisateur) + pointeur codebase :
  `md_cleaner/nettoyage.py` (passe d'écriture) ; corpus de calibration :
  `Examples/Nettoyage-balises/` (5 fichiers FIPECO)
- **Type**: improvement

## Idea (as captured)

> Je veux nettoyer par défaut les liens et balises (sauf si `--conserver-liens`
> est activée par l'utilisateur).
>
> Je veux que tous les «
> (<https://www.budget.gouv.fr/documentation/file-download/30586>) » et autres
> balises et liens soient nettoyés.
>
> exemples :
>
> ```text
> (#main-content)
>
> [Lire →](/commentaire/Le%20patrimoine%20des%20...%20fin%202025)
>
> (/videos)
> ```
>
> **Attention** sans enlever le contenu du texte. Par exemple dans « [*tome II des
> voies et moyens*](https://www.budget.gouv.fr/documentation/file-download/30586)
> » je veux garder « *tome II des voies et moyens* »
>
> Tu peux (et dois) faire ton calibrage et tes exemples réels sur ce dossier :
> `Examples/Nettoyage-balises` (chemin relatif au dépôt ; la demande d'origine
> fournissait le chemin absolu correspondant)

## Restated

Étendre le nettoyage par défaut des destinations de liens à l'écriture de la
sortie (features 004/005) aux formes **sans chevrons** — `](/chemin)`,
`](#ancre)`, `](https://...)` — aujourd'hui exclues du périmètre, en conservant
les libellés et le texte utile, avec réversibilité par le drapeau existant
`--conserver-liens`.

## Origin & Context

- **Raised by**: l'utilisateur (session du 2026-10-27, suite à une investigation
  en lecture seule de la sortie `fipeco.fr-000033-nettoye.md` ligne 6).
- **Trigger**: corpus FIPECO inédit (sorties du dossier
  `FIPECO - sortie/Nettoyé/001`) : la regex actuelle `RE_DESTINATION_LIEN`
  (`md_cleaner/nettoyage.py:12`) ne cible que les destinations entre chevrons
  `](<...>)`, périmètre délibérément arbitré « hors scope » (option A) par la
  spec 005 faute d'occurrences dans les corpus d'alors. Les sorties FIPECO
  conservent donc des destinations sans chevrons collées au texte utile.
- **Corpus de calibration désigné par l'utilisateur** :
  `Examples/Nettoyage-balises/` — 5 fichiers `fipeco.fr-00003{3..7}-nettoye.md`
  (198, 147, 178, 198, 240 lignes ; 961 lignes au total). Inventaire rapide :
  **201 occurrences de liens sans chevrons**, **0 forme à chevrons restante**
  (les features 004/005 ont bien nettoyé ces dernières). Formes observées :
  ancres `(#main-content)`, `(#)`, relatives `(/)`, `(/fiches)`,
  `(/commentaire/...encodé)`, absolues `(<https://www.fipeco.fr/...)`>,
  `(<https://www.budget.gouv.fr/...)`>, partage
  `(<https://www.linkedin.com/sharing/...)`>,
  `(<https://www.facebook.com/sharer/...)`>.

## First-Glance Unknowns

- [NEEDS CLARIFICATION: Libellés de navigation pure —
  `[Aller au contenu principal]`, `[Lire →]` : après retrait de la destination,
  le libellé seul reste-t-il (cohérent avec 004/005) ou certaines lignes
  doivent-elles disparaître entièrement ? Relève de la passe liens ou de la
  détection de motifs ?]
- [NEEDS CLARIFICATION: Images `![alt](url)` — la regex étendue doit-elle les
  épargner systématiquement ?]
- [NEEDS CLARIFICATION: Formes à titre `](url "titre")` sans chevrons — titre
  retiré avec la destination comme en 005 ?]
- [NEEDS CLARIFICATION: Garde-fous à confirmer : URLs nues hors syntaxe de lien,
  blocs de code — reconduire le contrat de la spec 005 ?]
- [NEEDS CLARIFICATION: Les 201 occurrences sont-elles réparties uniformément ou
  concentrées dans des blocs de navigation qui seraient de toute façon candidats
  à suppression par motifs ?]
