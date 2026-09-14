from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0009_loginpage"),
    ]

    operations = [
        migrations.AddField(
            model_name="workboarditemmodification",
            name="change_type",
            field=models.CharField(
                choices=[("lane", "Lane"), ("properties", "Properties")],
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="workboarditemmodification",
            name="changed_fields",
            field=models.JSONField(default=list),
        ),
    ]
