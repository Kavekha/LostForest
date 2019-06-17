NEXT:
    DONGEON:
        [ ] 250     Tile personnalisée pour l'affichage : Char, couleurs selon la tile et non pas au niveau de la map.
        [ ] 250     'Salles' avec evenements-types & variantes.
        [ ] 50      monster_table pas utilisé dans les specs des maps de donjon.
        [/] 250     Algorithme Brogue-like

    SAVES:
        [ ] 10      save & load : config Appli.

    INTERFACE:
        [ ] 250     Meilleure communication des actions possibles + boutons (ex: perso sur item : "(g) pick up {item}"
        [ ] 250     Afficher les objets et les personnages "en vue" avec description dans l'interface.
        [ ] 100     Afficher les caracts des items equipés.
        [ ] 100     Afficher les objets sous le personnage ou la target.
        [ ] 100     Les commandes necessaires devraient être indiquées (Exemple : "press g for pick up : item under me"

    TARGET SYSTEM:
        [/] 100     Autres critères de limitation : TILE only, TILE & ENTITY etc.
        [/] 100     Pouvoir transmettre les autres objets récupérés par la cible pour textes "flavor", ou refuser et envoyer paitre.
        [ ] 250     Radius & Direct effect, splash damage, join message pour une seule ligne avec plusieurs victimes. Damage to self message.

    CONTROLES:
        [ ] 50      mouse : deplacements souris
        [ ] 100     Permettre de definir controles par le joueur.

    MAP:
        [ ] 100     Rendre les salles moins carrés.
        [ ] 50      Animation au changement de map.
        [ ] 100     Garder la salle de transition d'une map à l'autre, illustre mieux le fait qu'on soit dans la meme foret.
        [ ] 250     Elements de map pouvant être detruits. Structure & resistance selon type Tuile. Attributs sur Tuile seulement une fois touché, sinon dans le type.

    LOOTS / MONSTRES:
        [ ] 250     Niveau de danger pour modifier un monstre de base selon le niveau du donjon.
        [ ] 250     Table de mobs / items : poids dependant du niveau de danger.
        [ ] 50      Nom de monstre vs nom de reference du monstre & idem pour items
        [ ] 50      Pack de monstres, thematique "monstre" de salles.
        [ ] 100     Items & monstres uniques, ou avec une limite, pour eviter trop grand nombre d'armes en doublon.
        [ ] 250     Creation d'items par morceaux selon region, chances de magique, budget magique a repartir, etc. affix / suffix and all that.
        [ ] 100     Creation de monstre par morceaux selon region, etc. cf.items?
        [ ] 100     Monstres par MonsterClass, autre organisation.
        [ ] 100     Avec DangerLevel, limite de mobs / salle & facon de spawner : Trop homogene, peu de surprises.
        [ ] 50      Limite dans les types d'objet ou de monstres pour assurer variété et eviter doublon.

    ITEMS :
        [ ] 50      Dropable : Graine, Piege
        [ ] 50      Readable : Scrolls, notes pour ambiance
        [ ] 50      Item : usage par defaut.
        [ ] 100     Message selon l'usage : '{} lance {}', '{} boit {}'
        [ ] 250     Pouvoir faire un usage creatif des autres modes. Actuellement : Potion tjrs drink. Concept unique de "use"
        [ ] 250     Items avec structure & resistance, pouvant être detruits.
        [ ] 50      Destruction de map.
        [ ] 50      Items correspondant aux nouveaux ciblages.
        [ ] 50      Usage par defaut des items.
        [ ] 100     Types d'items, regroupement par type et limite de type par map pour variété & eviter doublon.

    FIGHT:
        [ ] 250     Damage type : All reduced by Vitality. Acid, Fire, etc?

    CAMERA / RENDER:
        [ ] 100    map : camera, map plus grande que l'ecran de jeu
        [ ] 10     les stairs apparaissent une case dans le Fog du FOV. Et restent. Les objets devoilés devraient aussi non?

    EVENTS:
        [ ] 25      logs : accès archives

    GAMEPLAY
        [ ] 100     Beat : Tour = 5 beats. Beat Quick, Normal, NoSlow, Fast, Normal.
        [ ] 250     IA de pack de mobs, interaction entre eux et partage infos.
        [ ] 50      Reflechir : Game Master pour diriger IA, gerer l'ambiance, les loots, etc?
        [ ] 50      Reflechir : Foret & interaction avec elle.
        [ ] 250     Menu: Resumé de la partie perdue, score, game over, etc.
        [ ] 100     Monstres avec inventaire, peuvent utiliser des objets.
        [ ] 100     Fouiller l'inventaire d'un monstre mort.
        [ ] 100      Si monstres neutres ou amicaux, mode de combat : Attaquer, Parler, etc.
        [ ] 100     Potion acide devrait etre utilisable sur d'autres items.
        [ ] 250     Confirmation si action dangereuse que le joueur ne voudrait sans doute pas : Acide sur soit par exemple.

    LOCALIZATION
        [ ] 250     Avoir un texte selon le choix de la langue. POC to do.
        [ ] 100     Gerer l'utf8 ou en tout cas ne pas supprimer les mots avec accent. Libtcod ne semble pas suppoorter UTF8.

    IA / GAME MASTER
        [ ] 250     Remplacer le for entity in entities dans Game turn par une IA globale qui gère les actions des entités.
        [ ] 100     IA gère les entités via Commands. Dispose du systeme de Move astar etc.
        [ ] 100     Monstres non hostiles, monstres amicaux.

    ANIMATIONS
        [ ] 100     Animation via Event handler / Listener. Si animations en attente, le game turn les fait tourner avant de rendre la main.
        [ ] 100     Pouvoir interrompre l'animation ou l'acceler avec Escape.

    REFACTOS
        [ ] 100     Entities & co : Pourquoi mettre Game dedans? Comment eviter ca?
        [ ] 50      render : solution degueu du reset game window pour artefacts map precedente.
        [ ] 50      map_is_in_fov testé dans enemy turn avant action et dans ai: take_turn. Doublon? Logique?
        [ ] 100     map.entities contient toutes les entités. Si on veut deplacer mob, on trouve des items. Si on veut recuperer des items, on passe par des entités.
        [ ] 250     Clean des diverses actions sur application depuis des systemes plus bas dans la hierarchie, etc.
        [ ] 250     L'intelligence de ce qui doit s'afficher repose sur RenderEngine, ce devrait etre App & Game qui lui disent quoi afficher.
                        > Appli demande a Game ce qui doit etre affiché, puis demande a Render de le faire.
        [ ] 100     Faciliter l'ajout et la recuperation des monstres à creer. Numpy?
        [ ] 100     Menu : Si _options avec des entités, et pas de display_options avec texte : crash. Cf inventory.
        [ ] 100     Creation d'items vs data items.
        [ ] 50      Refacto Target : devrait etre associé au personnage? If link then command on linked entity?
        [ ] 100     Listener pour gerer les communications avec Game, App, etc. Remplacerait le Game dans Entité.
        [ ] 100     Refacto Target System. Pas souple du tout, specifique aux items.
        [ ] 100     Mieux utiliser les return True / False dans les fonctions, pour dire au moins "j'ai fais ce que tu m'a demandé"
        [ ] 50      Refacto effect functions / inventory / items : le message "{} thrown at {}" est dans effet. Devrait etre ailleurs.
        [ ] 100     Fonctions de combat hors Fighter : rends Fighter plus clean, permets de les utiliser sur les items et map.
        [/] 50      Spawners pour une meilleure reparition methode et plus de souplesse entre monstres & items.
        [/] 50      Constants / config pour Appli.
        [ ] 25      Requirements
        [/] 50      Readme
        [/] 100     savegame.bak grossit très vite. Semble faire ramer. Supprimer la save avant de la reecrire.
        [ ] 250     80x40 map = 3200 tiles. Faire une tuile de chaque etat et se referer à ces tuiles plutot. Defaut : une tuile pour toutes les cellules.
        [ ] 100     Spawner devrait recevoir un **parametre, et non pas elements par elements.

    TO LEARN:
        [ ]     Numpy pour creer des dictionnaires de monstres plus facilement.


    BUGS:
        [/] 250     Probleme de save + crash. Nouvelle partie. Je meurs. Je charge la save : je suis en vie avec 1 pv. Je me deplace. Crash. Perte de la save. Why?
        [ ] 100     Crash au reload d'une save apres victory screen. Plus de dungeon value.


    OBJECTIFS:

        # RELEASE 4 : Apparence de map, salles, items & monstres uniques.!

            [/] Ciblage amelioré, plus d'informations.
            [/] Meilleur systeme de spawn & valeurs d'items / monstres.
            [/] Nouvel algorithme de creation de map.
            [ ] Differentes couleurs de terrain sur la map, sans effet particulier.
            [ ] Salles-types :
                    Arbre Ancien, Arbre Mort,
                    Jardin naturel, jardin abandonné, Foret vivante,
                    Campement voyageur, ruines,
                    Preuves de souffrance.
            [ ] Items, mobs, etc.


        # RELEASE 5 :
            Lore, souffrances de la Foret, evenements associés.
            Textes d'ambiance, animations basiques.
            Vocabulaire : Stairs devient Borne Magique, disparition du concept de floor, etc.

        # RELEASE 6
            Score, multi-saves, nom du personnage.
            Interface, tutoriel ou meilleures indications.
            Equilibrage basique.
            Localisation
            Py2game.
            Refactos diverses.