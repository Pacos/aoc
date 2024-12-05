from dataclasses import dataclass, field

from loguru import logger

from tools.observability import monitor_exec_time

@dataclass
class ManualUpdates:
    constraints: list[tuple] = field(default_factory=list)
    updates: list[list[str]] = field(default_factory=list)


def find_order_from_constraints(constraints: list[tuple], input_pages: list[str]) -> dict[str, int]:
    constraints = [c for c in constraints if c[0] in input_pages and c[1] in input_pages]
    pages = set([c for tpl in constraints for c in tpl])
    nb_pages = len(pages)
    order = {page: 0 for page in pages}
    befores = set([c[0] for c in constraints])
    afters = set([c[1] for c in constraints])
    idx = 1
    while pages:
        last = pages.difference(befores).pop()
        first = pages.difference(afters).pop()
        order[last] = nb_pages - idx + 1
        order[first] = idx
        constraints = [c for c in constraints if c[0] != first and c[1] != last]
        pages = set([c for tpl in constraints for c in tpl])
        befores = set([c[0] for c in constraints])
        afters = set([c[1] for c in constraints])
        idx += 1
    for k,v in order.items():
        if v == 0:
            order[k] = int((nb_pages + 1)/2)
    return order

@monitor_exec_time
def compute_a(manual: ManualUpdates):
    result = 0
    for pages in manual.updates:
        order = find_order_from_constraints(manual.constraints, pages)
        sorted_pages = sorted(pages, key=lambda u : order.get(u))
        if sorted_pages == pages:
            result += int(pages[int((len(pages) - 1)/2)])
    return result

@monitor_exec_time
def compute_b(manual: ManualUpdates):
    result = 0
    for pages in manual.updates:
        order = find_order_from_constraints(manual.constraints, pages)
        sorted_pages = sorted(pages, key=lambda u : order.get(u))
        if sorted_pages != pages:
            result += int(sorted_pages[int((len(sorted_pages) - 1)/2)])
    return result

def parse_data(filename):
    manual = ManualUpdates()
    with open(filename) as f:
        for line in f:
            if "|" in line:
                manual.constraints.append((line.rstrip().split("|")[0], line.rstrip().split("|")[1]))
            if "," in line:
                manual.updates.append(line.rstrip().split(","))
    return manual

if __name__ == "__main__":
    manual_sample = parse_data("data/day5-sample")
    assert compute_a(manual_sample) == 143
    assert compute_b(manual_sample) == 123

    manual = parse_data("data/day5")
    logger.info(f"Day 5a > {compute_a(manual)}")
    logger.info(f"Day 5b > {compute_b(manual)}")


