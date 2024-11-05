from django.db import models

# Table principale pour chaque killmail
class Kill_Killmail(models.Model):
    killmail_id = models.IntegerField(primary_key=True)
    killmail_time = models.DateTimeField()
    solar_system_id = models.IntegerField()
    moon_id = models.IntegerField(null=True, blank=True)
    war_id = models.IntegerField(null=True, blank=True)

    # Position
    position_x = models.FloatField(null=True, blank=True)
    position_y = models.FloatField(null=True, blank=True)
    position_z = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = 'kill_killmail'

    def __str__(self):
        return f"Killmail {self.killmail_id}"

# Table pour enregistrer les détails de la victime dans le killmail
class Kill_Victim(models.Model):
    killmail = models.OneToOneField(Kill_Killmail, on_delete=models.CASCADE, related_name="victim")
    alliance_id = models.IntegerField(null=True, blank=True)
    character_id = models.IntegerField(null=True, blank=True)
    corporation_id = models.IntegerField(null=True, blank=True)
    faction_id = models.IntegerField(null=True, blank=True)
    damage_taken = models.IntegerField()
    ship_type_id = models.IntegerField()

    class Meta:
        db_table = 'kill_victim'

    def __str__(self):
        return f"Victim {self.character_id} in Killmail {self.killmail.killmail_id}"

# Table pour enregistrer les attaquants associés à chaque killmail
class Kill_Attacker(models.Model):
    killmail = models.ForeignKey(Kill_Killmail, on_delete=models.CASCADE, related_name="attackers")
    alliance_id = models.IntegerField(null=True, blank=True)
    character_id = models.IntegerField(null=True, blank=True)
    corporation_id = models.IntegerField(null=True, blank=True)
    faction_id = models.IntegerField(null=True, blank=True)
    damage_done = models.IntegerField()
    final_blow = models.BooleanField()
    security_status = models.FloatField()
    ship_type_id = models.IntegerField()
    weapon_type_id = models.IntegerField()

    class Meta:
        db_table = 'kill_attacker'

    def __str__(self):
        return f"Attacker {self.character_id} for Killmail {self.killmail.killmail_id}"

# Table pour les items possédés par la victime et détruits ou perdus
class Kill_VictimItem(models.Model):
    victim = models.ForeignKey(Kill_Victim, on_delete=models.CASCADE, related_name="items")
    item_type_id = models.IntegerField()
    flag = models.IntegerField()
    quantity_destroyed = models.BigIntegerField(null=True, blank=True)
    quantity_dropped = models.BigIntegerField(null=True, blank=True)
    singleton = models.IntegerField()

    class Meta:
        db_table = 'kill_victim_item'

    def __str__(self):
        return f"Item {self.item_type_id} for Victim {self.victim.character_id}"

# Table pour les sous-items (contenus dans un item de la victime)
class Kill_VictimContainedItem(models.Model):
    parent_item = models.ForeignKey(Kill_VictimItem, on_delete=models.CASCADE, related_name="contained_items")
    item_type_id = models.IntegerField()
    flag = models.IntegerField()
    quantity_destroyed = models.BigIntegerField(null=True, blank=True)
    quantity_dropped = models.BigIntegerField(null=True, blank=True)
    singleton = models.IntegerField()

    class Meta:
        db_table = 'kill_victim_contained_item'

    def __str__(self):
        return f"ContainedItem {self.item_type_id} in Item {self.parent_item.item_type_id}"
