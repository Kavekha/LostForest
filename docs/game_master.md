# CONCEPT
Une mecanique qui:
    - Regarde le niveau d'evenements interressants auquels le joueur a affaire.
    - Créé des situations interessantes quand le niveau est trop bas.

## RECUPERER LES EVENTS ET LEUR ATTRIBUER UNE VALEUR
Un certain nombre d'actions remonte un Event vers le Game Master.
Une valeur est attribuée par le game master à cet action.

### Exemples
Item pick up:
    Deja connu +1
    Jamais obtenu +5
    faible valeur +0
    moyenne valeur +1
    haute valeur +3
Rencontre avec un monstre
    Deja connu +3
    Jamais rencontré +15
    faible +0
    fort +5
    tres dangereux +10
    unique +25
Etc.

## ROLE DU GAME MASTER
Comme on a un niveau de situations interessantes, on peut en calculer la moyenne grace au nombre de tours.
Si la moyenne tombe en dessous d'un certain niveau, le game master essait de creer des situations interressantes.


### Exemples:
Faire deplacer des monstres existants vers un lieu proche du joueur.
Faire interagir entre eux des monstres a porté d'oreille du joueur.
Messages d'ambiance que le joueur n'a jamais eu.

Ces evenements sont eux memes remontés au Game MAster sous forme d'event, avec une valeur associée.
Cette valeur monte la moyenne jusqu'à un certain niveau :
    atteint la moyenne, mission accomplie.
    Non atteinte : mission a poursuivre.
Prevoir un cooldown entre deux interventions du Game Master pour eviter que ca parte en sucette.

