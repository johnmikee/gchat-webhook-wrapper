# gchat-webhook-wrapper
Small Class to wrap the Google Chat Webhook functionality 


Example Card usage:
ga = GAlert()
headers = ga.headers(
    title="Pizza Bot Customer Support",
    subtitle="pizzabot@example.com",
    imageUrl="https://i.imgur.com/FiNj8.jpg",
)
button = ga.button(
    "imageButton",
    iconUrl="https://i.imgur.com/FiNj8.jpg",
    onClick={"openLink": {"url": "https://i.imgur.com/FiNj8.jpg"}},
)
sections = ga.sections_widgets(
    [
        button,
        ga.key_value(topLabel="Version", content="version"),
        ga.key_value(topLabel="Testing", content="test"),
    ]
)
message = ga.build_alert(headers=headers, sections=sections)
ga.send_alert(message)

Example Simple usage:
ga = GAlert()
message = ga.simple("hello")
ga.send_alert(message)
