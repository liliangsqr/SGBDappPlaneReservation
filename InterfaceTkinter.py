import tkinter
import tkinter as tk
from tkinter import messagebox, ttk
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from BaseDeDonnées import Base, Utilisateur, Vol, Reservation  # Assume models.py contains the SQLAlchemy models and engine setup

# Configuration de la base de données
engine = create_engine('mysql://user:user@localhost/tp4_sgbd')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

class DatabaseManager:
    @staticmethod
    def ajouter_utilisateur(nom, email, mot_de_passe):
        if nom and email and mot_de_passe:
            try:
                utilisateur = Utilisateur(nom=nom, email=email, mot_de_passe=mot_de_passe)
                session.add(utilisateur)
                session.commit()
                return "Utilisateur ajouté avec succès"
            except Exception as e:
                session.rollback()
                return f"Erreur lors de l'ajout de l'utilisateur : {e}"
        else:
            return "Tous les champs sont obligatoires"

    @staticmethod
    def ajouter_vol(numero_vol, depart, arrivee, prix, presta):
        if numero_vol and depart and arrivee and prix and presta:
            try:
                vol = Vol(numero_vol=numero_vol, depart=depart, arrivee=arrivee, prix=int(prix),
                          prestataire=presta)
                session.add(vol)
                session.commit()
                return "Vol ajouté avec succès"
            except Exception as e:
                session.rollback()
                return f"Erreur lors de l'ajout du vol : {e}"
        else:
            return "Tous les champs sont obligatoires"

    @staticmethod
    def faire_reservation(utilisateur_id, vol_id):
        if utilisateur_id and vol_id:
            try:
                date_reservation = datetime.now()
                reservation = Reservation(utilisateur_id=int(utilisateur_id), vol_id=int(vol_id),
                                          date_reservation=date_reservation)
                session.add(reservation)
                session.commit()
                return "Réservation effectuée avec succès"
            except Exception as e:
                session.rollback()
                return f"Erreur lors de la réservation : {e}"
        else:
            return "Tous les champs sont obligatoires"

    @staticmethod
    def get_utilisateurs():
        return session.query(Utilisateur).all()

    @staticmethod
    def get_vols():
        return session.query(Vol).all()

    @staticmethod
    def get_reservations():
        return session.query(Reservation).all()

    @staticmethod
    def supprimer_vol(vol_id):
        try:
            vol = session.query(Vol).filter_by(id=vol_id).first()
            if vol:
                session.delete(vol)
                session.commit()
                return "Vol supprimé avec succès"
            else:
                return "Vol non trouvé"
        except Exception as e:
            session.rollback()
            return f"Erreur lors de la suppression du vol : {e}"

    @staticmethod
    def annuler_reservation(reservation_id):
        try:
            reservation = session.query(Reservation).filter_by(id=reservation_id).first()
            if reservation:
                session.delete(reservation)
                session.commit()
                return "Réservation annulée avec succès"
            else:
                return "Réservation non trouvée"
        except Exception as e:
            session.rollback()
            return f"Erreur lors de l'annulation de la réservation : {e}"

    @staticmethod
    def supprimer_utilisateur(utilisateur_id):
        try:
            utilisateur = session.query(Utilisateur).filter_by(id=utilisateur_id).first()
            if utilisateur:
                session.delete(utilisateur)
                session.commit()
                return "Utilisateur supprimé avec succès"
            else:
                return "Utilisateur non trouvé"
        except Exception as e:
            session.rollback()
            return f"Erreur lors de la suppression de l'utilisateur : {e}"

class GestionReservationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion de Réservations")
        self.create_menu()
        self.create_widgets()


    def status_boutons(self,bouton,utilisateur_id):
        if utilisateur_id != 15:
            bouton.config(state=tkinter.DISABLED)

    def create_menu(self):
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)
        self.menu_ajouter = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_supprimer = tk.Menu(self.menu_bar, tearoff=0)


    def create_widgets(self):
        # Création de la page de connexion
        self.frame_connexion = tk.Frame(self.root)
        self.frame_connexion.pack(pady=10)
        tk.Label(self.frame_connexion, text="Email").grid(row=0, column=0)
        self.entry_email_connexion = tk.Entry(self.frame_connexion)
        self.entry_email_connexion.grid(row=0, column=1)
        tk.Label(self.frame_connexion, text="Mot de passe").grid(row=1, column=0)
        self.entry_mdp_connexion = tk.Entry(self.frame_connexion, show="*")
        self.entry_mdp_connexion.grid(row=1, column=1)
        self.btn_connexion = tk.Button(self.frame_connexion, text="Connexion", command=self.connexion)
        self.btn_connexion.grid(row=2, columnspan=2)

        # Création de la page d'inscription
        self.frame_inscription = tk.Frame(self.root)
        self.frame_inscription.pack(pady=10)
        tk.Label(self.frame_inscription, text="Nom").grid(row=0, column=0)
        self.entry_nom_inscription = tk.Entry(self.frame_inscription)
        self.entry_nom_inscription.grid(row=0, column=1)
        tk.Label(self.frame_inscription, text="Email").grid(row=1, column=0)
        self.entry_email_inscription = tk.Entry(self.frame_inscription)
        self.entry_email_inscription.grid(row=1, column=1)
        tk.Label(self.frame_inscription, text="Mot de passe").grid(row=2, column=0)
        self.entry_mdp_inscription = tk.Entry(self.frame_inscription, show="*")
        self.entry_mdp_inscription.grid(row=2, column=1)
        self.btn_inscription = tk.Button(self.frame_inscription, text="Inscription", command=self.inscription)
        self.btn_inscription.grid(row=3, columnspan=2)

        #creation table acceuil ou on visualise les vols
        self.frame_tables = tk.Frame(self.root)
        self.frame_tables.pack(pady=10)
        self.tab_control = ttk.Notebook(self.frame_tables)
        self.tab_control.pack(expand=1, fill="both")
        self.tab_vols = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_vols, text='Vols')

        self.create_table_views(None)

    def affichage_des_tables(self,utilisateur):
        if utilisateur == Admin:
            # Affichage des tables
            self.frame_tables = tk.Frame(self.root)
            self.frame_tables.pack(pady=10)

            self.tab_control = ttk.Notebook(self.frame_tables)
            self.tab_control.pack(expand=1, fill="both")

            self.tab_utilisateurs = ttk.Frame(self.tab_control)
            self.tab_vols = ttk.Frame(self.tab_control)
            self.tab_reservations = ttk.Frame(self.tab_control)

            self.tab_control.add(self.tab_utilisateurs, text='Utilisateurs')
            self.tab_control.add(self.tab_vols, text='Vols')
            self.tab_control.add(self.tab_reservations, text='Réservations')

            self.create_table_views(utilisateur)
        else :
            # Affichage des tables
            self.frame_tables = tk.Frame(self.root)
            self.frame_tables.pack(pady=10)

            self.tab_control = ttk.Notebook(self.frame_tables)
            self.tab_control.pack(expand=1, fill="both")

            self.tab_vols = ttk.Frame(self.tab_control)
            self.tab_reservations = ttk.Frame(self.tab_control)

            self.tab_control.add(self.tab_vols, text='Vols')
            self.tab_control.add(self.tab_reservations, text='Vos Réservation')

            self.create_table_views(utilisateur)




    def connexion(self):
        email = self.entry_email_connexion.get()
        mot_de_passe = self.entry_mdp_connexion.get()
        utilisateur = session.query(Utilisateur).filter_by(email=email, mot_de_passe=mot_de_passe).first()
        if utilisateur == Admin:
            self.logged_in_user = utilisateur
            messagebox.showinfo("Info", f"Bienvenue, {utilisateur.nom} !")
            self.frame_connexion.pack_forget()  # Masquer la page de connexion après la connexion réussie
            self.frame_inscription.pack_forget()  # Masquer la page d'inscription après la connexion réussie
            self.frame_tables.pack_forget();

            self.menu_bar.add_cascade(label="Ajouter", menu=self.menu_ajouter)
            self.menu_ajouter.add_command(label="Utilisateur", command=self.show_ajouter_utilisateur)
            self.menu_ajouter.add_command(label="Vol", command=self.show_ajouter_vol)
            self.menu_ajouter.add_command(label="Réservation", command=self.show_ajouter_reservation)

            self.menu_bar.add_cascade(label="Supprimer", menu=self.menu_supprimer)
            self.menu_supprimer.add_command(label="Utilisateur", command=self.show_supprimer_utilisateur)
            self.menu_supprimer.add_command(label="Vol", command=self.show_supprimer_vol)
            self.menu_supprimer.add_command(label="Réservation", command=self.show_annuler_reservation)
            self.menu_bar.add_cascade(label="Déconnexion",command=self.root.quit)

            self.affichage_des_tables(utilisateur)

        elif utilisateur != Admin and utilisateur:
            self.logged_in_user = utilisateur
            messagebox.showinfo("Info", f"Bienvenue, {utilisateur.nom} !")
            self.frame_connexion.pack_forget()  # Masquer la page de connexion après la connexion réussie
            self.frame_inscription.pack_forget()  # Masquer la page d'inscription après la connexion réussie
            self.frame_tables.pack_forget(); #Masque la table d'accueil


            self.menu_bar.add_cascade(label="Ajouter", menu=self.menu_ajouter)
            self.menu_ajouter.add_command(label="Réservation", command=self.show_ajouter_reservation)

            self.menu_bar.add_cascade(label="Supprimer", menu=self.menu_supprimer)
            self.menu_supprimer.add_command(label="Réservation", command=self.show_annuler_reservation)
            self.menu_bar.add_cascade(label="Déconnexion",command=self.root.quit)

            self.affichage_des_tables(utilisateur)

        else:
            messagebox.showerror("Erreur", "Email ou mot de passe incorrect")

    def inscription(self):
        nom = self.entry_nom_inscription.get()
        email = self.entry_email_inscription.get()
        mot_de_passe = self.entry_mdp_inscription.get()
        message = DatabaseManager.ajouter_utilisateur(nom, email, mot_de_passe)
        messagebox.showinfo("Info", message)
    def create_table_views(self,utilisateur):
        if utilisateur == Admin:
            # Table view for Utilisateurs
            self.tree_utilisateurs = ttk.Treeview(self.tab_utilisateurs, columns=("id", "nom", "email", "mot_de_passe"), show='headings')
            self.tree_utilisateurs.heading("id", text="ID")
            self.tree_utilisateurs.heading("nom", text="Nom")
            self.tree_utilisateurs.heading("email", text="Email")
            self.tree_utilisateurs.heading("mot_de_passe", text="Mot de passe")
            self.tree_utilisateurs.pack(expand=1, fill="both")
            self.load_utilisateurs()

            # Table view for Vols
            self.tree_vols = ttk.Treeview(self.tab_vols, columns=("id", "numero_vol", "depart", "arrivee", "prix", "prestataire"), show='headings')
            self.tree_vols.heading("id", text="ID")
            self.tree_vols.heading("numero_vol", text="Numéro de vol")
            self.tree_vols.heading("depart", text="Départ")
            self.tree_vols.heading("arrivee", text="Arrivée")
            self.tree_vols.heading("prix", text="Prix")
            self.tree_vols.heading("prestataire", text="Prestataire")
            self.tree_vols.pack(expand=1, fill="both")
            self.load_vols()

            # Table view for Reservations
            self.tree_reservations = ttk.Treeview(self.tab_reservations, columns=("id", "utilisateur_id", "vol_id", "date_reservation"), show='headings')
            self.tree_reservations.heading("id", text="ID")
            self.tree_reservations.heading("utilisateur_id", text="ID Utilisateur")
            self.tree_reservations.heading("vol_id", text="ID Vol")
            self.tree_reservations.heading("date_reservation", text="Date de Réservation")
            self.tree_reservations.pack(expand=1, fill="both")
            self.load_reservations()
        elif utilisateur == None:
            # Table view for Vols
            self.tree_vols = ttk.Treeview(self.tab_vols,columns=("id", "numero_vol", "depart", "arrivee", "prix", "prestataire"),show='headings')
            self.tree_vols.heading("id", text="ID")
            self.tree_vols.heading("numero_vol", text="Numéro de vol")
            self.tree_vols.heading("depart", text="Départ")
            self.tree_vols.heading("arrivee", text="Arrivée")
            self.tree_vols.heading("prix", text="Prix")
            self.tree_vols.heading("prestataire", text="Prestataire")
            self.tree_vols.pack(expand=1, fill="both")
            self.load_vols()

        else:
            # Table view for Vols
            self.tree_vols = ttk.Treeview(self.tab_vols,
                                          columns=("id", "numero_vol", "depart", "arrivee", "prix", "prestataire"),
                                          show='headings')
            self.tree_vols.heading("id", text="ID")
            self.tree_vols.heading("numero_vol", text="Numéro de vol")
            self.tree_vols.heading("depart", text="Départ")
            self.tree_vols.heading("arrivee", text="Arrivée")
            self.tree_vols.heading("prix", text="Prix")
            self.tree_vols.heading("prestataire", text="Prestataire")
            self.tree_vols.pack(expand=1, fill="both")
            self.load_vols()

            # Table view for Reservations
            self.tree_reservations = ttk.Treeview(self.tab_reservations,
                                                  columns=("id", "utilisateur_id", "vol_id", "date_reservation"),
                                                  show='headings')
            self.tree_reservations.heading("id", text="ID")
            self.tree_reservations.heading("utilisateur_id", text="ID Utilisateur")
            self.tree_reservations.heading("vol_id", text="ID Vol")
            self.tree_reservations.heading("date_reservation", text="Date de Réservation")
            self.tree_reservations.pack(expand=1, fill="both")
            self.load_reservations()

    def load_utilisateurs(self):
        # Effacer les éléments existants
        for item in self.tree_utilisateurs.get_children():
            self.tree_utilisateurs.delete(item)
        # Charger les nouvelles données
        for utilisateur in DatabaseManager.get_utilisateurs():
            self.tree_utilisateurs.insert("", "end", values=(utilisateur.id, utilisateur.nom, utilisateur.email, utilisateur.mot_de_passe))

    def load_vols(self):
        # Effacer les éléments existants
        for item in self.tree_vols.get_children():
            self.tree_vols.delete(item)
        # Charger les nouvelles données
        for vol in DatabaseManager.get_vols():
            self.tree_vols.insert("", "end", values=(vol.id, vol.numero_vol, vol.depart, vol.arrivee, vol.prix, vol.prestataire))

    def load_reservations(self):
        # Effacer les éléments existants
        for item in self.tree_reservations.get_children():
            self.tree_reservations.delete(item)
        # Charger les nouvelles données
        for reservation in DatabaseManager.get_reservations():
            self.tree_reservations.insert("", "end", values=(reservation.id, reservation.utilisateur_id, reservation.vol_id, reservation.date_reservation))

    def show_ajouter_utilisateur(self):
        self.dialog_ajouter_utilisateur = tk.Toplevel(self.root)
        self.dialog_ajouter_utilisateur.title("Ajouter Utilisateur")

        tk.Label(self.dialog_ajouter_utilisateur, text="Nom").grid(row=0, column=0)
        self.entry_nom = tk.Entry(self.dialog_ajouter_utilisateur)
        self.entry_nom.grid(row=0, column=1)
        tk.Label(self.dialog_ajouter_utilisateur, text="Email").grid(row=1, column=0)
        self.entry_email = tk.Entry(self.dialog_ajouter_utilisateur)
        self.entry_email.grid(row=1, column=1)
        tk.Label(self.dialog_ajouter_utilisateur, text="Mot de passe").grid(row=2, column=0)
        self.entry_mdp = tk.Entry(self.dialog_ajouter_utilisateur, show="*")
        self.entry_mdp.grid(row=2, column=1)
        self.btn_ajouter_utilisateur = tk.Button(self.dialog_ajouter_utilisateur, text="Ajouter Utilisateur", command=self.ajouter_utilisateur)
        self.btn_ajouter_utilisateur.grid(row=3, columnspan=2)

    def show_ajouter_vol(self):
        self.dialog_ajouter_vol = tk.Toplevel(self.root)
        self.dialog_ajouter_vol.title("Ajouter Vol")

        tk.Label(self.dialog_ajouter_vol, text="Numéro___vol").grid(row=0, column=0)
        self.entry_numero_vol = tk.Entry(self.dialog_ajouter_vol)
        self.entry_numero_vol.grid(row=0, column=1)
        tk.Label(self.dialog_ajouter_vol, text="Départ").grid(row=1, column=0)
        self.entry_depart = tk.Entry(self.dialog_ajouter_vol)
        self.entry_depart.grid(row=1, column=1)
        tk.Label(self.dialog_ajouter_vol, text="Arrivée").grid(row=2, column=0)
        self.entry_arrivee = tk.Entry(self.dialog_ajouter_vol)
        self.entry_arrivee.grid(row=2, column=1)
        tk.Label(self.dialog_ajouter_vol, text="Prix").grid(row=3, column=0)
        self.entry_prix = tk.Entry(self.dialog_ajouter_vol)
        self.entry_prix.grid(row=3, column=1)
        tk.Label(self.dialog_ajouter_vol, text="Prestataire").grid(row=4, column=0)
        self.entry_prestataire = tk.Entry(self.dialog_ajouter_vol)
        self.entry_prestataire.grid(row=4, column=1)
        self.btn_ajouter_vol = tk.Button(self.dialog_ajouter_vol, text="Ajouter Vol", command=self.ajouter_vol_controller)
        self.btn_ajouter_vol.grid(row=5, columnspan=2)

    def show_ajouter_reservation(self):
        self.dialog_ajouter_reservation = tk.Toplevel(self.root)
        self.dialog_ajouter_reservation.title("Ajouter Réservation")

        tk.Label(self.dialog_ajouter_reservation, text="ID Utilisateur").grid(row=0, column=0)
        self.entry_utilisateur_id_reservation = tk.Entry(self.dialog_ajouter_reservation)
        self.entry_utilisateur_id_reservation.grid(row=0, column=1)

        tk.Label(self.dialog_ajouter_reservation, text="ID Vol").grid(row=1, column=0)
        self.entry_vol_id_reservation = tk.Entry(self.dialog_ajouter_reservation)
        self.entry_vol_id_reservation.grid(row=1, column=1)

        self.btn_ajouter_reservation = tk.Button(self.dialog_ajouter_reservation, text="Ajouter Réservation",
                                                 command=self.ajouter_reservation)
        self.btn_ajouter_reservation.grid(row=2, columnspan=2)

    def show_supprimer_vol(self):
        self.dialog_supprimer_vol = tk.Toplevel(self.root)
        self.dialog_supprimer_vol.title("Supprimer Vol")

        tk.Label(self.dialog_supprimer_vol, text="ID Vol à supprimer").grid(row=0, column=0)
        self.entry_vol_id_supprimer = tk.Entry(self.dialog_supprimer_vol)
        self.entry_vol_id_supprimer.grid(row=0, column=1)
        self.btn_supprimer_vol = tk.Button(self.dialog_supprimer_vol, text="Supprimer Vol", command=self.supprimer_vol)
        self.btn_supprimer_vol.grid(row=0, column=2)

    def show_annuler_reservation(self):
        self.dialog_annuler_reservation = tk.Toplevel(self.root)
        self.dialog_annuler_reservation.title("Annuler Réservation")

        tk.Label(self.dialog_annuler_reservation, text="ID Réservation à annuler").grid(row=0, column=0)
        self.entry_reservation_id_annuler = tk.Entry(self.dialog_annuler_reservation)
        self.entry_reservation_id_annuler.grid(row=0, column=1)
        self.btn_annuler_reservation = tk.Button(self.dialog_annuler_reservation, text="Annuler Réservation", command=self.annuler_reservation)
        self.btn_annuler_reservation.grid(row=0, column=2)

    def show_supprimer_utilisateur(self):
        self.dialog_supprimer_utilisateur = tk.Toplevel(self.root)
        self.dialog_supprimer_utilisateur.title("Supprimer Utilisateur")

        tk.Label(self.dialog_supprimer_utilisateur, text="ID Utilisateur à supprimer").grid(row=0, column=0)
        self.entry_utilisateur_id_supprimer = tk.Entry(self.dialog_supprimer_utilisateur)
        self.entry_utilisateur_id_supprimer.grid(row=0, column=1)
        self.btn_supprimer_utilisateur = tk.Button(self.dialog_supprimer_utilisateur, text="Supprimer Utilisateur", command=self.supprimer_utilisateur)
        self.btn_supprimer_utilisateur.grid(row=0, column=2)

    def ajouter_utilisateur(self):
        nom = self.entry_nom.get()
        email = self.entry_email.get()
        mot_de_passe = self.entry_mdp.get()
        message = DatabaseManager.ajouter_utilisateur(nom, email, mot_de_passe)
        messagebox.showinfo("Info", message)
        self.load_utilisateurs()

    def ajouter_reservation(self):
        utilisateur_id = self.entry_utilisateur_id_reservation.get()
        vol_id = self.entry_vol_id_reservation.get()
        message = DatabaseManager.faire_reservation(utilisateur_id, vol_id)
        messagebox.showinfo("Info", message)
        self.load_reservations()

    def ajouter_vol_controller(self):
        numero_vol = self.entry_numero_vol.get()
        depart = self.entry_depart.get()
        arrivee = self.entry_arrivee.get()
        prix = self.entry_prix.get()
        prestataire = self.entry_prestataire.get()
        message = DatabaseManager.ajouter_vol(numero_vol, depart, arrivee, prix, prestataire)
        messagebox.showinfo("Info", message)
        self.load_vols()
        self.dialog_ajouter_vol.destroy()

    def faire_reservation(self):
        utilisateur_id = self.entry_utilisateur_id.get()
        vol_id = self.entry_vol_id.get()
        message = DatabaseManager.faire_reservation(utilisateur_id, vol_id)
        messagebox.showinfo("Info", message)
        self.load_reservations()
        self.dialog_ajouter_reservation.destroy()

    def supprimer_vol(self):
        vol_id = self.entry_vol_id_supprimer.get()
        message = DatabaseManager.supprimer_vol(vol_id)
        messagebox.showinfo("Info", message)
        self.load_vols()

    def annuler_reservation(self):
        reservation_id = self.entry_reservation_id_annuler.get()
        message = DatabaseManager.annuler_reservation(reservation_id)
        messagebox.showinfo("Info", message)
        self.load_reservations()

    def supprimer_utilisateur(self):
        utilisateur_id = self.entry_utilisateur_id_supprimer.get()
        message = DatabaseManager.supprimer_utilisateur(utilisateur_id)
        messagebox.showinfo("Info", message)
        self.load_utilisateurs()


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1200x600")
    CurrentUser = None
    Admin = session.query(Utilisateur).filter_by(nom="Admin").first()

    app = GestionReservationApp(root)
    root.mainloop()
