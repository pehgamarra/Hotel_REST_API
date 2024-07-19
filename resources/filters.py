

def normalize_path_params(city=None, star_min=0, star_max=5, daily_min=0, daily_max=10000, limit=50, offset=0, **data):
    if city:
        return {
            'star_min': star_min,
            'star_max': star_max,
            'daily_min': daily_min,
            'daily_max': daily_max,
            'city': city,
            'limit': limit,
            'offset': offset
        }
    return {
        'star_min': star_min,
        'star_max': star_max,
        'daily_min': daily_min,
        'daily_max': daily_max,
        'limit': limit,
        'offset': offset
    }


not_city_search = "SELECT * FROM hotels \
            WHERE (star >= ? and star <= ?) \
            and (daily >= ? and daily <= ?) \
            LIMIT ? OFFSET ?"

with_city_search = "SELECT * FROM hotels \
            WHERE (star >= ? and star <= ?) \
            and (daily >= ? and daily <= ?) \
            and city = ? LIMIT ? OFFSET ?"