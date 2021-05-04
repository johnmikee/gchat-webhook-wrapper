from json import dumps
from httplib2 import Http

"""
This needs work on checking the validity of arguements passed.
Google is special on what can be passed to sub dicts.
Documentation at 
    Cards - https://developers.google.com/hangouts/chat/reference/message-formats/cards
    Simple - https://developers.google.com/hangouts/chat/reference/message-formats/basic
"""

WEBHOOKURL = ""

class GAlert:
    def __init__(
        self,
        base_card={"cards": [{"header": "", "sections": []}]},
        url=WEBHOOKURL,
    ):
        self.base_card = base_card
        self.message_headers = {"Content-Type": "application/json; charset=UTF-8"}
        self.url = url

    def _stringer(self, input):
        """
        all items passed must be strings or Google explodes.
        """
        if isinstance(input, str):
            return input
        else:
            return str(input)
        
    def _updater(self, arg, opts, **kwargs):
        base = {arg: {}}

        for k, v in kwargs.items():
            k = self._stringer(k)
            v = self._stringer(v)
            if k in opts.keys():
                opts[k] = v

        # convert to list to avoid RunTimeError for removing an item in the
        # list while iterating over it
        for item in list(opts.keys()):
            if not kwargs.get(item):
                opts.pop(item)

        base[arg] = opts

        return base

    def headers(self, **kwargs):
        """
        A card may have a single header structure, which can contain the following attributes:
        "title": "Pizza Bot Customer Support",
        "subtitle": "pizzabot@example.com",
        "imageUrl": "https://goo.gl/aeDtrS",
        "imageStyle": "IMAGE"
        """
        opts = {"title": "", "subtitle": "", "imageUrl": "", "imageStyle": ""}

        return self._updater("header", opts, **kwargs)

    def sections_widgets(self, widgets):
        """
        widgets arguement is a list of dicts

        A card must contain one or more sections, which are displayed in a vertical layout inside the card.
        Sections are separated by a line and contain one or more widgets.
        A section will look like the following in JSON form:
        "sections": [
                        {
                        "widgets": [
                                        { ... },
                                        { ... }
                        ]
                        },
        """
        base = {"sections": [{"widgets": []}]}

        for w in widgets:
            base["sections"][0]["widgets"].append(w)

        return base

    def text_paragraph(self, text):
        """
        A TextParagraph widget displays one or more lines of text, which may contain HTML tags as described in Card Text Formatting.
        Example:
        {
                        "textParagraph": {
                        "text": "<b>Roses</b> are <font color=\"#ff0000\">red</font>,<br><i>Violets</i> are <font color=\"#0000ff\">blue</font>"
        }
        """

        return {"textParagraph": {"text": text}}

    def key_value(self, **kwargs):
        """
        A KeyValue widget displays a topLabel, content, and a bottomLabel.
        You can attach an onClick event to the keyValue, making the topLabel, content, and bottomLabel into clickable regions.
        Set contentMultiline to true to allow content to span multiple lines.
        A KeyValue can also optionally have a built-in icon, a custom icon, or a button associated with it.
        ex:
                        "keyValue": {
                                        "topLabel": "Order No.",
                                        "content": "12345",
                                        "contentMultiline": "false",
                                        "bottomLabel": "Delayed",
                                        "onClick": {
                                                                        "openLink": {
                                                                        "url": "https://example.com/"
                                                                        }
                                                        },
                                        "icon": "TRAIN",
                                        "button": {
                                                        "textButton": {
                                                                        "text": "VISIT WEBSITE",
                                                                        "onClick": {
                                                                                        "openLink": {
                                                                                                        "url": "http://site.com"
                                                                                        }
                                                                        }
                                                                        }
                                                        }
                                        }
        """
        opts = {
            "topLabel": "",
            "content": "",
            "bottomLabel": "",
            "icon": "",
            "button": "",
        }

        return self._updater("keyValue", opts, **kwargs)

    def image(self, **kwargs):
        """
        An Image widget displays a full-width image from a custom URL. Example:
        {
                        "image": {
                        "imageUrl": "https://example.com/kitten.png",
                        "onClick": {
                                        "openLink": {
                                        "url": "https://example.com/"
                                        }
                        }
                        }
        }
        """
        opts = {"imageUrl": "", "onClick": ""}

        return self._updater("image", opts, **kwargs)

    def button(self, button_type, **kwargs):
        """
        button_type can be:
            imageButton
            textButton

        A widget may also contain one or more buttons. Buttons in the same widget will be laid out horizontally.
        Buttons are mutually exclusive with other UI elements in a widget;
        it is an error to specify another UI element alongside buttons in the same widget.
        There are two types of buttons: ImageButton and TextButton.
        An ImageButton may specify either a built-in icon (see Built-in Icons section below) or a custom image URL.
        A button can specify a URL that will be opened when a user clicks on it, or an action to be handled by the bot's CARD_CLICKED event handler, as shown in Creating interactive cards.
        Example:
        https://developers.google.com/hangouts/chat/reference/message-formats/cards#buttons


        """
        opts = {
            "iconUrl": "",
            "onClick": {"action": "", "openLink": "", "text": "Snooze 1 day"},
            "icon": "",
        }

        button_base = {"buttons": []}
        if button_type == "imageButton":
            image = self._updater("imageButton", opts, **kwargs)
            button_base["buttons"] = [image]
            return button_base

        elif button_type == "textButton":
            image = self._updater("textButton", opts, **kwargs)
            button_base["buttons"] = [image]
            return button_base

    def simple(self, text):
        """
        for simple one line cards
        """
        return {"text": text}

    def build_alert(self, headers, sections):
        """
        card_props should be a list of dicts.
        """
        base = self.base_card

        if headers:
            base["cards"][0]["header"] = headers["header"]
        else:
            del base["cards"][0]["header"]

        if sections:
            base["cards"][0]["sections"] = sections["sections"]
        else:
            del base["cards"][0]["sections"]

        return base

    def send_alert(self, message):
        http_obj = Http()

        response = http_obj.request(
            uri=self.url,
            method="POST",
            headers=self.message_headers,
            body=dumps(message),
        )

        if int(response[0]["status"]) != 200:
            raise ValueError(
                "Request to Google Chat returned an error, the response is:\n%s"
                % response,
            )
