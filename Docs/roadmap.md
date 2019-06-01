NEXT:
    DONGEON:
        [ ] 100     Ajouter des fonctions get_entities_from_map? Pour meilleur accès aux infos dans la map pour game?
        [ ] 250     Tile personnalisée pour l'affichage : Char, couleurs selon la tile et non pas au niveau de la map.
        [ ] 250     'Salles' avec evenements-types & variantes.
        [ ] 50      monster_table pas utilisé dans les specs des maps de donjon.

    SAVES:
        [ ] 10      save & load : config Appli.
        [/] 100     fix : Si reload de save, plus de menu possible car faisant reference à une App qui n existe plus.

    INTERFACE:
        [ ] 250     Meilleure communication des actions possibles + boutons (ex: perso sur item : "(g) pick up {item}"
        [ ] 250     Afficher les objets et les personnages "en vue" avec description dans l'interface.

    CONTROLES:
        [ ] 10     Pouvoir utiliser espace pour Stairs.
        [ ] 50      mouse : deplacements souris
        [ ] 100     Permettre de definir controles par le joueur.

    INVENTORY:
        [ ] 100     use inventory : Nawak, tout se melange entre game pour l'usage, iventory pour le consume, etc.

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
        [ ] 50      Nom de monstre vs nom de reference du monstre
        [ ] 50      Pack de monstres, thematique "monstre" de salles.

    FIGHT:
        [ ] 100     Items de baston.
        [/] 250     Mieux penser Might & Vitality pour que ca scale de facon moins radicale.

    CAMERA / RENDER:
        [ ] 100    map : camera, map plus grande que l'ecran de jeu
        [/] 50     fix : mauvais recalcul du fov, laisse des traces de lumiere au debut
        [ ] 10     les stairs apparaissent une case dans le Fog du FOV. Et restent. Les objets devoilés devraient aussi non?

    EVENTS:
        [ ] 25      logs : accès archives

    GAMEPLAY
        [/] 250     Leveling, gain d'xp, distribution de stats.
        [ ] 100     Beat : Tour = 5 beats. Beat Quick, Normal, NoSlow, Fast, Normal.
        [ ] 250     Equipement, items.
        [/] 100     Monstres, variété basique.
        [ ] 250     Throw, drop, Equip
        [ ] 250     IA de pack de mobs, interaction entre eux et partage infos.
        [ ] 50      Reflechir : Game Master pour diriger IA, gerer l'ambiance, les loots, etc?
        [ ] 50      Reflechir : Foret & interaction avec elle.

    LOCALIZATION
        [ ] 250     Avoir un texte selon le choix de la langue. POC to do.
        [ ] 100     Gerer l'utf8 ou en tout cas ne pas supprimer les mots avec accent. Libtcod ne semble pas suppoorter UTF8.

    REFACTOS
        [ ] 100     Entities & co : Pourquoi mettre Game dedans? Comment eviter ca?
        [ ] 250     Inventory: use item : wrapper les fonctions effects par un item_use pour meilleur controle et garder les Effets plus neutres (utilisable par sort & etc).
        [ ] 50      render : solution degueu du reset game window pour artefacts map precedente.
        [ ] 100     Creer entité / item necessite game, map pour ajouter events, etc. Pas très autonome.
        [ ] 250     Systeme de game_state : Avec nouveau systeme de Round, plus très pertinent. A corriger.
        [ ] 100     Monstres vraiment concernés par systeme de Round?
        [ ] 50      map_is_in_fov testé dans enemy turn avant action et dans ai: take_turn. Doublon? Logique?
        [ ] 100     map.entities contient toutes les entités. Si on veut deplacer mob, on trouve des items. Si on veut recuperer des items, on passe par des entités.
        [ ] 250     Clean de systeme de State, diverses actions sur application depuis des systemes plus bas dans la hierarchie, etc.
        [ ] 100     L'intelligence de ce qui doit s'afficher repose sur RenderEngine, ce devrait etre App & Game qui lui disent quoi afficher.
        [ ] 25      Etat de la victoire : On revient dans le jeu en quittant le menu? Autre chose?
        [/] 50     App est utilisé pour plein de choses, notamment menu. Du coup sauvegarde niqué, car elle sauvegarde au niveau du jeu. Ne plus referencer App.
        [ ] 100     Faciliter l'ajout et la recuperation des monstres à creer. Numpy?

    TO LEARN:
        [ ]     Decorator pour entourer les fonctionnalités use_function des items. Le decorateur etait joué dés le main menu,
                    et empechait la save du coup oO.
        [ ]     Numpy pour creer des dictionnaires de monstres plus facilement.


    OBJECTIFS:

    # RELEASE 2 : Victory screen, quelques monstres, menus OK, fiche de personnage.
        [/] Refacto controllers.
        [/] Menus & victory screen.
        [/] Combat & stats, leveling du joueur
        [/] variétés de monstres basiques.

    # RELEASE 3 : Equipement, items basiques, niveau de danger pour monstres & items.

    # RELEASE 4 : Maps & generation, salles speciales, meilleures tables de mobs.