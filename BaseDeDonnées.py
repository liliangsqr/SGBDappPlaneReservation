from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime,DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
import sqlalchemy
import datetime
import _mysql_connector
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import random

# Déclaration de la base de données
Base = declarative_base()


# Modèle de la table Utilisateur
class Utilisateur(Base):
    __tablename__ = 'utilisateurs'

    id = Column(Integer, primary_key=True)
    nom = Column(String(50), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    mot_de_passe = Column(String(50), nullable=False)
    reservations = relationship('Reservation', back_populates='utilisateur')


# Modèle de la table Vol
class Vol(Base):
    __tablename__ = 'vols'

    id = Column(Integer, primary_key=True)
    numero_vol = Column(String(50), nullable=False)
    depart = Column(String(50), nullable=False)
    arrivee = Column(String(50), nullable=False)
    prix = Column(Integer, nullable=False)
    prestataire = Column(String(50), nullable=False)
    date = Column(DateTime, nullable=False)  # Nouvelle colonne pour la date du vol
    reservations = relationship('Reservation', back_populates='vol')


# Modèle de la table Reservation
class Reservation(Base):
    __tablename__ = 'reservations'

    id = Column(Integer, primary_key=True)
    utilisateur_id = Column(Integer, ForeignKey('utilisateurs.id'), nullable=False)
    vol_id = Column(Integer, ForeignKey('vols.id'), nullable=False)
    date_reservation = Column(DateTime)
    utilisateur = relationship('Utilisateur', back_populates='reservations')
    vol = relationship('Vol', back_populates='reservations')


# Configuration de la base de données
engine = create_engine('mysql://user:user@localhost/tp4_sgbd')
Base.metadata.create_all(engine)

# Création d'une session pour interagir avec la base de données
Session = sessionmaker(bind=engine)
session = Session()

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
#     vol = Vol(
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
