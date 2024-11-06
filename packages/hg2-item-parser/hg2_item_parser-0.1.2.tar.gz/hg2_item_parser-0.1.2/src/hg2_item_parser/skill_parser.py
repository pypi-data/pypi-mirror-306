from .info_parser import InfoParser
from .models import ItemSkill
from .property_parser import PropertyParser
from .text_parser import TextParser
from .unificator import Unificator


class BaseSkillParser:
    @classmethod
    def parse_description_template(cls, item_skill_data: dict[str, str]) -> str:
        description_template_id = cls.parse_description_template_id(item_skill_data)
        description_template = TextParser.parse_text(description_template_id)

        return description_template

    @staticmethod
    def parse_description_template_id(item_skill_data: dict[str, str]) -> int:
        description_template_id = int(
            item_skill_data["DisplayDescription"].replace("TEXT", "")
        )

        return description_template_id

    @staticmethod
    def parse_id(item_skill_data: dict[str, str]) -> int:
        skill_id = int(item_skill_data["ID"])

        return skill_id

    @staticmethod
    def parse_damage_type(item_skill_data: dict[str, str]) -> str | None:
        damage_type = item_skill_data.get("Feature", "none")

        return Unificator.unificate_damage_type(damage_type)

    @classmethod
    def parse_title(cls, item_skill_data: dict[str, str]) -> str:
        title_id = cls.parse_title_id(item_skill_data)
        title = TextParser.parse_text(title_id)

        return title

    @staticmethod
    def parse_title_id(item_skill_data: dict[str, str]) -> int:
        title_id = int(item_skill_data["DisplayTitle"].replace("TEXT", ""))

        return title_id


class EquipSkillParser(BaseSkillParser):
    FANTASY_LEGEND_IDS = (
        4259,
        4260,
        4352,
        4353,
        4413,
        4414,
        4452,
        4453,
        4454,
        4497,
        4498,
        4501,
        4502,
        4503,
        4520,
        4521,
        4561,
        4562,
        4619,
        4620,
        4675,
        4676,
        4683,
        4684,
        4714,
        4715,
        4752,
        4753,
        4754,
        4755,
    )

    @classmethod
    def parse_skill(
        cls,
        item_main_data: dict[str, str],
        item_skill_data: dict[str, str],
        skill_num: int,
    ) -> ItemSkill:
        id = cls.parse_id(item_skill_data)
        damage_type = cls.parse_damage_type(item_skill_data)
        title_id = cls.parse_title_id(item_skill_data)
        title = cls.parse_title(item_skill_data)
        description_template_id = cls.parse_description_template_id(item_skill_data)
        description_template = cls.parse_description_template(item_skill_data)
        description = cls.parse_description(item_main_data, item_skill_data, skill_num)

        skill = ItemSkill(
            id,
            damage_type,
            title_id,
            title,
            description_template_id,
            description_template,
            description,
        )

        return skill

    @classmethod
    def parse_description(
        cls,
        item_main_data: dict[str, str],
        item_skill_data: dict[str, str],
        skill_num: int,
    ) -> str:
        description_template = cls.parse_description_template(item_skill_data)
        max_break_values = cls.parse_max_break_values(
            item_main_data, item_skill_data, skill_num
        )
        max_lvl_values = cls.parse_max_lvl_values(item_main_data, skill_num)
        description = TextParser.fill_skill_description_template(
            description_template, max_lvl_values, max_break_values
        )

        return description

    @classmethod
    def parse_max_break_values(
        cls,
        item_main_data: dict[str, str],
        item_skill_data: dict[str, str],
        skill_num: int,
    ) -> list[float]:
        max_break_values = []
        slot_num = cls.parse_slot_num(item_main_data, item_skill_data)
        for i in range(1, 6):
            max_break_value = cls.parse_max_break_value(
                item_main_data, item_skill_data, slot_num, skill_num, i
            )
            max_break_values.append(max_break_value)

        return max_break_values

    @classmethod
    def parse_max_break_value(
        cls,
        item_main_data: dict[str, str],
        item_skill_data: dict[str, str],
        slot_num: int,
        skill_num: int,
        param_num: int,
    ) -> float:
        max_up_value = cls.parse_max_up_value(item_skill_data, slot_num)
        max_lvl_value = cls.parse_max_lvl_value(item_main_data, skill_num, param_num)
        value_per_up = cls.parse_value_per_up(item_skill_data, slot_num, param_num)
        max_break_value = PropertyParser._calculate_value_on_lvl(
            max_lvl_value, value_per_up, max_up_value + 1, 5
        )

        return max_break_value

    @staticmethod
    def parse_max_up_value(item_skill_data: dict[str, str], slot_num: int) -> int:
        max_up_value_name = f"Slot{slot_num}MaxLevel"
        max_up_value = int(item_skill_data[max_up_value_name])

        return max_up_value

    @staticmethod
    def parse_value_per_up(
        item_skill_data: dict[str, str], slot_num: int, param_num: int
    ) -> float:
        value_per_up_name = f"Slot{slot_num}Para{param_num}Add"
        value_per_up = float(item_skill_data[value_per_up_name])

        return value_per_up

    @classmethod
    def parse_max_lvl_values(
        cls, item_main_data: dict[str, str], skill_num: int
    ) -> list[float]:
        max_lvl_values = []
        for i in range(1, 6):
            max_lvl_value = cls.parse_max_lvl_value(item_main_data, skill_num, i)
            max_lvl_values.append(max_lvl_value)

        return max_lvl_values

    @classmethod
    def parse_max_lvl_value(
        cls, item_main_data: dict[str, str], skill_num: int, param_num: int
    ) -> float:
        base_value = cls.parse_base_value(item_main_data, skill_num, param_num)
        value_per_lvl = cls.parse_value_per_lvl(item_main_data, skill_num, param_num)
        max_lvl = PropertyParser.parse_max_lvl(item_main_data)
        max_lvl_value = PropertyParser._calculate_value_on_lvl(
            base_value, value_per_lvl, max_lvl, 5
        )

        return max_lvl_value

    @staticmethod
    def parse_value_per_lvl(
        item_main_data: dict[str, str], skill_num: int, param_num: int
    ) -> float:
        value_name = f"Prop{skill_num}Param{param_num}Add"
        value = float(item_main_data[value_name])

        return value

    @staticmethod
    def parse_base_value(
        item_main_data: dict[str, str], skill_num: int, param_num: int
    ) -> float:
        value_name = f"Prop{skill_num}Param{param_num}"
        value = float(item_main_data[value_name])

        return value

    @classmethod
    def parse_slot_num(
        cls, item_main_data: dict[str, str], item_skill_data: dict[str, str]
    ) -> int:
        slots = cls.parse_slots(item_skill_data)
        for slot_num, slot in enumerate(slots, start=1):
            id = InfoParser.parse_id(item_main_data)
            if str(id) in slot.split(";"):
                slot_num = 1
                break

        return slot_num

    @classmethod
    def parse_slots(cls, item_skill_data: dict[str, str]) -> list[str]:
        slots = []
        slot_range = cls.parse_slot_range(item_skill_data)
        for i in slot_range:
            slot = item_skill_data[f"Slot{i}Equips"]
            slots.append(slot)

        return slots

    @classmethod
    def parse_slot_range(cls, item_skill_data: dict[str, str]) -> list[int]:
        slot_count = cls.parse_slot_count(item_skill_data)
        slot_range = list(range(1, slot_count + 1))

        return slot_range

    @staticmethod
    def parse_slot_count(item_skill_data: dict[str, str]) -> int:
        slot_count = int(item_skill_data["SlotCount"])

        return slot_count

    @classmethod
    def parse_skills_id(cls, item_main_data: dict[str, str]) -> list[int]:
        skills_id = []
        skill_range = cls.parse_skill_range(item_main_data)
        for i in skill_range:
            skill_id = cls.parse_skill_id(item_main_data, i)
            skills_id.append(skill_id)

        return skills_id

    @staticmethod
    def parse_skill_id(item_main_data: dict[str, str], skill_num: int) -> int:
        skill_name = f"Prop{skill_num}id"
        skill_id = int(item_main_data[skill_name])

        return skill_id

    @classmethod
    def parse_skill_range(cls, item_main_data: dict[str, str]) -> list[int]:
        skill_count = cls.parse_skill_count(item_main_data)
        skill_range = list(range(1, skill_count + 1))
        id = InfoParser.parse_id(item_main_data)
        if id in cls.FANTASY_LEGEND_IDS:
            skill_range += [6, 7]

        return skill_range

    @staticmethod
    def parse_skill_count(item_main_data: dict[str, str]) -> int:
        skill_count = int(item_main_data["NumProps"])

        return skill_count


class PetSkillParser(BaseSkillParser):
    SKILL_NAMES = (
        "UltraSkillid",
        "HiddenUltraSkillid",
        "normalSkill1Id",
        "normalSkill2Id",
    )

    @classmethod
    def parse_skill(cls, item_skill_data: dict[str, str]) -> ItemSkill:
        id = cls.parse_id(item_skill_data)
        damage_type = cls.parse_damage_type(item_skill_data)
        title_id = cls.parse_title_id(item_skill_data)
        title = cls.parse_title(item_skill_data)
        description_template_id = cls.parse_description_template_id(item_skill_data)
        description_template = cls.parse_description_template(item_skill_data)
        description = cls.parse_description(item_skill_data)

        skill = ItemSkill(
            id,
            damage_type,
            title_id,
            title,
            description_template_id,
            description_template,
            description,
        )

        return skill

    @classmethod
    def parse_description(cls, item_skill_data: dict[str, str]) -> str:
        description_template = cls.parse_description_template(item_skill_data)
        max_break_values = cls.parse_max_break_values(item_skill_data)
        max_lvl_values = cls.parse_values(item_skill_data)
        description = TextParser.fill_skill_description_template(
            description_template, max_lvl_values, max_break_values
        )

        return description

    @classmethod
    def parse_max_break_values(cls, item_skill_data: dict[str, str]) -> list[float]:
        max_break_values = []
        for i in range(1, 7):
            max_break_value = cls.parse_max_break_value(item_skill_data, i)
            max_break_values.append(max_break_value)

        return max_break_values

    @classmethod
    def parse_max_break_value(
        cls, item_skill_data: dict[str, str], param_num: int
    ) -> float:
        max_up_value = cls.parse_max_up_value(item_skill_data)
        value = cls.parse_value(item_skill_data, param_num)
        value_per_up = cls.parse_value_per_up(item_skill_data, param_num)
        max_break_value = PropertyParser._calculate_value_on_lvl(
            value, value_per_up, max_up_value + 1, 5
        )

        return max_break_value

    @staticmethod
    def parse_max_up_value(item_skill_data: dict[str, str]) -> int:
        max_up_value = int(item_skill_data["Maxlevel"])

        return max_up_value

    @staticmethod
    def parse_value_per_up(item_skill_data: dict[str, str], param_num: int) -> float:
        value_per_up_name = f"Para{param_num}SkillUpAdd"
        value_per_up = float(item_skill_data[value_per_up_name])

        return value_per_up

    @classmethod
    def parse_values(cls, item_skill_data: dict[str, str]) -> list[float]:
        values = []
        for i in range(1, 7):
            value = cls.parse_value(item_skill_data, i)
            values.append(value)

        return values

    @staticmethod
    def parse_value(item_skill_data: dict[str, str], param_num: int) -> float:
        value = float(item_skill_data[f"Para{param_num}"])

        return value

    @classmethod
    def parse_skills_id(cls, item_main_data: dict[str, str]) -> list[int]:
        skills_id = []
        for i in range(1, 5):
            skill_id = cls.parse_skill_id(item_main_data, i)
            skills_id.append(skill_id)

        return skills_id

    @classmethod
    def parse_skill_id(cls, item_main_data: dict[str, str], skill_num: int) -> int:
        skill_name = cls.SKILL_NAMES[skill_num - 1]
        skill_id = int(item_main_data[skill_name])

        return skill_id
