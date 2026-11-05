from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0006_workboarditems_acm_prio_alter_workboarditems_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="workboarditems",
            name="sort_order",
            field=models.PositiveIntegerField(default=0),
        ),
    ]
