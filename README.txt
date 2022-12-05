Voila mon api terminé 
Elle montre le taux d'isolement (en pourcentage) de la population en corse 


voici comment l'utiliser:
    -la route "/status" permet de savoir si le serveur fonctionne ou pas

    -la route "/home" permet de voir l'état "normal", elle ouvre un nouvel onglet avec la heatMap et
     un petit text epxplicatif dans la page initial

    -la route "/coord/<lLat>/<lLong>/<hLat>/<hLong>" prend 4 parametre (2 coordonnés : latitude,longitude)
    et retourne quelques donnés sur la zone séléctionné et ouvre dans un autre onglet la heatMap du taux d'isolement
    de la zone. La première coordonné en parametre doit être "inférieur" à la deuxième dans sa position.
    Exemple : la route "/coord/0/0/50/50" est valide car la première coordonné (0,0) est strictement inférieur  à la seconde (50,50)
    Essayez les routes suivantes:
        - "/status"
        - "/home"
        - "coord/42.03152/8.884357/42.4713/9.297683"
    
Amusez-vous bien
