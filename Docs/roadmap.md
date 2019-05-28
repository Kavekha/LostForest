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
        [ ] 250     handle_keys : Meilleure gestion de la prise en compte des touches du joueur et des actions selon state.
        [ ] 100     Pouvoir utiliser espace pour Stairs.
        [ ] 100     Fixer la repetition de l'effet FullScreen et Exit notamment.
        [ ] 50      mouse : deplacements souris
        [ ] 100     player_turn : get_action dans event handlers?

    INVENTORY:
        100     use inventory : Nawak, tout se melange entre game pour l'usage, iventory pour le consume, etc.

    MAKE_MAP:
        100      tofix : Map peut être hors index, en tout cas sans bord pour bloquer le passage
                >(Genre : case non bloqué sur le bord : j'avance, crash car hors index).
                > Probablement du à l'effet sur les corridors de 1 tile supp de large

    LOOTS / MONSTRES:
        [/] 100     Meilleure structure mobs & items : item de reference, item adapté (on ne prends que ce qui change)
        [ ] 250     Niveau de danger pour modifier un monstre de base selon le niveau du donjon.
        [ ] 250     Table de mobs / items : poids dependant du niveau de danger.
        [/] 100     Creation de monstres & items ailleurs que dans Spawner non?
        [ ] 50      Nom de monstre vs nom de reference du monstre

    FIGHT:
        [/] 100     fight : stats & combat
        [ ] 10      Si joueur meurt, les mobs jouent encore et un autre message de combat peut avoir lieu apres "you are dead"
        [ ] 250     Items de baston.
        [ ] 250     Mieux penser Might & Vitality pour que ca scale de facon moins radicale.

    CAMERA / RENDER:
        [ ] 250     map : camera, map plus grande que l'ecran de jeu
        [ ] 50     fix : mauvais recalcul du fov, laisse des traces de lumiere au debut
        [ ] 50      les stairs apparaissent une case dans le Fog du FOV.

    EVENTS:
        [ ] 25      logs : accès archives

    GAMEPLAY
        50      Tour par Tour? Timeline? Heartbeats
        250     Equipement, items.
        250     Monstres.

    REFACTOS
        [ ] 100     Entities & co : Pourquoi mettre Game dedans? Comment eviter ca?
        [ ] 50      S'assurer clareté de Render_all
        [ ] 250     La prise en compte des actions du joueur se repartissent à trop d'endroits. Systeme Commands? POC.
        [ ] 10      Entity? On divise en LivingEntity et InanimateEntity? Bof.
        [ ] 100     C'est le bordel dans le main menu de l'App, dans les options & mess erreurs.
        [/] 250     Format des datas pour monsters & items compendiums...
        [ ] 250     Inventory: use item : wrapper les fonctions effects par un item_use pour meilleur controle et garder les Effets plus neutres (utilisable par sort & etc).
        [ ] 50      render : solution degueu du reset game window pour artefacts map precedente.
        [ ] 100      Creer entité / item necessite game, map pour ajouter events, etc. Pas très autonome.

    TO LEARN:
        Decorator pour entourer les fonctionnalités use_function des items. Le decorateur etait joué dés le main menu,
            et empechait la save du coup oO.