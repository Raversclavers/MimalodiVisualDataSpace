from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0009_alter_blogpost_options_alter_tutorial_options"),
    ]

    operations = [
        migrations.CreateModel(
            name="CaseStudy",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200)),
                ("slug", models.SlugField(unique=True)),
                ("category", models.CharField(max_length=120)),
                ("accent", models.CharField(blank=True, max_length=120)),
                ("client_name", models.CharField(blank=True, max_length=160)),
                ("industry", models.CharField(blank=True, max_length=120)),
                ("summary", models.TextField()),
                ("client_context", models.TextField()),
                ("challenge", models.TextField()),
                ("approach", models.TextField()),
                ("solution", models.TextField()),
                ("tools_used", models.TextField(help_text="Comma-separated tools or capabilities used on the project.")),
                ("result", models.TextField()),
                ("featured_on_homepage", models.BooleanField(default=True)),
                ("is_published", models.BooleanField(default=True)),
                ("featured_order", models.PositiveSmallIntegerField(default=0)),
                ("hero_image", models.ImageField(blank=True, null=True, upload_to="case-studies/")),
                ("hero_image_path", models.CharField(blank=True, max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["featured_order", "title"]},
        ),
        migrations.CreateModel(
            name="CaseStudyMetric",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("label", models.CharField(max_length=120)),
                ("value", models.CharField(max_length=120)),
                ("sort_order", models.PositiveSmallIntegerField(default=0)),
                ("case_study", models.ForeignKey(on_delete=models.deletion.CASCADE, related_name="metrics", to="core.casestudy")),
            ],
            options={"ordering": ["sort_order", "id"]},
        ),
        migrations.CreateModel(
            name="CaseStudyScreenshot",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=160)),
                ("caption", models.TextField(blank=True)),
                ("image", models.ImageField(blank=True, null=True, upload_to="case-studies/")),
                ("image_path", models.CharField(blank=True, max_length=255)),
                ("sort_order", models.PositiveSmallIntegerField(default=0)),
                ("case_study", models.ForeignKey(on_delete=models.deletion.CASCADE, related_name="screenshots", to="core.casestudy")),
            ],
            options={"ordering": ["sort_order", "id"]},
        ),
    ]