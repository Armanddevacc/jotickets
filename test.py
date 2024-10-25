import requests
import db.spectators
import db.tickets


##ajoutez un utilisateur
def set_spectator(prenom,password):
    url = "http://localhost:5001/spectators/"
    spectator = {'username':prenom,'password':password}
    print(1)
    response = requests.post(url,json=spectator)


    # Afficher le statut et le contenu de la réponse
    if response.status_code == 200:
        print("opération validé")
    else:
        print(f"Erreur: {response.status_code}")
        


##modifier mdp
def update_password(spectator_username, mdp):
    url = f"http://localhost:5001/spectators/{spectator_username}"
    nouveau_mdp = {'password':mdp}
    # Envoyer une requête GET pour récupérer tous les spectateurs
    response = requests.patch(url,json=nouveau_mdp)
    # Afficher le statut et le contenu de la réponse
    if response.status_code == 200:
        print("Liste des spectateurs :", response.json())
    else:
        print(f"Erreur: {response.status_code}")


def update_event(id, params):
    url = f"http://localhost:5001/events/{id}"
    # Envoyer une requête GET pour récupérer tous les spectateurs
    response = requests.patch(url,json=params)
    # Afficher le statut et le contenu de la réponse
    if response.status_code == 200:
        print("Liste des spectateurs :", response.json())
    else:
        print(f"Erreur: {response.status_code}")



D={"Competition_Phase":"Girls group B" ,"Type":"FBL", "Gender":"M", "Status":"FINISHED", "Discipline_Code":"HTEAM", "Results_URL":"https://2024olympics", "location_code":"TKY", "start_date":"10/07/2025", "End_Date":"14/07/2025"}

def create_tickets(ticket_code, spectator_username, maxGuests,event_Code):
    conn = db.get_db_connexion()
    db.tickets.insert_ticket(ticket_code, maxGuests, event_Code, spectator_username, conn)
    conn.close()

##modifier acheteur d'un ticket
def update_user(ticket_id, nom):
    url = f"http://localhost:5001/tickets/{ticket_id}/purchase"
    nouveau_name = {'Username':nom}
    # Envoyer une requête GET pour récupérer tous les spectateurs
    response = requests.patch(url,json=nouveau_name)
    # Afficher le statut et le contenu de la réponse
    if response.status_code == 200:
        print("Liste des spectateurs :", response.json())
    else:
        print(f"Erreur: {response.status_code}")


# def test_get_spectator_data():
#     conn = db.get_db_connexion()
#     cursor = conn.cursor()
#     print(dict(db.spectators.get_spectator_data("Jenifer", cursor)))
#     conn.close()


if __name__ == "__main__":

    #db.transform_csv("data/schedules.csv", "data/schedules2.csv")
    #print(app_utils.load_config())
    #update_event(1, D)
    #create_tickets(10000001, "Armand", 1000, 1)
    #create_tickets(10000002, "Armand", 1000, 1)
    #create_tickets(10000003, "Armand", 1000, 1)
    #create_tickets(10000004, "Armand", 1000, 1)
    #update_user(10000002, "Jenifer")
    set_spectator("Armando","password")
