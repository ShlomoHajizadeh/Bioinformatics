"""
Observables for analysis
"""

def count_alive_targets(targets):
    return sum(t.alive for t in targets.values())