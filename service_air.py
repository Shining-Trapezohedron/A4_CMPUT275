from unit.air_unit import AirUnit
import unit, helper, effects
from unit.base_unit import BaseUnit
from tiles import Tile
import pygame

class service_air(AirUnit):
    """
    A fighter jet. Moves fast, but needs to refuel constantly. Good at peppering
    the ground with shots as well as eliminating other air units.
    
    Armour: Low
    Speed: Medium
    Range: Low
    Damage: None
    Fuel: Medium
    
    Other notes:
    - In order to maintain its high speed, the fighter has fairly low fuel.
      Make well-planned strafing runs and be sure you can get back to a carrier
      in time!
    - When firing at another air unit, this unit does extra damage.
    """
    sprite = pygame.image.load("assets/service_air.png")
    
    def __init__(self, **keywords):
        #load the image for the base class.
        self._base_image = service_air.sprite

        #load the base class
        super().__init__(**keywords)
        
        #sounds
        self.hit_sound = "MachineGunFire"

        #set unit specific things.
        self.type = "Air Service"
        self.speed = 8
        self.max_atk_range = 1
        self.damage = 3
        self.defense = 0
        self.bonus_damage = 0
        self.max_fuel = 20
        self.set_fuel(self.max_fuel)
        self.min_move_distance = 3
        self.hit_effect = effects.Ricochet
        
    def get_damage(self, target, target_tile):
        """
        Returns the potential attack damage against a given enemy.
        
        This overrides the super class function to allow
        special damage effects.
        """
        # Do bonus damage to other air unit
        if target.health < target.max_health:
            if (target.health + self.damage)>= target.max_health:
                target.health = target.max_health
            else:
                target.health = target.health + self.damage
        return 0


    def is_attackable(self, from_tile, from_pos, to_tile, to_pos):
        """
        Returns whether the given tile is attackable.
        
        Override this for subclasses, perhaps using this as a default value.
        """
        # We can only attack within the unit's range.
        if not self.is_tile_in_range(from_tile, from_pos, to_pos):
            return False
        
        # Get the unit we're going to attack.
        u = BaseUnit.get_unit_at_pos(to_pos)
        
        # We can't attack if there's no unit there, if it's on our team,
        # if we can't hit this particular unit, or if the damage is 0
        if (not u):
            return False
        if (u
            and u.team == self.team
            and self.can_hit(u)
            and from_pos != to_pos):
            return True
 
            
        return False

unit.unit_types["service_air"] = service_air
