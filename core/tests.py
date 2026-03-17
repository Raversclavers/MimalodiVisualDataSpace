from django.test import TestCase, override_settings
from django.urls import reverse

from .models import (
	BlogPost,
	CaseStudy,
	CaseStudyMetric,
	CaseStudyScreenshot,
	ContactSubmission,
	Service,
	ServiceDeliverable,
	Tutorial,
)


@override_settings(SECURE_SSL_REDIRECT=False)
class CorePageTests(TestCase):
	@classmethod
	def setUpTestData(cls):
		cls.post = BlogPost.objects.create(
			title="Launch-ready storytelling",
			slug="launch-ready-storytelling",
			content="This is a sample post for route and template validation.",
		)
		Tutorial.objects.create(
			title="Intro tutorial",
			content="A short tutorial entry used to validate the tutorials page.",
		)
		cls.case_study = CaseStudy.objects.create(
			title="Portfolio test case",
			slug="portfolio-test-case",
			category="Dashboard strategy",
			accent="Testing",
			client_name="Example client",
			industry="Analytics",
			summary="A test case study used to verify the portfolio detail flow.",
			client_context="An example client needed clearer reporting.",
			challenge="The reporting workflow was fragmented.",
			approach="Structured the data story and dashboard flow.",
			solution="Created a cleaner reporting experience.",
			tools_used="Django, Python, Plotly",
			result="Improved clarity for reviewers.",
			featured_order=99,
			hero_image_path="images/multiplot.jpg",
		)
		CaseStudyMetric.objects.create(case_study=cls.case_study, label="Outcome", value="Clearer reporting", sort_order=1)
		CaseStudyScreenshot.objects.create(
			case_study=cls.case_study,
			title="Test screenshot",
			caption="A sample screenshot for the detail page.",
			image_path="images/data.jpg",
			sort_order=1,
		)
		cls.service = Service.objects.create(
			title="Dashboard Design",
			slug="dashboard-design",
			icon="fas fa-chart-line",
			short_description="Design dashboards that make recurring performance reviews easier to understand and act on.",
			hero_headline="Dashboard design for clearer recurring reporting",
			overview="This service helps teams structure dashboards around the metrics and questions that actually matter in reviews.",
			ideal_client="Founders, managers, and teams that need cleaner monitoring views.",
			business_value="Improves visibility and reduces confusion during reporting cycles.",
			process_summary="Start by clarifying metrics and audience, then structure the layout and narrative flow.",
			inquiry_subject="Dashboard design inquiry",
			seo_title="Dashboard Design Services | MVDS",
			seo_description="Dashboard design support for clearer KPI reporting and stakeholder alignment.",
			featured_order=1,
		)
		cls.service.case_studies.add(cls.case_study)
		ServiceDeliverable.objects.create(
			service=cls.service,
			title="Dashboard concept",
			description="A KPI layout designed for recurring decision reviews.",
			sort_order=1,
		)

	def test_public_pages_load(self):
		urls = [
			reverse("home"),
			reverse("about"),
			reverse("services"),
			reverse("service_detail", kwargs={"slug": self.service.slug}),
			reverse("contact"),
			reverse("signup"),
			reverse("login"),
			reverse("blog_list"),
			reverse("portfolio"),
			reverse("portfolio_detail", kwargs={"slug": self.case_study.slug}),
			reverse("tutorials"),
			reverse("analytics"),
			reverse("visualizations"),
		]

		for url in urls:
			with self.subTest(url=url):
				response = self.client.get(url, follow=True)
				self.assertEqual(response.status_code, 200)

	def test_blog_detail_uses_slug_route(self):
		response = self.client.get(reverse("blog_detail", kwargs={"slug": self.post.slug}), follow=True)

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, self.post.title)

	def test_portfolio_detail_renders_case_study_content(self):
		response = self.client.get(reverse("portfolio_detail", kwargs={"slug": self.case_study.slug}), follow=True)

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, self.case_study.title)
		self.assertContains(response, "Clearer reporting")

	def test_service_detail_renders_deliverables(self):
		response = self.client.get(reverse("service_detail", kwargs={"slug": self.service.slug}), follow=True)

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, self.service.title)
		self.assertContains(response, "Dashboard concept")

	def test_contact_page_prefills_subject_for_service_queries(self):
		response = self.client.get(f"{reverse('contact')}?service={self.service.slug}", follow=True)

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Dashboard design inquiry")

	def test_contact_submission_is_saved(self):
		response = self.client.post(
			reverse("contact"),
			{
				"name": "Marlo Data",
				"email": "marlo@example.com",
				"subject": "Dashboard redesign",
				"message": "I need help creating a cleaner reporting dashboard for internal leadership reviews.",
			},
			follow=True,
		)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(ContactSubmission.objects.count(), 1)
		self.assertContains(response, "Your inquiry has been received")

	def test_contact_submission_validation_errors(self):
		response = self.client.post(
			reverse("contact"),
			{
				"name": "A",
				"email": "not-an-email",
				"subject": "Hi",
				"message": "Too short",
			},
			follow=True,
		)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(ContactSubmission.objects.count(), 0)
		self.assertContains(response, "Please review the form and correct the highlighted fields.")
