from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0011_seed_case_studies"),
    ]

    operations = [
        migrations.CreateModel(
            name="Service",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200)),
                ("slug", models.SlugField(unique=True)),
                ("icon", models.CharField(default="fas fa-chart-line", max_length=80)),
                ("short_description", models.TextField(help_text="Short summary used on cards, previews, and SEO-heavy sections.")),
                ("hero_headline", models.CharField(blank=True, max_length=220)),
                ("overview", models.TextField()),
                ("ideal_client", models.TextField()),
                ("business_value", models.TextField()),
                ("process_summary", models.TextField()),
                ("inquiry_subject", models.CharField(blank=True, max_length=160)),
                ("seo_title", models.CharField(blank=True, max_length=70)),
                ("seo_description", models.CharField(blank=True, max_length=160)),
                ("featured_on_homepage", models.BooleanField(default=True)),
                ("is_published", models.BooleanField(default=True)),
                ("featured_order", models.PositiveSmallIntegerField(default=0)),
                ("hero_image", models.ImageField(blank=True, null=True, upload_to="services/")),
                ("hero_image_path", models.CharField(blank=True, max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "case_studies",
                    models.ManyToManyField(blank=True, related_name="related_services", to="core.casestudy"),
                ),
            ],
            options={
                "ordering": ["featured_order", "title"],
            },
        ),
        migrations.CreateModel(
            name="ServiceDeliverable",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=120)),
                ("description", models.TextField(blank=True)),
                ("sort_order", models.PositiveSmallIntegerField(default=0)),
                (
                    "service",
                    models.ForeignKey(on_delete=models.deletion.CASCADE, related_name="deliverables", to="core.service"),
                ),
            ],
            options={
                "ordering": ["sort_order", "id"],
            },
        ),
    ]