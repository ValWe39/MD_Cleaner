# Research: Traitement multi-documents en une invocation

- **Feature**: 007-traitement-multi-documents
- **Date**: 2026-10-05
- **Sources**: `md_cleaner/cli.py` (lu intégralement), `md_cleaner/detection.py` (`charger_echantillon`), `md_cleaner/sortie.py`, `specs/001-nettoyage-md-repetitif/contracts/cli.md`, spec 007 et assessment `multi-documents`, plan de la feature 006 (précédent de structure).

## Décisions

### D1 — Argument positionnel variadique : `nargs="+"`

- **Decision** : l'argument positionnel `fichier` devient `entrees` avec `nargs="+"` et `type=Path` ; il reçoit un ou plusieurs chemins. Avec un seul chemin, `argparse` produit une liste à un élément — le chemin de code du mono-document est emprunté à l'identique (FR-005, SC-005).
- **Rationale** : `nargs="+"` garde l'invocation `md-cleaner doc.md` valide sans nouvelle syntaxe et rend zéro argument invalide (usage, code 3) — le contrat mono-document est préservé par construction.
- **Alternatives considered** : `nargs="*"` (rejeté : une invocation sans argument doit rester une erreur d'usage, pas un lot vide) ; sous-commande `md-cleaner lot ...` (rejeté : contredit la spec FR-001 « la ligne de commande DOIT accepter une ou plusieurs entrées positionnelles » et ajoute de la surface) ; option `--lot` (rejeté : même raison, et l'intake demande la détection seule).

### D2 — Résolution du lot : fonction pure dans un module nouveau `md_cleaner/lot.py`

- **Decision** : nouvelle fonction pure `resoudre_lot(entrees: list[Path]) -> tuple[list[Path], list[str]]` qui développe chaque entrée — un fichier `.md` existant est retenu tel quel ; un dossier existant est développé en ses fichiers `.md` de premier niveau triés par nom (`suffix.lower() == ".md"`, `iterdir()` non récursif, tri par `name`, précédent `charger_echantillon`) ; un dossier sans aucun `.md` est ignoré avec un message explicite ajouté à la liste des avertissements ; un chemin inexistant ou non-`.md` listé directement est conservé tel quel dans le lot (il échouera au traitement avec l'erreur d'entrée actuelle, code 1, signalé par document — FR-007).
- **Rationale** : isole la seule logique nouvelle (détection fichier/dossier, ordre, filtrage) en une fonction pure testée isolément ; `cli.py` reste un aiguillage ; le tri non récursif par nom réutilise la convention éprouvée de `--echantillon` (FR-012) et évite le piège structurel d'`Examples/` (Sample + Input mélangés, cf. assessment research.md).
- **Alternatives considered** : réutiliser `charger_echantillon` (rejeté : il segmente en pages, plafonne à 5 et échoue si vide — sémantique de calibrage, pas de lot) ; tout inline dans `cli.py` (rejeté : `cli.py` atteint ~230 lignes, la fonction pure mérite ses tests unitaires dédiés) ; récursivité (`rglob`) (rejeté : spec Out of Scope, assumption non récursif validée en spécification).

### D3 — Ordre et doublons

- **Decision** : ordre de traitement = ordre d'apparition des arguments ; au sein d'un dossier, tri alphabétique des noms. Un doublon (même fichier listé deux fois, ou listé et contenu dans un dossier) est traité à chaque occurrence, dans l'ordre ; les sorties sont désambiguïsées par le mécanisme de suffixe existant (`resoudre_chemin_nettoye`, `-1`, `-2` — jamais d'écrasement, FR-010).
- **Rationale** : déterminisme total (chaque choix est une fonction de l'entrée) ; le mécanisme anti-collision de 006 couvre déjà le cas sans nouveau code.
- **Alternatives considered** : déduplication silencieuse (rejeté : contredit le non-silence de SC-004 sans contrepoids, et le comportement « chaque occurrence traitée » est plus simple à spécifier et tester).

### D4 — Refactor de `cli.py` : résoudre le lot, puis traiter chaque document

- **Decision** : le corps de `main()` est réorganisé : (1) validations globales existantes (bornes `--extrait`, incompatibilité `--dry-run`+`--suggestion`) ; (2) résolution du lot via `resoudre_lot` ; (3) si le lot est vide → erreur d'entrée (code 1) ; (4) neutralisation conditionnelle des options non applicables (D6) ; (5) validation de `--echantillon` une seule fois (comportement actuel, erreur code 2 avant tout traitement de document) ; (6) boucle : pour chaque document, une fonction `_traiter_document(args, fichier) -> int` contenant le traitement actuel (segmentation, détection, suggestion par défaut, dossier de run, écritures, messages) inchangé au comportement près ; (7) agrégation des codes (D7).
- **Rationale** : chaque document emprunte le chemin existant → parité octet par octet garantie par construction (SC-002) ; la validation `--echantillon` reste un échec rapide global (Config Validation) et non par document, car l'échantillon est un paramètre de calibrage du lot entier.
- **Alternatives considered** : traiter l'échantillon par document (rejeté : sémantique de calibrage global, et le re-valider N fois est du bruit) ; extraire `_traiter_document` dans un module séparé (rejeté : déplacement gratuit, `cli.py` reste le point d'entrée naturel).

### D5 — Neutralisation conditionnelle : seuil « plus d'un document »

- **Decision** : `--dry-run` et `--suggestion` sont neutralisées (avec avertissement, D6) uniquement lorsque le lot résolu contient plus d'un document ; un lot d'un seul document — y compris issu d'un dossier — se comporte strictement comme l'invocation mono-document actuelle (dry-run et suggestion pleinement fonctionnels).
- **Rationale** : FR-005 exige un mono-document strictement identique ; la spec borne la neutralisation à « un lot » et l'US3 la motive par la suggestion « liée à un seul document » ; la frontière naturelle est la cardinalité du lot, pas la syntaxe de l'invocation.
- **Alternatives considered** : neutraliser dès qu'un dossier apparaît dans les arguments (rejeté : un dossier peut contenir un seul `.md`, et la règle serait non observable par l'utilisateur) ; refuser `--dry-run` même en mono-document issu de dossier (rejeté : rupture de FR-005).

### D6 — Avertissements de neutralisation : forme et moment

- **Decision** : avant la boucle de traitement, un avertissement par option neutralisée est écrit sur stderr, au format des avertissements existants : `AVERTISSEMENT : --dry-run ignorée en lot : applicable à un seul document` (et l'équivalent pour `--suggestion`). Les options neutralisées ne produisent aucun artefact de dry-run ; le lot est traité en nettoyage complet. L'incompatibilité `--dry-run`+`--suggestion` ensemble reste une erreur d'usage (code 3) avant résolution du lot, inchangée.
- **Rationale** : cohérence avec le canal des avertissements actuels (stderr, préfixe `AVERTISSEMENT :`, FR-016 de 001) ; non-silence exigé par SC-004 ; un avertissement unique par option suffit (le lot est homogène).
- **Alternatives considered** : refus bloquant code 3 (rejeté en clarification utilisateur du 2026-10-05 : avertissement + neutralisation choisis) ; avertissement par document (rejeté : bruit répétitif sans information nouvelle).

### D7 — Sémantique d'échec : poursuite, fail-fast au 3e échec consécutif, agrégation des codes

- **Decision** : chaque document en échec est signalé sur stderr (`ERREUR : <chemin> : <raison>`, à la place du message d'erreur actuel qui reste identique par document) ; le lot poursuit sur le document suivant ; un compteur d'échecs **consécutifs** est incrémenté à chaque échec et remis à zéro à chaque succès ; au troisième échec consécutif, le lot s'arrête immédiatement sans traiter les documents suivants. Code retour final : 0 si et seulement si tous les documents ont été traités avec succès, 1 sinon. Les sorties déjà produites sont conservées (aucune annulation). Le compteur porte sur les documents, indépendamment du nombre d'arguments.
- **Rationale** : arbitrages utilisateurs du 2026-10-05 (US4) ; les codes retour restent dans l'alphabet du contrat 001 (0/1/2/3) sans en créer de nouveau — un échec par document ne peut être qu'une erreur d'entrée (1) puisque la suggestion est neutralisée en lot et l'échantillon validé globalement (D4) ; l'arrêt aux 3 échecs consécutifs protège des lots majoritairement invalides sans coûter de contrat.
- **Alternatives considered** : fail-fast au premier échec (rejeté en clarification : poursuite demandée) ; code retour composite « succès partiel » (rejeté : hors périmètre de l'option A, glissement vers l'option B de l'assessment) ; continue-on-error illimité (rejeté : clarification utilisateur du 2026-10-05).

### D8 — Messages console : un flux par document, sans résumé de lot

- **Decision** : chaque document produit exactement les lignes actuelles (`Sortie : …`, `Sortie paginée : …`, `Cartographie : …`, avertissements sur stderr) ; aucun résumé de fin de lot n'est ajouté ; le code retour porte l'information d'échec global (D7) et chaque échec est individuellement tracé.
- **Rationale** : FR-011 et l'Out of Scope de l'option A (résumé = extension B) ; réduit la surface de contrat.
- **Alternatives considered** : ligne de résumé `N traités, K erreurs` (rejeté : reporté à l'extension B, aucun besoin observé).

### D9 — Révision du contrat CLI de la feature 001 et documentation

- **Decision** : la livraison modifie (1) `specs/001-nettoyage-md-repetitif/contracts/cli.md` — le point d'entrée devient multi-entrées, la table des options note `--dry-run`/`--suggestion` comme applicables à un lot d'un seul document, la section codes retour précise l'émission en lot ; (2) le README (nouvelle section « traiter plusieurs documents » avec les trois formes : fichiers listés, dossier, mélange, et l'avertissement sur les options neutralisées) ; (3) crée `specs/007-traitement-multi-documents/contracts/multi-entrees.md` comme contrat autoritaire du delta. La suite de tests existante doit passer sans relâchement (aucun contenu attendu des sorties individuelles ne change).
- **Rationale** : précédent 006 (D6 du plan 006 : contrat 001 et README révisés dans la même livraison) ; SC-002 et SC-005 exigent que rien d'observable ne change pour le mono-document.
- **Alternatives considered** : ne pas toucher au contrat 001 (rejeté : il deviendrait faux — FR-001 « un run = un fichier d'entrée » est révisé par la spec) ; tout déplacer dans le contrat 007 sans réviser 001 (rejeté : 001 est la référence citée partout, la divergence serait source d'erreurs).

## NEEDS CLARIFICATION résolus

Aucun marqueur restant : les trois arbitrages structurants (neutralisation avec avertissement, poursuite avec fail-fast au 3e échec consécutif, dossier sans `.md` ignoré avec message) ont été tranchés en clarification de la spécification le 2026-10-05 et sont intégrés à la spec et aux décisions ci-dessus.
