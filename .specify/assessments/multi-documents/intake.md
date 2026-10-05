# Idea Intake: Traitement de plusieurs documents en une seule invocation

- **Slug**: multi-documents
- **Created**: 2026-10-05
- **Source**: pasted text
- **Type**: improvement

## Idea (as captured)

> J'envisage de permettre à l'outil de traiter plusieurs documents en une
> seule invocation.
>
> Règles :
>
> - un traitement par document : N documents input => N sorties
> - les paramètres de cleaning sont les mêmes pour tout les documents
> - L'outil repère seul s'il y a plusieurs docs ou un seul (si possible)
>
> notes :
>
> - les documents peuvent être ajoutés dans le chemin à la suite
>   ("md-cleaner doc1 doc2 doc3") ou à partir d'un dossier
>   ("md-cleaner dossierA").
> - dans le cas d'un dossier, seuls les MD sont traités, par les autres
>   documents. [sic : « pas les autres documents » présumé]
>
> arbitrage sur les commandes optionnelles : seules celles pouvant être
> appliquées à plusieurs docs gardent un rôle, les autres sont ignogées
> [sic : « ignorées » présumé] lorsque plusieurs documents sont proposés
> (dry-run, suggestion, etc.)

## Restated

Permettre à MD_Cleaner d'accepter plusieurs documents en une seule
invocation — listés sur la ligne de commande ou via un dossier — en
appliquant les mêmes paramètres de cleaning à chacun, avec une sortie par
document, et en ignorant les options non applicables au traitement en lot.

## Origin & Context

- **Raised by**: l'utilisateur (mainteneur du projet MD_Cleaner)
- **Trigger**: [NEEDS CLARIFICATION: événement ou besoin déclencheur non
  précisé]

## First-Glance Unknowns

- [NEEDS CLARIFICATION: dans le cas d'un dossier, la recherche des
  fichiers `.md` est-elle récursive (sous-dossiers) ou limitée au premier
  niveau ?]
- [NEEDS CLARIFICATION: peut-on mélanger documents individuels et
  dossiers dans une même invocation ("md-cleaner doc1.md dossierA") ?]
- [NEEDS CLARIFICATION: "les options ignorées" signifie-t-elle
  silencieusement ignorées, un avertissement, ou une erreur ?]
- [NEEDS CLARIFICATION: la détection "plusieurs docs ou un seul" — dans
  quels cas n'est-elle "pas possible", et quel est le comportement par
  défaut alors ?]
- [NEEDS CLARIFICATION: gestion des erreurs par document — si un document
  échoue, le traitement continue-t-il sur les suivants ou s'arrête-t-il ?]
- [NEEDS CLARIFICATION: nommage et emplacement des N sorties — où
  vont-elles quand les entrées viennent d'un dossier ?]
- [NEEDS CLARIFICATION: comportement attendu de la sortie console
  (résumé global vs détaillé par document) et interaction avec dry-run /
  suggestion]
- [NEEDS CLARIFICATION: les options globales actuelles (backup, output,
  etc.) s'appliquent-elles document par document ou globalement ?]
