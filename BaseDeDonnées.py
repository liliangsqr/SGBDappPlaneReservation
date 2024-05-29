from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime,DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
import sqlalchemy
import _mysql_connector
from sqlalchemy.orm.exc import NoResultFound

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
