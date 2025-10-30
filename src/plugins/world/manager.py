class WorldManager:
    def __init__(self):
        self.next_id = 0
        self.entities = set()

        """
        self.components = {
            type(Component): {
                EntityId: Component,
                EntityId: Component,
                ...
            },
            type(Component): {
                EntityId: Component,
                EntityId: Component,
                ...
            },
            ...
        }
        """
        self.components = {}  # {ComponentType: {entity_id: component}}

    def create_entity(self):
        entity_id = self.next_id
        self.next_id += 1
        self.entities.add(entity_id)
        return entity_id

    def remove_entity(self, entity_id):
        self.entities.discard(entity_id)
        for comp_dict in self.components.values():
            comp_dict.pop(entity_id, None)

    def add_component(self, entity_id, component):
        comp_type = type(component)
        if comp_type not in self.components:
            self.components[comp_type] = {}
        self.components[comp_type][entity_id] = component

    def get_component(self, entity_id, comp_type):
        return self.components.get(comp_type, {}).get(entity_id)

    def has_component(self, entity_id, comp_type):
        return entity_id in self.components.get(comp_type, {})

    def remove_component(self, entity_id, comp_type):
        if comp_type in self.components:
            self.components[comp_type].pop(entity_id, None)

    def get_entities_with(self, *comp_types):
        if not comp_types:
            return list(self.entities)

        result = set(self.entities)
        for comp_type in comp_types:
            if comp_type in self.components:
                result &= set(self.components[comp_type].keys())
            else:
                return []

        return list(result)
