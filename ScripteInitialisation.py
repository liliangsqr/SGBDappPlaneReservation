
# # Ajout de 10 utilisateurs avec des noms et emails créatifs
# utilisateurs = []
# noms_utilisateurs = [
#     'Alice Wonder', 'Bob Builder', 'Charlie Chaplin', 'Diana Prince', 'Evan Almighty',
#     'Fiona Shrek', 'George Jetson', 'Holly Golightly', 'Igor Frankenstein', 'Jack Sparrow'
# ]
#
# for i, nom in enumerate(noms_utilisateurs):
#     utilisateur = Utilisateur(
#         nom=nom,
#         email=f'{nom.lower().replace(" ", ".")}@example.com',
#         mot_de_passe='password'
#     )
#     utilisateurs.append(utilisateur)
#     session.add(utilisateur)
#
# session.commit()
#
# # Ajout de 10 vols avec des noms de vols et prestataires créatifs
# vols = []
# noms_vols = [
#     'Flight of the Phoenix', 'Skyward Bound', 'Sunset Soarer', 'Dawn Patrol', 'Midnight Express',
#     'Cloud Nine', 'Eagle Eye', 'Star Gazer', 'Dreamliner', 'Comet Chaser'
# ]
# villes_depart = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose']
# villes_arrivee = ['Miami', 'Orlando', 'Seattle', 'Denver', 'Las Vegas', 'Atlanta', 'Boston', 'Detroit', 'San Francisco', 'Charlotte']
# prestataires = ['SkyHigh Airlines', 'DreamFlights', 'Sunshine Airways', 'Moonlight Travels', 'Starlight Air', 'EagleWings', 'CloudHopper', 'JetSet', 'AirLux', 'FlyAway']
#
# for i in range(10):
#     vol = Vols(
#         numero_vol=noms_vols[i],
#         depart=villes_depart[i],
#         arrivee=villes_arrivee[i],
#         prix=random.randint(100, 1000),
#         prestataire=prestataires[i],
#         date=datetime.now() + timedelta(days=i)
#     )
#     vols.append(vol)
#     session.add(vol)
#
# session.commit()
#
# # Ajout de 15 réservations en associant de manière aléatoire des utilisateurs aux vols
# for i in range(15):
#     reservation = Reservation(
#         utilisateur_id=random.choice(utilisateurs).id,
#         vol_id=random.choice(vols).id,
#         date_reservation=datetime.now()
#     )
#     session.add(reservation)
#
# session.commit()
#
# # Fermeture de la session
# session.close()
#
# print("Ajout des utilisateurs, vols et réservations terminé.")