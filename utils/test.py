adj_value = {
    "stop_x": 52,
    "stop_y": 0.1,
    "feed_x": 45,
    "feed_y": -20,
}

print(
    adj_value
    == {
        "stop_x": 52,
        "stop_y": 0,
        "feed_x": 45,
        "feed_y": -20,
    }
)
