class Fact:
    def __init__(self, key, value, source=None):
        self.key = key
        self.value = value
        self.source = source

    def __eq__(self, other):
        return self.key == other.key and self.value == other.value

    def __hash__(self):
        return hash((self.key, self.value))

    def __repr__(self):
        return f"Fact({self.key}={self.value})"

class Rule:
    def __init__(self, name, condition, action, description=""):
        self.name = name
        self.condition = condition  # facts -> bool
        self.action = action  # engine -> None
        self.description = description

class Engine:
    def __init__(self):
        self.facts = []
        self.rules = []
        self.triggered_rules = set()
        self.explanations = []

    def add_fact(self, fact):
        self.facts.append(fact)

    def add_rule(self, rule):
        self.rules.append(rule)

    def run(self):
        changed = True
        while changed:
            changed = False
            for rule in self.rules:
                if rule.name not in self.triggered_rules:
                    condition_result = rule.condition(self.facts)
                    if condition_result:
                        rule.action(self)
                        self.triggered_rules.add(rule.name)
                        
                        if rule.description:
                            # Extrae fuentes para XAI
                            if isinstance(condition_result, list) and condition_result:
                                unique_sources = list(set([str(s) for s in condition_result if s]))
                                if unique_sources:
                                    sources_str = ", ".join(unique_sources)
                                    final_desc = rule.description.replace("{sources}", sources_str)
                                else:
                                    final_desc = rule.description.replace("{sources}", "varios de tu equipo")
                            else:
                                final_desc = rule.description.replace("{sources}", "el equipo")
                                
                            self.explanations.append(final_desc)
                            
                        changed = True

    def get_recommendations(self):
        return [f.value for f in self.facts if f.key == 'recommend_item_tag']
