Les commandes existantes sont:
  `$help`
Affiche ce texte.

  `$ping`
  Affiche le temps de réponse du bot, et permet de vérifier qu'il est en ligne.

  `$next [groupe] [n]`
Affiche le n-prochain cours du groupe choisi, avec ces infos correspondantes.
Pour afficher le prochain cours du groupe IN301A3 il suffit de faire `$next IN3 1`, pour afficher celui qui suit `$next IN3 2`, etc. Par defaut n est 1, donc `$next MI2 1` peut s'ecrire `$next MI2`. Le groupe peut etre indiqué comme ça `IN5`, ou comme ça `MA`, pour se referer au groupe IN301A5, ou à la série MA301 respectivement. Les noms des séries sont MA, MI, et IN.
En plus, 15 minutes avant chaque cours, Notifications EDT envoi un message avec les infos du cours, comme `$next`, et il mentionne les personnes concernées.

  `$groupe [groupe]`
Attribue le rôle [groupe]. Par exemple `$groupe IN4` attribue le rôle IN4 correspondant au groupe IN301A4.

  `$donate`
Donne des informations sur comment faire une donation.
