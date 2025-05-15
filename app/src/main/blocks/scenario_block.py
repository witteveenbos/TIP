from wagtail.blocks import StructBlock, CharBlock, TextBlock, StreamBlock
from .image_chooser_block import ImageChooserBlock


class ScenarioComponent(StructBlock):
    title = CharBlock(required=True)
    description = TextBlock(
        required=True, help_text="Geef meer informatie over het scenario."
    )
    image = ImageChooserBlock(required=True)
    data_link = CharBlock(
        required=True, help_text="Voeg een link toe naar de data van het scenario."
    )


class ScenarioBlock(StructBlock):
    scenarios = StreamBlock(
        [
            ("scenario", ScenarioComponent(required=True)),
        ],
        help_text="Voeg een of meerdere scenario's toe aan de pagina.",
        min_num=1,
    )

    class Meta:
        icon = "image"
        label = "Scenario"
