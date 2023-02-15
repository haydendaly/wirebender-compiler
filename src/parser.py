# todo use formal parser with BNF
def parse(str):
    return [["var", "num_times", 10], ["var", "bend_angle", ["/", 360, "num_times"]], ["repeat", "num_times", [["feed", 2], ["bend", "bend_angle"]], ["feed", 10]]]