"""
STIG Mapping Engine
"""

import json
import logging
import os
from typing import List, Dict

from regscale.models import SecurityPlan
from regscale.models.regscale_models import Asset, AssetMapping, Component

logger = logging.getLogger(__name__)


class StigMappingEngine:
    """
    A class to map assets to STIGs based on defined rules.
    """

    comparator_functions = {
        "equals": lambda a, b: a == b,
        "contains": lambda a, b: b in a,
        "notcontains": lambda a, b: b not in a,
        "startswith": lambda a, b: a.startswith(b),
        "notin": lambda a, b: b not in a,
        "endswith": lambda a, b: a.endswith(b),
        "notstartswith": lambda a, b: not a.startswith(b),
        "notendswith": lambda a, b: not a.endswith(b),
        "gt": lambda a, b: a > b,
        "lt": lambda a, b: a < b,
        "gte": lambda a, b: a >= b,
        "lte": lambda a, b: a <= b,
        "ne": lambda a, b: a != b,
        "in": lambda a, b: a in b,
        "nin": lambda a, b: a not in b,
    }

    def __init__(self, json_file: str):
        self.rules = self.load_rules(json_file)
        logger.info(f"Loaded {len(self.rules)} rules from {json_file}")
        # Preprocess rules for faster access
        self.stig_to_rules = {}
        for rule in self.rules:
            stig_name = rule.get("stig")
            if stig_name not in self.stig_to_rules:
                self.stig_to_rules[stig_name] = []
            self.stig_to_rules[stig_name].append(rule.get("comparators", []))

    @staticmethod
    def load_rules(json_file: str) -> List[Dict[str, str]]:
        """
        Load rules from a JSON file.

        :param str json_file: The path to the JSON file.
        :return: A list of rules.
        :rtype: List[Dict[str, str]]
        """
        if not os.path.exists(json_file):
            logger.error(f"File not found: {json_file}")
            return []
        try:
            with open(json_file, "r") as file:
                data = json.load(file)
                return data.get("rules", [])
        except json.JSONDecodeError as e:
            logger.error(f"JSON decoding error in file {json_file}: {e}")
        except Exception as e:
            logger.error(f"Error loading rules from {json_file}: {e}")
        return []

    @staticmethod
    def asset_matches_comparators(asset: Asset, comparators: List[Dict[str, str]]) -> bool:
        """
        Determine if the asset matches the given comparators.

        :param Asset asset: An asset.
        :param List[Dict[str, str]] comparators: List of comparator dictionaries.
        :return: True if the asset matches the comparators, False otherwise.
        """
        match_result = True

        for comparator in comparators:
            property_name = comparator.get("property")
            if not hasattr(asset, property_name):
                return False

            operator = comparator.get("comparator")
            comparator_func = StigMappingEngine.comparator_functions.get(operator)
            if not comparator_func:
                return False

            value = comparator.get("value")
            asset_value = getattr(asset, property_name)
            comparison_result = comparator_func(asset_value, value)

            logical_operator = comparator.get("logical_operator", "and").lower()

            if logical_operator == "and":
                match_result = match_result and comparison_result
                if not match_result:
                    return False
            elif logical_operator == "or":
                match_result = match_result or comparison_result
            else:
                logger.warning(f"Unknown logical operator: {logical_operator}")
                return False

        return match_result

    def match_asset_to_stigs(self, asset: Asset, ssp_id: int) -> List[Component]:
        """
        Match an asset to STIG components based on rules.

        :param Asset asset: An asset.
        :param int ssp_id: The security plan ID.
        :return: A list of matching components.
        :rtype: List[AssetMapping]
        """
        if not self.rules:
            return []

        # Cache components to avoid redundant database queries
        if not hasattr(self, "_component_cache"):
            components = Component.get_all_by_parent(parent_module=SecurityPlan.get_module_slug(), parent_id=ssp_id)
            self._component_cache = {comp.title: comp for comp in components}
        else:
            components = self._component_cache.values()

        matching_components = []

        for stig_name, comparators_list in self.stig_to_rules.items():
            component = self._component_cache.get(stig_name)
            if not component:
                continue

            for comparators in comparators_list:
                if self.asset_matches_comparators(asset, comparators):
                    matching_components.append(component)
                    break  # No need to check other comparators for this STIG

        return matching_components

    def map_stigs_to_assets(
        self,
        assets: List[Asset],
        ssp_id: int,
    ) -> List[AssetMapping]:
        """
        Map STIG components to assets based on rules.

        :param List[Asset] asset_list assets: A list of assets.
        :param List[Component] ssp_id: The security plan ID.
        :return: A list of asset mappings.
        :rtype: List[AssetMapping]
        """
        new_mappings = []

        # Cache components to avoid redundant database queries
        if not hasattr(self, "_component_cache"):
            components = Component.get_all_by_parent(parent_module=SecurityPlan.get_module_slug(), parent_id=ssp_id)
            self._component_cache = {comp.title: comp for comp in components}
        else:
            components = self._component_cache.values()

        # Build a mapping of existing mappings for quick lookup
        existing_mappings = {}
        for component in components:
            mappings = AssetMapping.find_mappings(component_id=component.id)
            existing_mappings[component.id] = {m.assetId for m in mappings}

        for stig_name, comparators_list in self.stig_to_rules.items():
            component = self._component_cache.get(stig_name)
            if not component:
                continue

            component_existing_asset_ids = existing_mappings.get(component.id, set())

            for asset in assets:
                for comparators in comparators_list:
                    if self.asset_matches_comparators(asset, comparators):
                        if asset.id not in component_existing_asset_ids:
                            mapping = AssetMapping(assetId=asset.id, componentId=component.id)
                            new_mappings.append(mapping)
                            component_existing_asset_ids.add(asset.id)
                            logger.info(f"Mapping -> Asset ID: {asset.id}, Component ID: {component.id}")
                        else:
                            logger.info(
                                f"Existing mapping found for Asset ID: {asset.id}, Component ID: {component.id}"
                            )
                        break  # No need to check other comparators for this asset and STIG

        return new_mappings

    def map_associated_stigs_to_asset(self, asset: Asset, ssp_id: int) -> List[AssetMapping]:
        """
        Map associated STIGs to an asset based on rules.

        :param asset: An asset.
        :param ssp_id: The security plan ID.
        :return: A list of asset mappings.
        """
        new_mappings = []
        associated_components = self.match_asset_to_stigs(asset, ssp_id)

        # Pre-fetch existing mappings to avoid redundant database calls
        existing_mappings = AssetMapping.get_all_by_parent(parent_module=Asset.get_module_slug(), parent_id=asset.id)
        existing_component_ids = {m.componentId for m in existing_mappings}

        for component in associated_components:
            if component.id not in existing_component_ids:
                mapping = AssetMapping(assetId=asset.id, componentId=component.id)
                mapping.create()
                new_mappings.append(mapping)
                logger.debug(f"Created mapping for Asset ID: {asset.id}, Component ID: {component.id}")
            else:
                logger.debug(f"Mapping already exists for Asset ID: {asset.id}, Component ID: {component.id}")

        return new_mappings
