from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0008_contactsubmission"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="blogpost",
            options={"ordering": ["-created_at"]},
        ),
        migrations.AlterModelOptions(
            name="tutorial",
            options={"ordering": ["-created_at"]},
        ),
    ]