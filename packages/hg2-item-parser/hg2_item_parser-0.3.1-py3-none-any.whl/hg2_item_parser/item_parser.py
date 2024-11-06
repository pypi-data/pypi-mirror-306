from pathlib import Path

from .exceptions import ItemNotFoundError
from .info_parser import InfoParser
from .models import Item, ItemInfo, ItemProperty, ItemSkill
from .property_parser import PropertyParser
from .skill_parser import EquipSkillParser, PetSkillParser
from .tsvreader import TSVReader
from .types_ import ItemCategory


class ItemParser:
    MAIN_DATA_FILE_MAP: dict[ItemCategory, str] = {
        "weapon": "WeaponDataV3.tsv",
        "costume": "CostumeDataV2.tsv",
        "badge": "PassiveSkillDataV3.tsv",
        "pet": "PetData.tsv",
    }
    SKILL_DATA_FILE_MAP: dict[ItemCategory, str] = {
        "weapon": "SpecialAttributeDataV2.tsv",
        "costume": "SpecialAttributeDataV2.tsv",
        "badge": "SpecialAttributeDataV2.tsv",
        "pet": "PetSkillData.tsv",
    }

    def __init__(self, data_dir_path: str):
        self.data_dir_path = Path(data_dir_path)
        self.main_data = self._load_main_data()
        self.skill_data = self._load_skill_data()

    def parse_items_from_to(self, first_item_id: int, last_item_id: int) -> list[Item]:
        items = []
        for item_id in range(first_item_id, last_item_id + 1):
            item = self.parse_item(item_id)
            items.append(item)

        return items

    def parse_item(self, item_id: int) -> Item:
        info = self.parse_item_info(item_id)
        property = self.parse_item_property(item_id)
        skills = self.parse_item_skills(item_id)

        item = Item(
            info,
            property,
            skills,
        )

        return item

    def parse_item_info(self, item_id: int) -> ItemInfo:
        item_main_data = self.search_item_main_data(item_id)
        item_info = InfoParser.parse_info(item_main_data)

        return item_info

    def parse_item_property(self, item_id: int) -> ItemProperty:
        item_main_data = self.search_item_main_data(item_id)
        item_property = PropertyParser.parse_property(item_main_data)

        return item_property

    def parse_item_skills(self, item_id: int) -> list[ItemSkill]:
        item_skills_data = self.search_item_skills_data(item_id)
        item_skills = []
        for i, item_skill_data in enumerate(item_skills_data, start=1):
            if item_skill_data["Category"] == "pet":
                item_skill = PetSkillParser.parse_skill(item_skill_data)
            else:
                item_main_data = self.search_item_main_data(item_id)
                item_skill = EquipSkillParser.parse_skill(
                    item_main_data, item_skill_data, i
                )
            item_skills.append(item_skill)

        return item_skills

    def search_item_skills_data(self, item_id: int) -> list[dict[str, str]]:
        for item_category in self.MAIN_DATA_FILE_MAP:
            item_skills_data = self.get_item_skills_data(item_id, item_category)

            if item_skills_data is not None:
                return item_skills_data

        raise ItemNotFoundError(item_id)

    def get_item_skills_data(
        self, item_id: int, item_category: ItemCategory
    ) -> list[dict[str, str]] | None:
        item_main_data = self.get_item_main_data(item_id, item_category)
        if item_main_data is None:
            return None

        item_skills_data = []
        if item_category == "pet":
            skills_id = PetSkillParser.parse_skills_id(item_main_data)
        else:
            skills_id = EquipSkillParser.parse_skills_id(item_main_data)

        for skill_id in skills_id:
            item_skill_data = self.get_item_skill_data(skill_id, item_category)
            if item_skill_data is None:
                return None
            item_skills_data.append(item_skill_data)

        return item_skills_data

    def get_item_skill_data(
        self, skill_id: int, item_category: ItemCategory
    ) -> dict[str, str] | None:
        category_skills_data = self.skill_data[item_category]
        item_skill_data = category_skills_data.get_row_by_column_value("ID", skill_id)
        if (
            item_skill_data is not None
            and item_skill_data.get("DisplayTitle", "0") != "0"
        ):
            item_skill_data["Category"] = item_category
            return item_skill_data

        return None

    def search_item_main_data(self, item_id: int) -> dict[str, str]:
        for item_category in self.MAIN_DATA_FILE_MAP:
            item_main_data = self.get_item_main_data(item_id, item_category)

            if item_main_data is not None:
                return item_main_data

        raise ItemNotFoundError(item_id)

    def get_item_main_data(
        self, item_id: int | str, item_category: ItemCategory
    ) -> dict[str, str] | None:
        category_main_data = self.main_data[item_category]
        item_main_data = category_main_data.get_row_by_column_value(
            "DisplayNumber", item_id
        )
        if item_main_data is not None:
            item_main_data["Category"] = item_category
            return item_main_data

        return None

    def _load_main_data(self) -> dict[ItemCategory, TSVReader]:
        main_data = self._load_data_many(self.MAIN_DATA_FILE_MAP)

        return main_data

    def _load_skill_data(self) -> dict[ItemCategory, TSVReader]:
        skill_data = self._load_data_many(self.SKILL_DATA_FILE_MAP)

        return skill_data

    def _load_data_many(
        self, data_map: dict[ItemCategory, str]
    ) -> dict[ItemCategory, TSVReader]:
        data = {}
        for name, data_file_name in data_map.items():
            data[name] = self._load_data(data_file_name)

        return data

    def _load_data(self, data_file_name: str) -> TSVReader:
        data_file_path = self.data_dir_path / (data_file_name)
        data = TSVReader(data_file_path)

        return data
