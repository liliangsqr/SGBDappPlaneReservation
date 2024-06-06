# Projet sgbd avec python python
********************
* Petit projet à encore pauffiner surtout au niveau de la sécurité des données
* Factorisation possiblement envisageables
* une variable global à résoudre 
* Tkinter qui fait tout disparaitre si un bouton a une fonction prenant des paramètres
* *****************

#	Fonctionnement du logiciel

Le logiciel fonctionne avec une connexion via Apache sur une base de données MySQL que nous gérons dans le code avec SQLAlchemy ORM. Dans notre programme nous pouvons rassembler les fonctions en plusieurs familles. Nous avons les fonctions d’initialisation des objets que nous utilisons et qui représentent les différents onglets/fenêtres, ensuite nous avons les fonctions d’affichage de ces objets et pour finir nous avons les fonctions qui chargent l’affichage des tables et celles qui gèrent les interactions avec la base de données.

Lorsqu’on lance le programme, on arrive sur une page qui nous affiche les vols enregistrés dans la base de données ainsi que plusieurs informations comme la date du vol, la compagnie etc. Cependant pour pouvoir faire des réservations nous avons besoins d’avoir un compte client. Sur cette page nous avons, en plus, des zones pour se connecter et s’enregistrer. Pour vérifier la connexion nous appelons des fonctions qui interagissent avec la base de données et regardent s’il existe un utilisateur avec un mail et un mot de passe correspondant à celui renseigné, si ce n’est pas le cas alors la personne est invitée à réessayer dans le cas où elle s’est trompée ou de se créer un compte via le champ d’enregistrement. Si la personne se crée un compte alors on ajoute les données de cette personne dans la base de données.
 
Une fois connecté nous désaffichons la page précédente et en affichons une nouvelle sur la même fenêtre pour faire l’illusion d’un changement de pages. Sur cette nouvelle page on retrouve une liste consultable des vols possibles ainsi qu’une section pour voir les réservations effectuées par l’utilisateur connecté. Ils possèdent également des boutons notamment pour faire une réservation, pour supprimer une réservation et pour se déconnecter. Ce sont les seules actions que l’utilisateur connecté peut faire. Nous faisons l’association dans la base de données avec l’identifiant de l’utilisateur connecté et l’identifiant du vol. Pour faire une nouvelle réservation, l’utilisateur sera invité à écrire seulement l’identifiant du vol souhaité, son identifiant à lui est directement récupéré et associé au vol renseigné. Cela évite qu’un client puisse réserver avec l’identité d’un autre client.
 
Notre application permet aussi à un administrateur de pouvoir se connecter et de bénéficier d’accès spéciaux sur j’ajout et la suppression d’utilisateurs, de vols et de réservations présentes dans la base de données. L’administrateur un contrôle total permettant une bonne gestion de la plateforme. Contrairement à l’utilisateur, l’administrateur aura plus de champs à remplir dans la réservation, il devra renseigner manuellement l’identifiant de la personne à laquelle il ajouter une réservation en plus de l’identifiant du vol.
	
Pour Résumer nous avons fait un logiciel avec une interface et des fonctionnalités qui changent en fonction de la personne qui se connecte en comparant dans la base de données, si la personne qui se connecte a les identifiants d’un Administrateur ou non. En fonction de ces identifiants les possibilités d’actions changent. 


