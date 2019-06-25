NEXT:
    DONGEON:
        [ ] 250     Tile personnalisée pour l'affichage : Char, couleurs selon la tile et non pas au niveau de la map.
        [ ] 250     'Salles' avec evenements-types & variantes.
        [ ] 50      monster_table pas utilisé dans les specs des maps de donjon.

    SAVES:
        [ ] 10      save & load : config Appli.

    INTERFACE:
        [ ] 250     Meilleure communication des actions possibles + boutons (ex: perso sur item : "(g) pick up {item}"
        [ ] 250     Afficher les objets et les personnages "en vue" avec description dans l'interface.
        [ ] 100     Afficher les caracts des items equipés.
        [ ] 100     Afficher les objets sous le personnage ou la target.
        [ ] 100     Les commandes necessaires devraient être indiquées (Exemple : "press g for pick up : item under me"
        [ ] 250     Depuis Inventory : Je selectionne l'objet : fenetre avec actions Use, Drop, Equip, etc + description.

    TARGET SYSTEM:
        [ ] 250     Radius & Direct effect, splash damage, join message pour une seule ligne avec plusieurs victimes. Damage to self message.

    CONTROLES:
        [ ] 50      mouse : deplacements souris
        [ ] 100     Permettre de definir controles par le joueur.

    MAP:
        [ ] 100     Rendre les salles moins carrés.
        [ ] 50      Animation au changement de map.
        [ ] 100     Garder la salle de transition d'une map à l'autre, illustre mieux le fait qu'on soit dans la meme foret.
        [ ] 100     Elements de map pouvant être detruits. Structure & resistance selon type Tuile. Attributs sur Tuile seulement une fois touché, sinon dans le type.

    LOOTS / MONSTRES:
        [ ] ???     Niveau de danger pour modifier un monstre de base selon le niveau du donjon.
        [ ] ???     Table de mobs / items : poids dependant du niveau de danger.
        [ ] 50      Nom de monstre vs nom de reference du monstre & idem pour items
        [ ] 100     Pack de monstres, thematique "monstre" de salles.
        [ ] 100     Items & monstres uniques, ou avec une limite, pour eviter trop grand nombre d'armes en doublon.
        [ ] 250     Creation d'items par morceaux selon region, chances de magique, budget magique a repartir, etc. affix / suffix and all that.
        [ ] 100     Creation de monstre par morceaux selon region, etc. cf.items?
        [ ] 100     Monstres par MonsterClass, autre organisation.
        [ ] ???     Avec DangerLevel, limite de mobs / salle & facon de spawner : Trop homogene, peu de surprises.
        [ ] 50      Limite dans les types d'objet ou de monstres pour assurer variété et eviter doublon.
        [ ] 100     Lieux avec frequence dans les infos de mobs, pouvoir recuperer tous les mobs liés à une zone.
        [ ] 100     Monstres & items table generés automatiquement par Zone de Donjon & Tiers, sur la base d'informations dans les datas Monsters & Items.

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
        [ ] 50      Damage type : All reduced by Vitality. Acid, Fire, etc?
        [/] 500     Refaire le systeme de combat.

    CAMERA / RENDER:
        [ ] 100    map : camera, map plus grande que l'ecran de jeu
        [ ] 100     Les objets devoilés devraient restés affichés? Les monstres de meme? "Remanence" d'un etat. Connaissance du joueur.

    EVENTS:
        [ ] 25      logs : accès archives

    GAMEPLAY
        [ ] 100     Beat : Tour = 5 beats. Beat Quick, Normal, NoSlow, Fast, Normal.
        [ ] 250     IA de pack de mobs, interaction entre eux et partage infos.
        [ ] 50      Reflechir : Game Master pour diriger IA, gerer l'ambiance, les loots, etc?
        [ ] 50      Reflechir : Foret & interaction avec elle.
        [ ] 100     Menu: Resumé de la partie perdue, score, game over, etc.
        [ ] 100     Monstres avec inventaire, peuvent utiliser des objets, les recuperer ou meme les rattraper.
        [ ] 100     Fouiller l'inventaire d'un monstre mort.
        [ ] 100     Si monstres neutres ou amicaux, mode de combat : Attaquer, Parler, etc.
        [ ] 100     Potion acide devrait etre utilisable sur d'autres items.
        [ ] 250     Confirmation si action dangereuse que le joueur ne voudrait sans doute pas : Acide sur soit par exemple.

    LOCALIZATION
        [/] 250     Pouvoir choisir la langue du jeu.
        [ ] 100     Gerer l'utf8 ou en tout cas ne pas supprimer les mots avec accent. Libtcod ne semble pas suppoorter UTF8.
        [/] 250     Traduction dans les menus
        [ ] 250     Traduction des items et monstres.

    IA / GAME MASTER
        [ ] 250     Remplacer le for entity in entities dans Game turn par une IA globale qui gère les actions des entités.
        [ ] 100     IA gère les entités via Commands. Dispose du systeme de Move astar etc.
        [ ] 100     Monstres non hostiles, monstres amicaux.

    ANIMATIONS
        [ ] 100     Animation via Event handler / Listener. Si animations en attente, le game turn les fait tourner avant de rendre la main.
        [ ] 100     Pouvoir interrompre l'animation ou l'acceler avec Escape.

    REFACTOS
        # Construction
        [ ] 100     Entities & co : Pourquoi mettre Game dedans? Comment eviter ca?
        [ ] 100     map.entities contient toutes les entités. Si on veut deplacer mob, on trouve des items. Si on veut recuperer des items, on passe par des entités.
        [ ] 100     Clean des diverses actions sur application depuis des systemes plus bas dans la hierarchie, etc.
        [ ] 250     L'intelligence de ce qui doit s'afficher repose sur RenderEngine, ce devrait etre App & Game qui lui disent quoi afficher.
                        > Appli demande a Game ce qui doit etre affiché, puis demande a Render de le faire.
        [ ] 100     Faciliter l'ajout et la recuperation des monstres à creer. Numpy?
        [ ] 100     Creation d'items vs data items.
        [ ] 250     Listener pour gerer les communications avec Game, App, etc. L'intelligence de ce qui doit s'afficher repose sur RenderEngine.
        [ ] 100     Refacto Target System. Pas souple du tout, specifique aux items.
        [ ] 50      Refacto effect functions / inventory / items : le message "{} thrown at {}" est dans effet. Devrait etre ailleurs.
        [ ] 100     Fonctions de combat hors Fighter : rends Fighter plus clean, permets de les utiliser sur les items et map.
        [ ] 25      Requirements
        [ ] 100     Spawner devrait recevoir un **parametre, et non pas elements par elements.
        [ ] 50      Room devrait etre un vrai objet, et Rect juste un outil de creation.
        [ ] 100     Terrains & Tiles, devraient etre definis dans MapSpec et surtout mieux gerées.
        [ ] 50      Colors dans map spec & dans la tile de reference.
        [ ] 100     Gestion erreurs diverses. Notées en TODO.
        [ ] 500     Refacto : passer en Entité Composant System ECS
        [ ] 50      Rassembler les Enums au meme endroit.
        [ ] 250     Refacto menus : Retirer les doublements, les hacks, mieux gerer les textes.
        [ ] 250     Creation d'entités, gestion des erreurs pour eviter les crashs.
        [ ] 100     MonsterCompendium : eviter d'avoir du eval Libtcod.color. Cf gestion pour Brain, ou equivalent.
        [ ] 100     Compendium : Meilleure gestion des Brains, use_function, target type, etc. Dictionnaires relous à M.A.J.
        [ ] 100     Compendium : Json plus lisible sur la durée.

        # Dirty fixes
        [ ] 50      render : solution degueu du reset game window pour artefacts map precedente.

        # Questionnement
        [ ] 50      map_is_in_fov testé dans enemy turn avant action et dans ai: take_turn. Doublon? Logique?
        [ ] 50      Refacto Target : devrait etre associé au personnage? If link then command on linked entity?
        [ ] 50      Mieux utiliser les return True / False dans les fonctions, pour dire au moins "j'ai fais ce que tu m'a demandé"?

        # Bugs
        [ ] 100     Menu : Si _options avec des entités, et pas de display_options avec texte : crash. Cf inventory.
        [ ] 100     Crash au reload d'une save apres victory screen. Plus de dungeon value.
        [ ] 100     Retours à la ligne non pris en compte avec Texts.get_text
        [ ] 50      Message "Item equipé" si slot.NONE. Ne devrait pas etre possible.

        # POC
        [ ] 500     Passage / POC sur bearlib terminal.



    OBJECTIFS:

        # RELEASE 0.5 : Systeme de combat & Ergos
            [/] Systeme de combat mis à jour.
            [/] Nouvelle fiche de personnage.
            [/] Chargement des datas monstres via des CSV, plus faciles à mettre à jour.
            [/] Refacto creation entités monstres & player.
            [/] Table items : Par categorie, puis par items. Idem pour monstres.
            [/] Chargement des datas items via des CSV.
            [ ] Pluss d'infos sur les items dans les menus.
            [ ] Nouveau systeme d'inventaire : equipement, throw, drop, etc.
            [ ] Egos items, base.
            [ ] Monstres & items uniques : gestion.
            [ ] Spawning plus pertinent?

        # RELEASE 0.6 : Apparence.
            [ ] Images du jeu.
            [ ] Score
            [ ] multi-saves, nom du personnage.
            [ ] Interface, tutoriel ou meilleures indications?
            [ ] Py2game ou Nuitka (?) : exe pour windoz.

        # RELEASE 0.7 :
            [ ] Bearlib!

