from django.contrib.auth.models import AnonymousUser, User
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory, TestCase
from django.urls import resolve, reverse

from .models import BlogPost, CaseStudy, ContactSubmission, Profile, Service, ServiceDeliverable, Tutorial


class CorePageTests(TestCase):
	@classmethod
	def setUpTestData(cls):
		cls.blog_post = BlogPost.objects.create(
			title="Reporting design principles",
			slug="reporting-design-principles",
			content="Useful reporting systems balance clarity, context, and action.",
		)
		Tutorial.objects.create(
			title="Tutorial overview",
			content="This tutorial teaches practical visualization choices.",
		)
		cls.case_study = CaseStudy.objects.create(
			title="Executive KPI Command Center Test",
			slug="executive-kpi-command-center-test",
			category="Dashboard strategy",
			accent="Leadership reporting",
			client_name="Growth-stage leadership team",
			industry="Operations",
			summary="A dashboard concept for executive review.",
			client_context="Leaders needed a clearer source of truth.",
			challenge="The reporting process was fragmented.",
			approach="Defined a tighter KPI structure.",
			solution="Created a premium dashboard concept.",
			tools_used="Django, Python, Plotly",
			result="Leadership gained faster access to key information.",
			hero_image_path="images/multiplot.jpg",
		)
		cls.service = Service.objects.create(
			title="Dashboard Strategy",
			slug="dashboard-strategy",
			short_description="Create calmer, clearer reporting systems.",
			overview="A full review of reporting and dashboard needs.",
			ideal_client="Teams with growing reporting complexity.",
			business_value="Sharper decisions with less reporting friction.",
			process_summary="Audit, redesign, and handoff.",
			hero_image_path="images/data.jpg",
		)
		cls.service.case_studies.add(cls.case_study)
		ServiceDeliverable.objects.create(
			service=cls.service,
			title="Dashboard audit",
			description="A review of the current dashboard structure.",
		)

	def setUp(self):
		self.factory = RequestFactory()

	def _prepare_request(self, request, user=None, with_messages=False):
		SessionMiddleware(lambda req: None).process_request(request)
		request.session.save()
		request.user = user or AnonymousUser()
		if with_messages:
			setattr(request, "_messages", FallbackStorage(request))
		return request

	def _render_route(self, route_name, *, user=None, kwargs=None):
		kwargs = kwargs or {}
		path = reverse(route_name, kwargs=kwargs)
		request = self._prepare_request(self.factory.get(path), user=user)
		match = resolve(path)
		response = match.func(request, **match.kwargs)
		if hasattr(response, "render"):
			response.render()
		return response

	def test_public_pages_load(self):
		routes = [
			"home",
			"about",
			"services",
			"portfolio",
			"contact",
			"analytics",
			"blog_list",
			"tutorials",
			"visualizations",
			"login",
			"signup",
		]
		for route_name in routes:
			with self.subTest(route=route_name):
				response = self._render_route(route_name)
				self.assertEqual(response.status_code, 200)

	def test_detail_pages_load(self):
		response = self._render_route("blog_detail", kwargs={"slug": self.blog_post.slug})
		self.assertEqual(response.status_code, 200)

		response = self._render_route("service_detail", kwargs={"slug": self.service.slug})
		self.assertEqual(response.status_code, 200)

		response = self._render_route("portfolio_detail", kwargs={"slug": self.case_study.slug})
		self.assertEqual(response.status_code, 200)

	def test_contact_form_creates_submission(self):
		path = reverse("contact")
		request = self._prepare_request(
			self.factory.post(
				path,
				{
					"name": "Marlo",
					"email": "marlo@example.com",
					"subject": "Need reporting help",
					"message": "I need a clearer KPI dashboard.",
				},
			),
			with_messages=True,
		)
		response = resolve(path).func(request)
		self.assertEqual(response.status_code, 302)
		self.assertEqual(ContactSubmission.objects.count(), 1)

	def test_signup_creates_user_and_profile(self):
		path = reverse("signup")
		request = self._prepare_request(
			self.factory.post(
				path,
				{
					"username": "newuser",
					"first_name": "New",
					"last_name": "User",
					"email": "newuser@example.com",
					"password1": "StrongTestPass123",
					"password2": "StrongTestPass123",
				},
			),
			with_messages=True,
		)
		response = resolve(path).func(request)
		self.assertEqual(response.status_code, 302)
		user = User.objects.get(username="newuser")
		self.assertTrue(Profile.objects.filter(user=user).exists())

	def test_profile_requires_login(self):
		path = reverse("profile")
		request = self._prepare_request(self.factory.get(path))
		response = resolve(path).func(request)
		self.assertEqual(response.status_code, 302)
		self.assertIn(reverse("login"), response.url)
