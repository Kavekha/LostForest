# Stats

HP      :   Points de vie.
Might   :   Puissance des dommages. Limite la puissance des coups si trop faible, augmente les dommages si trop fort.
Vitality :  Reduit les dmg subits. Si dommages trop faibles, ils sont réduits. Si trop forts, ils sont augmentés.

# Combat flow

Si les deux entités ont un component Fighter & block True, le combat a lieu à l'interaction.
Attaquant .attack pour X damage (Base dmg * Might).
Defenseur .get hit. Il modifie les dmg et retourne leur nouvelle valeur.
Defenseur .take_damage. Verifie si le defenseur meurt.
Attaquant .kill si Defenseur meurt.
Defenseur .on_death si Defenseur meurt.


# Damage formula

Si damage superieur à Might, limité à might.
Si damage inferieur à Might x 2, damage doublés.
Sinon, damage de base.
i.e :
J'ai Might 5. J'utilise une arme 2-4. Je fais 2. J'inflige 4 dmg. Vrais Dmg : 4, 3, 4.
J'ai Might 5. J'utilise une arme 3-5. Je fais 3. J'inflige 3 dmg. Vrais dmg : 3, 4, 5.
J'ai Might 1. J'utilise une arme 2-4. Je fais 2. J'inflige 1 dmg. Vrais dmg : 1, 1, 1.

