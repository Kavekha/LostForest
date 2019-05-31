NEXT:
    DONGEON:
        [ ] 100     Ajouter des fonctions get_entities_from_map? Pour meilleur accès aux infos dans la map pour game?
        [ ] 250     Tile personnalisée pour l'affichage : Char, couleurs selon la tile et non pas au niveau de la map.

    SAVES:
        10      save & load : config Appli.

    INTERFACE:
        250     box :       La rendre utilisable partout in game.
        50      box :       Faire en sorte que la BOX et le menu du fond ne se confondent pas.
        100     options:    Rendre generique le choix d une option parmi une liste de 26.
        250     menus :     Rendre les menus existants plus propres dans la circulation.

    CONTROLES:
        [/] 250     handle_keys : Meilleure gestion de la prise en compte des touches du joueur in game
        [ ] 250     handle keys : meilleure gestion des touches hors personnage : App & Menu.
        [ ] 100     Pouvoir utiliser espace pour Stairs.
        [ ] 100     Fixer la repetition de l'effet FullScreen et Exit notamment.
        [ ] 50      mouse : deplacements souris
        [ ] 100     Permettre de definir controles par le joueur.

    INVENTORY:
        100     use inventory : Nawak, tout se melange entre game pour l'usage, iventory pour le consume, etc.

    MAKE_MAP:
        100      tofix : Map peut être hors index, en tout cas sans bord pour bloquer le passage
                >(Genre : case non bloqué sur le bord : j'avance, crash car hors index).
                > Probablement du à l'effet sur les corridors de 1 tile supp de large

    LOOTS / MONSTRES:
        [ ] 250     Niveau de danger pour modifier un monstre de base selon le niveau du donjon.
        [ ] 250     Table de mobs / items : poids dependant du niveau de danger.
        [ ] 50      Nom de monstre vs nom de reference du monstre

    FIGHT:
        [/] 10      Si joueur meurt, les mobs jouent encore et un autre message de combat peut avoir lieu apres "you are dead"
        [ ] 100     Items de baston.
        [ ] 250     Mieux penser Might & Vitality pour que ca scale de facon moins radicale.

    CAMERA / RENDER:
        [ ] 100    map : camera, map plus grande que l'ecran de jeu
        [ ] 50     fix : mauvais recalcul du fov, laisse des traces de lumiere au debut
        [ ] 10     les stairs apparaissent une case dans le Fog du FOV. Les objets devoilés devraient aussi non?

    EVENTS:
        [ ] 25      logs : accès archives

    GAMEPLAY
        [/] 100     Tour par tour. Action determine si tour passe, ou non.
        [ ] 100     Beat : Tour = 5 beats. Beat Quick, Normal, NoSlow, Fast, Normal.
        [ ] 250     Equipement, items.
        [ ] 250     Monstres.

    LOCALIZATION
        250     Avoir un texte selon le choix de la langue. POC to do.
        100     Gerer l'utf8 ou en tout cas ne pas supprimer les mots avec accent. Libtcod ne semble pas suppoorter UTF8.

    REFACTOS
        [ ] 100     Entities & co : Pourquoi mettre Game dedans? Comment eviter ca?
        [ ] 50      S'assurer clareté de Render_all
        [/] 250     La prise en compte des actions du joueur se repartissent à trop d'endroits. Systeme Commands? POC.
        [ ] 10      Entity? On divise en LivingEntity et InanimateEntity? Bof.
        [ ] 100     C'est le bordel dans le main menu de l'App, dans les options & mess erreurs.
        [ ] 250     Inventory: use item : wrapper les fonctions effects par un item_use pour meilleur controle et garder les Effets plus neutres (utilisable par sort & etc).
        [ ] 50      render : solution degueu du reset game window pour artefacts map precedente.
        [ ] 100      Creer entité / item necessite game, map pour ajouter events, etc. Pas très autonome.
        [ ] 250     Systeme de game_state : Avec nouveau systeme de Round, plus très pertinent. A corriger.
        [ ] 100     Monstres vraiment concernés par systeme de Round?
        [ ] 50      map_is_in_fov testé dans enemy turn avant action et dans ai: take_turn. Doublon? Logique?
        [ ] 100     map.entities contient toutes les entités. Si on veut deplacer mob, on trouve des items. Si on veut recuperer des items, on passe par des entités.

    TO LEARN:
        Decorator pour entourer les fonctionnalités use_function des items. Le decorateur etait joué dés le main menu,
            et empechait la save du coup oO.