from loguru import logger

from tools.observability import monitor_exec_time


def parse_data(filename):
    with open(filename) as f:
        return [[int(elem) for elem in line.rstrip().split(" ")] for line in f]


def is_report_safe(report):
    safe = True
    prev_lvl = report[0]
    ascending = report[1] > report[0]
    for level in report[1:]:
        if prev_lvl == level:
            safe = False
            logger.debug(
                f"Report {report} is unsafe: identical consecutive levels - stopping on {level} vs {prev_lvl}"
            )
            break
        if ascending != (level > prev_lvl):
            safe = False
            logger.debug(
                f"Report {report} is unsafe: not strictly ascending/descending - stopping on {level} vs {prev_lvl} - ascending: {ascending}"
            )
            break
        if abs(level - prev_lvl) > 3:
            safe = False
            logger.debug(
                f"Report {report} is unsafe: difference > 3 - stopping on {level} vs {prev_lvl}"
            )
            break
        prev_lvl = level
    if safe:
        logger.debug(f"Report {report} is safe")
    return safe


@monitor_exec_time
def compute_a(reports):
    nb_safe = 0
    for report in reports:
        safe = is_report_safe(report)
        if safe:
            nb_safe += 1
    return nb_safe


@monitor_exec_time
def compute_b(reports):
    nb_safe = 0
    for report in reports:
        if is_report_safe(report):
            nb_safe += 1
            continue
        for i in range(len(report)):
            if is_report_safe(report[:i] + report[i + 1 :]):
                nb_safe += 1
                break
    return nb_safe


if __name__ == "__main__":
    reports_sample = parse_data("data/day2-sample")
    assert compute_a(reports_sample) == 2
    reports = parse_data("data/day2")
    logger.info(f"Day 2a > {compute_a(reports)}")
    assert compute_b(reports_sample) == 4
    logger.info(f"Day 2b > {compute_b(reports)}")
