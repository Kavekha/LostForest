NEXT:
    DONGEON:
        [ ] 100     Ajouter des fonctions get_entities_from_map? Pour meilleur accès aux infos dans la map pour game?
        [ ] 250     Tile personnalisée pour l'affichage : Char, couleurs selon la tile et non pas au niveau de la map.
        [ ] 250     'Salles' avec evenements-types & variantes.
        [ ] 50      monster_table pas utilisé dans les specs des maps de donjon.

    SAVES:
        [ ] 10      save & load : config Appli.

    INTERFACE:
        [ ] 250     Meilleure communication des actions possibles + boutons (ex: perso sur item : "(g) pick up {item}"
        [ ] 250     Afficher les objets et les personnages "en vue" avec description dans l'interface.
        [/] 100     Afficher items equipés dans menu Inventaire & Character?
        [ ] 100     Afficher les caracts des items equipés.
        [ ] 100     Afficher les objets sous le personnage ou la target.

    TARGET SYSTEM:
        [/] 100     Differents critères de limitation de l entité Target, selon type : FIGHTER, ITEM, SELF.
        [ ] 100     Autres critères de limitation : TILE only, TILE & ENTITY etc.

    CONTROLES:
        [/] 10      Pouvoir utiliser espace.
        [ ] 50      mouse : deplacements souris
        [ ] 100     Permettre de definir controles par le joueur.
        [ ] 100     FIX: Quand inventaire reclamé via 'i', le menu est aussitot activé avec la touche 'i'. Idem Char screen, etc.

    INVENTORY:
        [/] 100     use inventory : Nawak, tout se melange entre game pour l'usage, iventory pour le consume, etc.

    MAKE_MAP:
        [ ] 100    tofix : Map peut être hors index, en tout cas sans bord pour bloquer le passage
                      >(Genre : case non bloqué sur le bord : j'avance, crash car hors index).
                      > Probablement du à l'effet sur les corridors de 1 tile supp de large
        [ ] 100    Rendre les salles moins carrés.
        [ ] 50     Animation au changement de map.
        [ ]100     Garder la salle de transition d'une map à l'autre, illustre mieux le fait qu'on soit dans la meme foret.

    LOOTS / MONSTRES:
        [ ] 250     Niveau de danger pour modifier un monstre de base selon le niveau du donjon.
        [ ] 250     Table de mobs / items : poids dependant du niveau de danger.
        [ ] 50      Nom de monstre vs nom de reference du monstre & idem pour items
        [ ] 50      Pack de monstres, thematique "monstre" de salles.
        [ ] 100     Items & monstres uniques, ou avec une limite, pour eviter trop grand nombre d'armes en doublon.
        [ ] 250     Creation d'items par morceaux selon region, chances de magique, budget magique a repartir, etc. affix / suffix and all that.
        [ ] 100     Creation de monstre par morceaux selon region, etc. cf.items?

    ITEMS :
        [/] 50      Drinkable : Potions
        [/] 50      Throwable : Acide,
        [ ] 50      Dropable : Graine, Piege
        [ ] 50      Readable : Scrolls
        [ ] 100     Message selon l'usage : '{} lance {}', '{} boit {}'
        [ ] 250     Pouvoir faire un usage creatif des autres modes. Actuellement : Potion tjrs drink. Concept unique de "use"

    FIGHT:
        [/] 100     Items basiques de baston.
        [ ] 250     Damage type : All reduced by Vitality. Acid, Fire, etc?

    CAMERA / RENDER:
        [ ] 100    map : camera, map plus grande que l'ecran de jeu
        [ ] 10     les stairs apparaissent une case dans le Fog du FOV. Et restent. Les objets devoilés devraient aussi non?

    EVENTS:
        [ ] 25      logs : accès archives

    GAMEPLAY
        [ ] 100     Beat : Tour = 5 beats. Beat Quick, Normal, NoSlow, Fast, Normal.
        [/] 250     Equipement, items
        [/] 250     Throw, drop, Equip - basique
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
        [/] 100     Inventory: use item : wrapper les fonctions effects par un item_use pour meilleur controle et garder les Effets plus neutres (utilisable par sort & etc).
        [ ] 50      render : solution degueu du reset game window pour artefacts map precedente.
        [ ] 50      map_is_in_fov testé dans enemy turn avant action et dans ai: take_turn. Doublon? Logique?
        [ ] 100     map.entities contient toutes les entités. Si on veut deplacer mob, on trouve des items. Si on veut recuperer des items, on passe par des entités.
        [/] 100     Clean de systeme de State
        [ ] 250     Clean des diverses actions sur application depuis des systemes plus bas dans la hierarchie, etc.
        [ ] 100     L'intelligence de ce qui doit s'afficher repose sur RenderEngine, ce devrait etre App & Game qui lui disent quoi afficher.
        [ ] 100     Faciliter l'ajout et la recuperation des monstres à creer. Numpy?
        [ ] 100     Menu : Si _options avec des entités, et pas de display_options avec texte : crash. Cf inventory.
        [ ] 100     Creation d'items vs data items.
        [ ] 50      Refacto Target : devrait etre associé au personnage? If link then command on linked entity?
        [ ] 100     Listener pour gerer les communications avec Game, App, etc. Remplacerait le Game dans Entité.
        [ ] 100     Refacto Target System. Pas souple du tout, specifique aux items.
        [ ] 100     Mieux utiliser les return True / False dans les fonctions, pour dire au moins "j'ai fais ce que tu m'a demandé"
        [ ] 50      Refacto effect functions / inventory / items : le message "{} thrown at {}" est dans effet. Devrait etre ailleurs.
        [/] 50      Target Self devrait être dans le systeme de targeting, pas inventory.

    TO LEARN:
        [ ]     Decorator pour entourer les fonctionnalités use_function des items. Le decorateur etait joué dés le main menu,
                    et empechait la save du coup oO.
        [ ]     Numpy pour creer des dictionnaires de monstres plus facilement.


    OBJECTIFS:

        # RELEASE 3 : Equipement, items basiques, repartition des monstres & items dans la map selon Facteur Danger.
            [/] Refacto, clean up.
            [/] Items basiques supplementaires.
            [/] Equiper et déséquiper des armes.
            [/] DropMenu
            [/] Systeme de ciblage pour usage des items.
            [/] Actions automatiques : Throw, Drink, Equip
            [ ] Repartition des monstres dans une map sur une base de Facteur Danger.
            [ ] Repartition des items dans une map sur une base Facteur Valeur.
            [ ] Limite dans les types d'objet ou de monstres pour assurer variété et eviter doublon.

        # RELEASE 4 : Maps & generation, salles speciales, meilleures tables de mobs.