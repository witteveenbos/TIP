from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0004_workboardpage_workboarditems_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="workboarditems",
            name="type",
            field=models.CharField(
                choices=[
                    ("Woningbouw", "Woningbouw"),
                    ("Laadinfra", "Laadinfra"),
                    (
                        "Bedrijventerrein / logistiek",
                        "Bedrijventerrein / logistiek",
                    ),
                    ("Zon", "Zon"),
                ],
                default="Woningbouw",
                max_length=32,
            ),
        ),
        migrations.AddField(
            model_name="workboarditems",
            name="size_mw",
            field=models.IntegerField("Size (MW)", default=0),
        ),
        migrations.AddField(
            model_name="workboarditems",
            name="status",
            field=models.IntegerField(
                choices=[
                    (1, "Idee"),
                    (2, "Beleidsvoornemen"),
                    (3, "Planvorming"),
                    (4, "Besluitvorming loopt vast"),
                    (5, "Vastgesteld / in uitvoering"),
                ],
                default=1,
            ),
        ),
    ]