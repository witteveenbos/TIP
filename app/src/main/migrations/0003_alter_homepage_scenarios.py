from django.db import migrations
import main.blocks.image_chooser_block
import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0002_homepage_scenarios"),
    ]

    operations = [
        migrations.AlterField(
            model_name="homepage",
            name="scenarios",
            field=wagtail.fields.StreamField(
                [
                    (
                        "scenario",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "scenarios",
                                    wagtail.blocks.StreamBlock(
                                        [
                                            (
                                                "scenario",
                                                wagtail.blocks.StructBlock(
                                                    [
                                                        (
                                                            "title",
                                                            wagtail.blocks.CharBlock(
                                                                required=True
                                                            ),
                                                        ),
                                                        (
                                                            "description",
                                                            wagtail.blocks.TextBlock(
                                                                help_text="Geef meer informatie over het scenario.",
                                                                required=True,
                                                            ),
                                                        ),
                                                        (
                                                            "image",
                                                            main.blocks.image_chooser_block.ImageChooserBlock(
                                                                required=True
                                                            ),
                                                        ),
                                                        (
                                                            "data_link",
                                                            wagtail.blocks.CharBlock(
                                                                help_text="Voeg een link toe naar de data van het scenario.",
                                                                required=True,
                                                            ),
                                                        ),
                                                    ],
                                                    required=True,
                                                ),
                                            )
                                        ],
                                        help_text="Voeg een of meerdere scenario's toe aan de pagina.",
                                        min_num=1,
                                    ),
                                )
                            ]
                        ),
                    )
                ],
                blank=True,
                null=True,
                use_json_field=True,
                verbose_name="Scenarios",
            ),
        ),
    ]
