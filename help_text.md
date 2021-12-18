Les commandes existantes sont:
  `$help`
Affiche ce texte.

  `$ping`
  Affiche le temps de réponse du bot, et permet de vérifier qu'il est en ligne.

  `$next [groupe] [n]`
Affiche le n-prochain cours du groupe choisi, avec ces infos correspondantes.
Pour afficher le prochain cours du groupe IN301A3 il suffit de faire `$next INF3 1`, pour afficher celui qui suit `$next INF3 2`, etc. Par defaut n est 1, donc `$next MI2 1` peut s'ecrire `$next MI2`. Le groupe peut etre indiqué comme ça `INF5`, ou comme ça `MA`, pour se referer au groupe INF401A5, ou à la série MA401 respectivement. Les noms des séries sont MA, IGM, MI, et INF.
En plus, 15 minutes avant chaque cours, Notifications EDT envoi un message avec les infos du cours, comme `$next`, et il mentionne les personnes concernées.

  `$groupe [groupe]`
Attribue le rôle [groupe]. Par exemple `$groupe INF4` attribue le rôle INF4 correspondant au groupe INF401A4.

  `$donate`
Donne des informations sur comment faire une donation.
