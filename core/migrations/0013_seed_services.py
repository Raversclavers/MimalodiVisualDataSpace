from django.db import migrations


def seed_services(apps, schema_editor):
    Service = apps.get_model("core", "Service")
    ServiceDeliverable = apps.get_model("core", "ServiceDeliverable")

    if Service.objects.exists():
        return

    services = [
        {
            "title": "Executive Dashboard Design",
            "slug": "executive-dashboard-design",
            "icon": "fas fa-tachometer-alt",
            "short_description": "Decision-grade dashboards built for leadership teams that need performance visibility without the noise.",
            "hero_headline": "Dashboards that leadership teams actually use to make decisions.",
            "overview": "I design and build dashboards that consolidate scattered metrics into a single, clear view of business performance. The focus is on what leaders need to see, how they review it, and what action it should trigger — not on cramming every data point into one screen.",
            "ideal_client": "Founder-led teams, operations leaders, or department heads who need a reliable performance view that works for weekly reviews, board updates, or cross-functional alignment.",
            "business_value": "A well-structured dashboard replaces hours of spreadsheet work, reduces misalignment between teams, and gives leadership a faster path from question to decision.",
            "process_summary": "Discovery starts with understanding the review cadence, audience, and decisions the dashboard needs to support. From there I define KPI structure, design the layout, and deliver a working prototype ready for review and iteration.",
            "inquiry_subject": "Dashboard design inquiry",
            "seo_title": "Executive Dashboard Design | Mimalodi Visual Data Space",
            "seo_description": "Custom dashboards designed for leadership teams — built around decisions, not decoration.",
            "featured_on_homepage": True,
            "featured_order": 1,
            "deliverables": [
                ("KPI framework document", "A structured map of the metrics that matter, how they connect, and which decisions they support."),
                ("Dashboard prototype", "A working dashboard layout designed for your review cadence and stakeholder audience."),
                ("Stakeholder walkthrough", "A guided review session to validate the design before handoff or deployment."),
                ("Iteration round", "One round of structured revisions based on stakeholder feedback."),
            ],
        },
        {
            "title": "Reporting Systems & KPI Design",
            "slug": "reporting-systems-kpi-design",
            "icon": "fas fa-chart-bar",
            "short_description": "Structured reporting workflows that turn scattered metrics into consistent, trustworthy business updates.",
            "hero_headline": "Reporting that reads fast, updates reliably, and supports real conversations.",
            "overview": "I help teams move from ad-hoc number-pulling to structured reporting systems. That means defining what gets measured, how it gets communicated, and building repeatable formats that stakeholders can rely on without chasing analysts for context.",
            "ideal_client": "Teams that send regular reports to clients, leadership, or investors and want those reports to feel more credible, easier to produce, and clearer to interpret.",
            "business_value": "A structured reporting system reduces time spent on manual updates, improves consistency across review cycles, and builds confidence in the numbers being shared.",
            "process_summary": "I start by auditing the current reporting workflow — what data exists, who receives it, and where friction or confusion shows up. Then I design a reporting structure with consistent formats, clearer KPI framing, and a delivery rhythm that matches the business cadence.",
            "inquiry_subject": "Reporting systems inquiry",
            "seo_title": "Reporting Systems & KPI Design | Mimalodi Visual Data Space",
            "seo_description": "Structured reporting workflows designed for consistency, clarity, and faster stakeholder communication.",
            "featured_on_homepage": True,
            "featured_order": 2,
            "deliverables": [
                ("Reporting audit summary", "A review of the current state — what works, what causes friction, and what to fix first."),
                ("KPI structure & definitions", "Clear metric definitions with ownership, cadence, and communication guidance."),
                ("Report template design", "A repeatable reporting format built for your audience and review rhythm."),
                ("Delivery workflow guide", "A short operational guide for producing and distributing reports consistently."),
            ],
        },
        {
            "title": "Data Storytelling & Visual Communication",
            "slug": "data-storytelling-visual-communication",
            "icon": "fas fa-pen-nib",
            "short_description": "Polished visual narratives that translate complex analysis into insight stakeholders can act on.",
            "hero_headline": "Turn analysis into a visual story that lands with decision-makers.",
            "overview": "Not all insight needs a dashboard. Sometimes the most effective delivery is a visual narrative — a structured story that walks stakeholders through the data, highlights what matters, and frames the recommended action. I design these for presentations, investor updates, board decks, and client-facing communication.",
            "ideal_client": "Consultants, analysts, and leaders who need to present data findings in a way that is persuasive, clear, and polished enough for high-visibility settings.",
            "business_value": "A strong data story gets buy-in faster, makes complex findings accessible to non-technical audiences, and raises the perceived quality of your analytical work.",
            "process_summary": "I work from your raw analysis or findings, identify the core narrative arc, and design a visual flow that moves from context to insight to recommendation. The output is presentation-ready and designed to hold up under scrutiny.",
            "inquiry_subject": "Data storytelling inquiry",
            "seo_title": "Data Storytelling & Visual Communication | Mimalodi Visual Data Space",
            "seo_description": "Visual data narratives designed for presentations, decks, and stakeholder communication.",
            "featured_on_homepage": True,
            "featured_order": 3,
            "deliverables": [
                ("Narrative outline", "The core story arc mapped before any design work begins — ensuring the message is right."),
                ("Visual insight deck", "A polished presentation with annotated charts, clear framing, and a decision-ready conclusion."),
                ("Chart design & annotation", "Custom chart designs with explanatory annotations that guide the reader through the data."),
                ("Executive summary slide", "A standalone summary slide suitable for board decks or quick stakeholder communication."),
            ],
        },
        {
            "title": "Analytics Consulting & Strategy",
            "slug": "analytics-consulting-strategy",
            "icon": "fas fa-compass",
            "short_description": "Advisory sessions to help teams clarify what to measure, how to structure data work, and where to invest first.",
            "hero_headline": "Get clearer on what your data should actually be doing for the business.",
            "overview": "Sometimes the problem is not a missing dashboard — it is unclear thinking about what data work should accomplish. I offer consulting sessions to help teams define their analytics priorities, evaluate their current data maturity, and build a practical roadmap for improvement without over-investing in tools or infrastructure.",
            "ideal_client": "Early-stage teams, founders, or department leads who know they need to be more data-driven but are not sure where to start or what to prioritize.",
            "business_value": "A focused strategy session saves months of trial-and-error by identifying the highest-value data work first and creating a realistic plan that matches your team capacity and budget.",
            "process_summary": "I run a structured discovery session to understand your business model, current data landscape, team capacity, and decision-making needs. The output is a prioritized recommendations document with concrete next steps — not a vague roadmap.",
            "inquiry_subject": "Analytics consulting inquiry",
            "seo_title": "Analytics Consulting & Strategy | Mimalodi Visual Data Space",
            "seo_description": "Advisory support to help teams prioritize data work, define KPIs, and build a practical analytics roadmap.",
            "featured_on_homepage": True,
            "featured_order": 4,
            "deliverables": [
                ("Discovery session", "A structured 60-90 minute working session to understand and map your current data landscape."),
                ("Prioritized recommendations", "A clear document outlining what to focus on first, what to defer, and why."),
                ("Analytics roadmap", "A phased plan aligned to your team capacity, budget, and business goals."),
                ("Follow-up review", "A check-in session to assess progress and adjust priorities based on new information."),
            ],
        },
    ]

    for service_data in services:
        deliverables = service_data.pop("deliverables")
        service = Service.objects.create(**service_data)
        for sort_order, (title, description) in enumerate(deliverables):
            ServiceDeliverable.objects.create(
                service=service,
                title=title,
                description=description,
                sort_order=sort_order,
            )


def reverse_services(apps, schema_editor):
    Service = apps.get_model("core", "Service")
    Service.objects.filter(
        slug__in=[
            "executive-dashboard-design",
            "reporting-systems-kpi-design",
            "data-storytelling-visual-communication",
            "analytics-consulting-strategy",
        ]
    ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0012_service_models"),
    ]

    operations = [
        migrations.RunPython(seed_services, reverse_services),
    ]
