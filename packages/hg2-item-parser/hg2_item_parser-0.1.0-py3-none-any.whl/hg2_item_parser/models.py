from dataclasses import dataclass
from typing import Literal


@dataclass
class ItemInfo:
    id: int
    title_id: int
    title: str
    image_id: int
    image_url: str
    damage_type: str | None
    rarity: int


@dataclass
class ItemProperty:
    max_lvl: int


@dataclass
class WeaponProperty(ItemProperty):
    cost: int
    max_lvl_hp: int | float
    type: str | None
    max_lvl_damage: int | float
    max_lvl_ammo: int | float | Literal["∞"]
    max_lvl_atk_speed: float
    deploy_limit: int
    duration: float
    crit_rate: str


@dataclass
class CostumeProperty(ItemProperty):
    cost: int
    max_lvl_hp: int | float


@dataclass
class BadgeProperty(ItemProperty):
    cost: int


@dataclass
class PetProperty(ItemProperty):
    max_lvl_damage: int | float
    crit_rate: str
    base_sync: int | float
    max_sync: int | float


@dataclass
class ItemSkill:
    id: int
    damage_type: str | None
    title_id: int
    title: str
    description_template_id: int
    description_template: str
    description: str


@dataclass
class Item:
    info: ItemInfo
    property: ItemProperty
    skills: list[ItemSkill]
