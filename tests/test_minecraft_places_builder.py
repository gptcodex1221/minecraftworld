from minecraft_places_builder import GoogleMapsParseError, parse_google_maps_url


def test_parse_at_pattern() -> None:
    lat, lon = parse_google_maps_url("https://www.google.com/maps/@48.85837,2.294481,17z")
    assert lat == 48.85837
    assert lon == 2.294481


def test_parse_query_pattern() -> None:
    lat, lon = parse_google_maps_url("https://www.google.com/maps/search/?api=1&query=55.7558,37.6176")
    assert lat == 55.7558
    assert lon == 37.6176


def test_parse_plain_coords() -> None:
    lat, lon = parse_google_maps_url("40.6892,-74.0445")
    assert lat == 40.6892
    assert lon == -74.0445


def test_parse_invalid() -> None:
    try:
        parse_google_maps_url("https://www.google.com/maps/place/Paris")
    except GoogleMapsParseError:
        return
    raise AssertionError("Expected GoogleMapsParseError")
