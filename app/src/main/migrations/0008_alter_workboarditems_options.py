from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0007_workboarditems_sort_order"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="workboarditems",
            options={
                "ordering": ["lane", "sort_order", "id"],
                "verbose_name": "Workboard item",
                "verbose_name_plural": "Workboard items",
            },
        ),
    ]
