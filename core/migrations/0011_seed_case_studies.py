from django.db import migrations


def seed_case_studies(apps, schema_editor):
    CaseStudy = apps.get_model("core", "CaseStudy")
    CaseStudyMetric = apps.get_model("core", "CaseStudyMetric")
    CaseStudyScreenshot = apps.get_model("core", "CaseStudyScreenshot")

    if CaseStudy.objects.exists():
        return

    studies = [
        {
            "title": "Executive KPI Command Center",
            "slug": "executive-kpi-command-center",
            "category": "Dashboard strategy",
            "accent": "Leadership reporting",
            "client_name": "Growth-stage leadership team",
            "industry": "Operations and revenue management",
            "summary": "A leadership dashboard concept designed to consolidate performance, reduce reporting friction, and create faster alignment around weekly priorities.",
            "client_context": "A growing leadership team needed one source of truth for revenue, operations, and customer performance without relying on spreadsheet handoffs.",
            "challenge": "The reporting process was fragmented, slow to update, and difficult to interpret across functions. Leaders needed clearer visibility and a more consistent review rhythm.",
            "approach": "Defined a tighter KPI structure, prioritized cross-functional metrics, and designed a dashboard flow that moved from executive summary to decision-focused detail.",
            "solution": "Created a premium dashboard concept with role-aware KPI blocks, trend views, and commentary space to support weekly executive review conversations.",
            "tools_used": "Django, Python, Pandas, Plotly, KPI design, Executive reporting",
            "result": "The outcome was a clearer performance command center concept that helps leaders spot movement faster, align teams around the same metrics, and reduce reporting friction.",
            "featured_order": 1,
            "hero_image_path": "images/multiplot.jpg",
            "metrics": [("Review cadence", "Weekly"), ("KPI groups", "4 aligned views"), ("Primary goal", "Faster executive decisions")],
            "screenshots": [
                ("Executive summary layout", "A top-level dashboard composition designed for weekly performance reviews.", "images/multiplot.jpg"),
                ("Trend and variance view", "A supporting view that highlights movement over time and exceptions that need action.", "images/line graph.jpg"),
            ],
        },
        {
            "title": "Monthly Insights Pack for Client Services",
            "slug": "monthly-insights-pack-client-services",
            "category": "Reporting system",
            "accent": "Client reporting",
            "client_name": "Service business account team",
            "industry": "Client services",
            "summary": "A polished reporting pack concept for teams that need client-ready analytics without overwhelming the audience with technical detail.",
            "client_context": "A service business needed client-facing monthly reports that looked credible, explained performance clearly, and made renewal conversations easier.",
            "challenge": "The existing reports were metric-heavy but insight-light. Clients could see numbers, but not the narrative behind results or what actions were recommended.",
            "approach": "Reframed raw metrics into a structured insights pack with trend summaries, performance highlights, and visual callouts built for non-technical stakeholders.",
            "solution": "Designed a repeatable monthly reporting format with visual hierarchy, commentary blocks, and cleaner summaries for account teams to present with confidence.",
            "tools_used": "Data analysis, Narrative reporting, Visualization design, Client communications, Performance storytelling",
            "result": "The reporting system becomes easier to deliver, easier for clients to understand, and better suited to strategic conversations around results and next steps.",
            "featured_order": 2,
            "hero_image_path": "images/data.jpg",
            "metrics": [("Report format", "Monthly insight pack"), ("Audience", "Clients and account teams"), ("Primary benefit", "Clearer retention conversations")],
            "screenshots": [
                ("Summary page concept", "A concise opening report page that highlights changes, wins, and focus areas.", "images/data.jpg"),
                ("Performance callout section", "A visual layout that turns recurring metrics into a strategic update.", "images/static house.jpg"),
            ],
        },
        {
            "title": "Board-Ready Performance Storytelling",
            "slug": "board-ready-performance-storytelling",
            "category": "Visual insight design",
            "accent": "Stakeholder communication",
            "client_name": "Founder and stakeholder team",
            "industry": "Strategy and performance communication",
            "summary": "A visual storytelling concept built for high-stakes reporting where growth, risk, and priorities need to be communicated with confidence.",
            "client_context": "A founder preparing for stakeholder discussions needed to explain growth, risk, and operational priorities with confidence.",
            "challenge": "There was too much raw information and not enough presentation logic. The audience needed a clear narrative, not a stack of disconnected charts.",
            "approach": "Built a visual storytelling structure that distilled complex metrics into a concise sequence of charts, annotations, and action-oriented commentary.",
            "solution": "Developed a board-ready layout that balanced performance highlights, strategic context, and visual emphasis for easier stakeholder interpretation.",
            "tools_used": "Performance analysis, Slide-ready visuals, Trend interpretation, Decision support, Executive communication",
            "result": "The final concept gives decision-makers a sharper understanding of what changed, why it matters, and what should happen next.",
            "featured_order": 3,
            "hero_image_path": "images/line graph.jpg",
            "metrics": [("Presentation mode", "Board and stakeholder review"), ("Narrative sections", "3 focused chapters"), ("Primary outcome", "Higher-confidence communication")],
            "screenshots": [
                ("Performance narrative opener", "An opening visual sequence designed to establish the key performance story quickly.", "images/line graph.jpg"),
                ("Priority action slide", "A visual format for connecting performance trends to next-step recommendations.", "images/multiplot.jpg"),
            ],
        },
    ]

    for study_data in studies:
        metrics = study_data.pop("metrics")
        screenshots = study_data.pop("screenshots")
        case_study = CaseStudy.objects.create(**study_data)
        for index, (label, value) in enumerate(metrics, start=1):
            CaseStudyMetric.objects.create(case_study=case_study, label=label, value=value, sort_order=index)
        for index, (title, caption, image_path) in enumerate(screenshots, start=1):
            CaseStudyScreenshot.objects.create(
                case_study=case_study,
                title=title,
                caption=caption,
                image_path=image_path,
                sort_order=index,
            )


def remove_seed_case_studies(apps, schema_editor):
    CaseStudy = apps.get_model("core", "CaseStudy")
    CaseStudy.objects.filter(
        slug__in=[
            "executive-kpi-command-center",
            "monthly-insights-pack-client-services",
            "board-ready-performance-storytelling",
        ]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0010_case_study_models"),
    ]

    operations = [
        migrations.RunPython(seed_case_studies, remove_seed_case_studies),
    ]