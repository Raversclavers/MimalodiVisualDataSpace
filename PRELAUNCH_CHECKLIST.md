# Pre-Launch Verification Checklist

This checklist is written for this exact Django project: Mimalodi Visual Data Space.

Use it before your first public deployment.

If you are a beginner, follow the steps in order and do not skip ahead.

## 1. Prepare your local environment

Goal: make sure you are testing the same project state you plan to deploy.

1. Open PowerShell in the project root.
1. Activate the virtual environment.

```powershell
.\venv\Scripts\Activate.ps1
```

1. Confirm dependencies are installed.

```powershell
pip install -r requirements.txt
```

1. Make sure your environment variables are set.

Minimum local values:

```powershell
$env:DJANGO_SECRET_KEY='replace-with-a-real-secret-key'
$env:DJANGO_DEBUG='True'
$env:DJANGO_ALLOWED_HOSTS='localhost,127.0.0.1'
$env:DJANGO_CSRF_TRUSTED_ORIGINS='http://localhost:8000'
```

1. Confirm the project starts cleanly.

```powershell
python manage.py runserver
```

Pass if:

- the server starts without import errors
- you can open `http://127.0.0.1:8000/`
- there is no error page on first load

## 2. Migration checks

Goal: make sure the database schema matches the models used by the site.

1. Check for unapplied migrations.

```powershell
python manage.py showmigrations
```

1. Run migrations.

```powershell
python manage.py migrate
```

1. Check whether Django wants to create new migrations unexpectedly.

```powershell
python manage.py makemigrations --check --dry-run
```

Pass if:

- `migrate` completes without errors
- `makemigrations --check --dry-run` does not report model drift
- the `Service` and `CaseStudy` tables work in admin and public pages

Important for this project:

- make sure migration `core/migrations/0012_service_models.py` is applied
- the public services pages depend on the `Service` and `ServiceDeliverable` models

## 3. Local run checks

Goal: confirm the main public site works with real page loads.

Start the local server if it is not already running:

```powershell
python manage.py runserver
```

Open each of these pages in a browser and confirm they load without errors:

- `/`
- `/about/`
- `/services/`
- one service detail page such as `/services/dashboard-design/` if sample data exists
- `/portfolio/`
- one case study detail page
- `/contact/`
- `/blog/`
- `/tutorials/`
- `/visualizations/`
- `/login/`
- `/signup/`

Pass if:

- every page returns normally
- there are no broken layouts or missing images on major sections
- no page shows a Django debug error

## 4. Static files checks

Goal: make sure CSS, icons, images, and collected static assets work before deployment.

1. Run collectstatic.

```powershell
python manage.py collectstatic --noinput
```

1. Check that the command completes successfully.
1. Reload the local site and confirm styling still appears correctly.
1. Verify these assets load in the browser:

- main stylesheet
- favicon files
- apple touch icon
- home hero image
- service or case study images

Pass if:

- `collectstatic` finishes without crashing
- the site still looks styled after collection
- icons and images appear correctly

Note for this project:

- `staticfiles/` is generated output and should not stay tracked in git
- duplicate static file warnings can happen because old generated files were committed earlier; they should be cleaned from git tracking before launch maintenance work

## 5. Broken link checks

Goal: make sure visitors do not hit dead ends.

Manually click through the main navigation and footer links:

- Home
- About
- Services
- Portfolio
- Contact
- Blog
- Tutorials
- Visualizations
- Account
- Book a discovery call
- footer links

Also test:

- links from the home page to service pages
- links from the home page to portfolio pages
- links from service detail pages to contact and portfolio
- links from portfolio detail pages back to portfolio and contact

Pass if:

- every clicked link lands on the expected page
- there are no 404 pages for public navigation paths
- related service and related case study cards resolve correctly

Optional command-based check:

```powershell
python manage.py test
```

This project already includes route coverage in tests, but you should still do the manual click-through.

## 6. Admin checks

Goal: make sure the content management side is ready for real updates.

1. Create an admin user if you do not already have one.

```powershell
python manage.py createsuperuser
```

1. Open `/admin/` and sign in.
1. Confirm these models appear and open correctly:

- Blog posts
- Tutorials
- Contact submissions
- Case studies
- Services

1. Create or edit one record in each important area:

- one `Service`
- one `ServiceDeliverable`
- one `CaseStudy`
- one `CaseStudyMetric`
- one `CaseStudyScreenshot`

1. Save each record and reload its public page.

Pass if:

- admin login works
- add/edit forms save successfully
- service detail pages reflect service content
- portfolio detail pages reflect case study content

## 7. Contact form checks

Goal: make sure public inquiries can be submitted and reviewed.

1. Open `/contact/`.
1. Submit the form with invalid data first.

Example invalid test:

- name: `A`
- email: `not-an-email`
- subject: `Hi`
- message: `Too short`

Confirm:

- validation errors appear
- fields show clear feedback
- the submission is not saved

1. Submit the form again with valid data.

Example valid test:

- name: your real name
- email: an email you can check
- subject: `Pre-launch contact form test`
- message: `This is a launch readiness test for the contact workflow and admin review process.`

1. Confirm the success message appears.
1. Open Django admin and verify the submission appears under `Contact submissions`.
1. If email settings are enabled, confirm the notification email arrives.

Pass if:

- invalid submissions are blocked
- valid submissions are saved
- the admin can review the saved inquiry

Also test one service-prefilled inquiry:

1. Open a service detail page.
1. Click the inquiry button.
1. Confirm the contact form subject is prefilled for that service.

## 8. Mobile responsiveness checks

Goal: make sure the public site feels professional on phones and tablets.

Use your browser dev tools device toolbar.

Test at least these widths:

- 375px wide
- 768px wide
- 1280px wide

Check these pages carefully:

- home page
- services page
- one service detail page
- portfolio page
- one portfolio detail page
- contact page

Look for:

- navigation menu opens and closes correctly
- buttons do not overlap
- cards stack cleanly
- images do not overflow their containers
- text remains readable without horizontal scrolling
- form fields are easy to tap

Pass if:

- there is no horizontal scroll on major pages
- CTA buttons remain visible and usable
- spacing still looks intentional on mobile

## 9. SEO metadata checks

Goal: make sure the site has basic search-friendly metadata.

For these pages, open page source or inspect the `<head>` section:

- home page
- services page
- one service detail page
- portfolio page
- one portfolio detail page

Check for:

- a meaningful `<title>`
- a `<meta name="description">`
- correct favicon links
- viewport meta tag

Pass if:

- page titles are specific and readable
- descriptions are not empty
- icons load correctly

Project-specific note:

- the base template already has a default meta description
- service models include `seo_title` and `seo_description`
- before launch, verify that service detail pages actually show page-specific descriptions in the rendered HTML
- do the same spot check for important portfolio pages so generic metadata does not slip into production

## 10. Accessibility spot checks

Goal: catch obvious usability issues before the site goes live.

Manually test:

1. Press `Tab` from the top of the page.
1. Confirm the skip link appears and works.
1. Continue tabbing through navigation, buttons, and forms.
1. Confirm focus remains visible.
1. On the contact page, confirm error messages are readable and connected to the relevant fields.
1. Confirm images have meaningful alt text.
1. Confirm headings appear in a sensible order on major pages.

Check these pages at minimum:

- home
- services
- service detail
- contact
- login
- signup

Pass if:

- keyboard navigation works
- the skip link jumps to main content
- form errors are visible and understandable
- no major page becomes unusable without a mouse

This project already includes some accessibility work such as:

- skip link support
- ARIA-aware form error attributes
- semantic navigation labels

You are confirming those features still work after recent edits.

## 11. Deployment environment variable checks

Goal: make sure production settings are correct before you go live.

Confirm these variables are set on the host:

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG=False`
- `DJANGO_ALLOWED_HOSTS`
- `DJANGO_CSRF_TRUSTED_ORIGINS`

Optional but useful:

- `DEFAULT_FROM_EMAIL`
- `CONTACT_NOTIFICATION_EMAIL`
- `SQLITE_PATH`

Local production-style validation command:

```powershell
$env:DJANGO_SECRET_KEY='replace-with-a-long-random-secret-key'
$env:DJANGO_DEBUG='False'
$env:DJANGO_ALLOWED_HOSTS='localhost,127.0.0.1'
$env:DJANGO_CSRF_TRUSTED_ORIGINS='http://localhost:8000'
python manage.py check --deploy
```

Pass if:

- `check --deploy` reports no issues
- `DEBUG` is false in production
- allowed hosts match the real domain
- CSRF trusted origins match the real HTTPS URL

## 12. Post-deploy smoke test checklist

Goal: confirm the live site works immediately after deployment.

After you deploy:

1. Open the live home page.
1. Confirm the site loads over HTTPS.
1. Open these live pages:

- home
- about
- services
- one service detail page
- portfolio
- one portfolio detail page
- contact
- blog
- admin login

1. Confirm CSS and icons load correctly.
1. Submit a real contact test message.
1. Confirm the message appears in admin.
1. Log into admin and confirm content pages still open.
1. Check one image-heavy page and one form-heavy page on mobile.
1. Refresh a few pages directly by URL to catch any routing or static issues.

Pass if:

- no page returns a server error
- styling loads correctly on the live domain
- admin works
- contact submissions save correctly
- the main marketing pages are usable on mobile and desktop

## 13. Final go-live decision

You are ready to launch when all of these are true:

- migrations are current
- the site runs locally without errors
- static files collect successfully
- public links work
- admin editing works
- contact form submissions save correctly
- mobile checks look clean
- metadata is present and reasonable
- accessibility spot checks pass
- deployment environment variables are correct
- live smoke tests pass on the deployed site

If even one of those areas fails, fix it before publicly sharing the site.
