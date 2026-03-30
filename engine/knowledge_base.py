class Fact:
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __eq__(self, other):
        return self.key == other.key and self.value == other.value

    def __hash__(self):
        return hash((self.key, self.value))

    def __repr__(self):
        return f"Fact({self.key}={self.value})"

class Rule:
    def __init__(self, name, condition, action, description=""):
        self.name = name
        self.condition = condition  # function taking a set of facts, returns bool
        self.action = action  # function taking the engine, adds facts
        self.description = description

class Engine:
    def __init__(self):
        self.facts = set()
        self.rules = []
        self.triggered_rules = set()
        self.explanations = []

    def add_fact(self, fact):
        self.facts.add(fact)

    def add_rule(self, rule):
        self.rules.append(rule)

    def run(self):
        changed = True
        while changed:
            changed = False
            for rule in self.rules:
                if rule.name not in self.triggered_rules:
                    if rule.condition(self.facts):
                        rule.action(self)
                        self.triggered_rules.add(rule.name)
                        if rule.description:
                            self.explanations.append(rule.description)
                        changed = True

    def get_recommendations(self):
        return [f.value for f in self.facts if f.key == 'recommend_item_tag']
