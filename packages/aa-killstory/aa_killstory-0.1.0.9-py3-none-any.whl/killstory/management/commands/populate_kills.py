import requests
import time
from django.core.management.base import BaseCommand
from django.db import transaction, IntegrityError
from aa_killstory.models import Kill_Killmail, Kill_Victim, Kill_Attacker, Kill_VictimItem, Kill_VictimContainedItem
from allianceauth.eveonline.models import EveCharacter

# Points de terminaison API
KILLMAIL_LIST_ENDPOINT = "https://killstory.soeo.fr/{}.json"
KILLMAIL_DETAIL_ENDPOINT = "https://esi.evetech.net/latest/killmails/{}/{}"

BATCH_SIZE = 100  # Taille des lots d'insertion
RETRY_LIMIT = 5   # Limite des tentatives de récupération de données

class Command(BaseCommand):
    help = 'Populate killmails data for all characters'

    def handle(self, *args, **options):
        characters = EveCharacter.objects.all()
        batch = []

        for character in characters:
            try:
                killmails = self.fetch_killmail_list(character.character_id)
                if not killmails:
                    continue  # Passe au personnage suivant si aucun killmail trouvé
                for kill_id, kill_hash in killmails.items():
                    killmail_data = self.fetch_killmail_details(kill_id, kill_hash)
                    if not killmail_data:
                        continue  # Si les détails du killmail sont introuvables, passe au suivant
                    killmail = self.create_killmail_instance(killmail_data)
                    batch.append((killmail, killmail_data))

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
        """Récupère la liste des killmails pour un personnage donné. Passe si non trouvé."""
        try:
            response = self.make_request(KILLMAIL_LIST_ENDPOINT.format(character_id))
            if response and response.status_code == 404:
                self.stdout.write(self.style.WARNING(f"Character_id {character_id} non trouvé, passage au suivant."))
                return {}  # Retourne un dictionnaire vide pour passer au personnage suivant
            return response.json() if response else {}
        except requests.RequestException as e:
            self.stdout.write(self.style.ERROR(f"Erreur lors de la récupération des killmails pour character_id {character_id}: {e}"))
            return {}

    def fetch_killmail_details(self, kill_id, kill_hash):
        """Récupère les détails d'un killmail spécifique."""
        response = self.make_request(KILLMAIL_DETAIL_ENDPOINT.format(kill_id, kill_hash))
        return response.json() if response else {}

    def make_request(self, url):
        """Effectue une requête avec gestion des erreurs et des pauses."""
        retries = 0
        while retries < RETRY_LIMIT:
            try:
                response = requests.get(url)
                status_code = response.status_code
                if status_code == 304:
                    self.stdout.write(self.style.WARNING("Requête non modifiée (304), utilisation de données en cache."))
                    return None  # Pas de nouvelle donnée à récupérer
                elif status_code == 400:
                    self.stdout.write(self.style.ERROR("Requête incorrecte (400), passage au suivant."))
                    return None
                elif status_code == 404:
                    return response  # Gérer 404 dans `fetch_killmail_list`
                elif status_code == 420:
                    self.stdout.write(self.style.WARNING("Limite atteinte (420), pause de 60 secondes."))
                    time.sleep(60)
                elif status_code == 422:
                    self.stdout.write(self.style.ERROR("Données de killmail invalides (422), passage au suivant."))
                    return None
                elif status_code == 500:
                    self.stdout.write(self.style.WARNING("Erreur interne serveur (500), tentative de nouvelle requête..."))
                    time.sleep(2 ** retries)  # Exponential backoff
                elif status_code == 503:
                    self.stdout.write(self.style.WARNING("Service indisponible (503), tentative de nouvelle requête..."))
                    time.sleep(2 ** retries)  # Exponential backoff
                elif status_code == 504:
                    self.stdout.write(self.style.WARNING("Délai d'attente dépassé (504), tentative de nouvelle requête..."))
                    time.sleep(2 ** retries)  # Exponential backoff
                else:
                    response.raise_for_status()
                    return response
            except requests.RequestException as e:
                self.stdout.write(self.style.ERROR(f"Erreur réseau : {e}, tentative {retries + 1}"))
            retries += 1

        self.stdout.write(self.style.ERROR("Limite de tentatives atteinte, passage au killmail suivant."))
        return None

    def create_killmail_instance(self, data):
        """Crée et retourne une instance de Kill_Killmail."""
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
            for killmail, killmail_data in batch:
                try:
                    killmail.save()
                    if "victim" in killmail_data:
                        self.create_victim_instance(killmail, killmail_data['victim'])
                    for attacker_data in killmail_data.get('attackers', []):
                        self.create_attacker_instance(killmail, attacker_data)
                except IntegrityError:
                    continue  # Ignore les erreurs d'intégrité et passe au killmail suivant

    def create_victim_instance(self, killmail, victim_data):
        """Crée et sauvegarde l'instance de Victime associée au Killmail."""
        victim = Kill_Victim(
            killmail=killmail,
            alliance_id=victim_data.get('alliance_id'),
            character_id=victim_data.get('character_id'),
            corporation_id=victim_data.get('corporation_id'),
            faction_id=victim_data.get('faction_id'),
            damage_taken=victim_data['damage_taken'],
            ship_type_id=victim_data['ship_type_id']
        )
        victim.save()
        for item_data in victim_data.get('items', []):
            self.create_victim_item_instance(victim, item_data)

    def create_attacker_instance(self, killmail, attacker_data):
        """Crée et sauvegarde une instance d'attaquant pour le Killmail."""
        attacker = Kill_Attacker(
            killmail=killmail,
            alliance_id=attacker_data.get('alliance_id'),
            character_id=attacker_data.get('character_id'),
            corporation_id=attacker_data.get('corporation_id'),
            faction_id=attacker_data.get('faction_id'),
            damage_done=attacker_data['damage_done'],
            final_blow=attacker_data['final_blow'],
            security_status=attacker_data['security_status'],
            ship_type_id=attacker_data['ship_type_id'],
            weapon_type_id=attacker_data.get('weapon_type_id')
        )
        attacker.save()

    def create_victim_item_instance(self, victim, item_data):
        """Crée et sauvegarde un item pour la victime."""
        item = Kill_VictimItem(
            victim=victim,
            item_type_id=item_data['item_type_id'],
            flag=item_data['flag'],
            quantity_destroyed=item_data.get('quantity_destroyed'),
            quantity_dropped=item_data.get('quantity_dropped'),
            singleton=item_data['singleton']
        )
        item.save()
        for contained_item_data in item_data.get('items', []):
            self.create_contained_item_instance(item, contained_item_data)

    def create_contained_item_instance(self, parent_item, contained_item_data):
        """Crée et sauvegarde un item contenu pour un item parent."""
        contained_item = Kill_VictimContainedItem(
            parent_item=parent_item,
            item_type_id=contained_item_data['item_type_id'],
            flag=contained_item_data['flag'],
            quantity_destroyed=contained_item_data.get('quantity_destroyed'),
            quantity_dropped=contained_item_data.get('quantity_dropped'),
            singleton=contained_item_data['singleton']
        )
        contained_item.save()
