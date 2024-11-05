import requests
from django.core.management.base import BaseCommand
from django.db import transaction, IntegrityError
from aa_killstory.models import Kill_Killmail, Kill_Victim, Kill_Attacker, Kill_VictimItem, Kill_VictimContainedItem
from allianceauth.eveonline.models import EveCharacter

# Points de terminaison API
KILLMAIL_LIST_ENDPOINT = "https://killstory.soeo.fr/{}.json"
KILLMAIL_DETAIL_ENDPOINT = "https://esi.evetech.net/latest/killmails/{}/{}"

BATCH_SIZE = 100  # Taille des lots d'insertion

class Command(BaseCommand):
    help = 'Populate killmails data for all characters'

    def handle(self, *args, **options):
        characters = EveCharacter.objects.all()  # Récupère tous les personnages
        batch = []

        for character in characters:
            try:
                killmails = self.fetch_killmail_list(character.character_id)
                for kill_id, kill_hash in killmails.items():
                    killmail_data = self.fetch_killmail_details(kill_id, kill_hash)
                    killmail = self.create_killmail_instance(killmail_data)
                    batch.append(killmail)

                    # Insère le batch dans la base de données lorsque la taille est atteinte
                    if len(batch) >= BATCH_SIZE:
                        self.save_batch(batch)
                        batch.clear()

            except requests.HTTPError as e:
                self.stdout.write(self.style.ERROR(f"Erreur de requête pour character_id {character.character_id}: {e}"))
            except IntegrityError as e:
                self.stdout.write(self.style.ERROR(f"Erreur d'intégrité pour character_id {character.character_id}: {e}"))

        # Insère le dernier lot
        if batch:
            self.save_batch(batch)
        self.stdout.write(self.style.SUCCESS("Population terminée"))

    def fetch_killmail_list(self, character_id):
        """Récupère la liste des killmails pour un personnage donné."""
        response = requests.get(KILLMAIL_LIST_ENDPOINT.format(character_id))
        response.raise_for_status()
        return response.json()

    def fetch_killmail_details(self, kill_id, kill_hash):
        """Récupère les détails d'un killmail spécifique."""
        response = requests.get(KILLMAIL_DETAIL_ENDPOINT.format(kill_id, kill_hash))
        response.raise_for_status()
        return response.json()

    def create_killmail_instance(self, data):
        """Crée et retourne une instance de Kill_Killmail et ses relations."""
        killmail = Kill_Killmail(
            killmail_id=data['killmail_id'],
            killmail_time=data['killmail_time'],
            solar_system_id=data['solar_system_id'],
            moon_id=data.get('moon_id'),
            war_id=data.get('war_id'),
            position_x=data.get('position', {}).get('x'),
            position_y=data.get('position', {}).get('y'),
            position_z=data.get('position', {}).get('z')
        )
        return killmail

    def save_batch(self, batch):
        """Sauvegarde un lot de killmails avec les informations complètes en une transaction."""
        with transaction.atomic():
            for killmail in batch:
                try:
                    killmail.save()
                    if "victim" in killmail:
                        self.create_victim_instance(killmail, killmail_data['victim'])
                    for attacker_data in killmail_data['attackers']:
                        self.create_attacker_instance(killmail, attacker_data)
                except IntegrityError:
                    continue  # Ignore les erreurs d'intégrité et passe au killmail suivant
