from django.test import TestCase, Client
from django.urls import reverse
from .models import Search, JobListing
from unittest.mock import patch
import datetime

class SearchModelTest(TestCase):
    def test_search_creation(self):
        search = Search.objects.create(query='Python Developer')
        self.assertEqual(str(search), 'Python Developer')
        self.assertIsInstance(search.created_at, datetime.datetime)


class JobListingModelTest(TestCase):
    def setUp(self):
        self.search = Search.objects.create(query='Backend Developer')

    def test_job_listing_creation(self):
        job = JobListing.objects.create(
            search=self.search,
            title='Senior Backend Developer',
            company='TechCorp',
            location='Remote',
            summary='Develop backend APIs using Django.',
            url='https://example.com/job/1'
        )
        self.assertEqual(str(job), 'Senior Backend Developer')
        self.assertEqual(job.search.query, 'Backend Developer')


class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.index_url = reverse('index')
        self.scrape_url = reverse('scrape_jobs')

    def test_index_view_status_code(self):
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'jobs.html')

    @patch('scraper.views.requests.get')
    def test_scrape_jobs_post(self, mock_get):
        # Mocked HTML response
        mock_html = '''
        <table id="jobsboard">
            <tr class="job">
                <td>
                    <h2 itemprop="title">Data Analyst</h2>
                    <h3 itemprop="name">DataCorp</h3>
                    <div class="location">Anywhere</div>
                    <div class="description">Analyze datasets.</div>
                    <a class="preventLink" href="/remote-jobs/12345">Job Link</a>
                </td>
            </tr>
        </table>
        '''
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = mock_html.encode('utf-8')

        response = self.client.post(self.scrape_url, {'job_title': 'data analyst'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'jobs.html')
        self.assertEqual(JobListing.objects.count(), 1)

        job = JobListing.objects.first()
        self.assertEqual(job.title, 'Data Analyst')
        self.assertEqual(job.company, 'DataCorp')
        self.assertEqual(job.location, 'Anywhere')
        self.assertIn('12345', job.url)

