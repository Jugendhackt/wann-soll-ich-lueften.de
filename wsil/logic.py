from wsil.waqi_wrapper import get_pollution_data, get_stations_by_name


def analyse_pollution_data(location: str):
    # prevent some sort of input injection
    if "@" in location:
        # TODO: Proper return
        return

    p_data = get_pollution_data(location)
    print(p_data)


if __name__ == "__main__":
    # get_pollution_data("london")
    print(get_stations_by_name("london"))
