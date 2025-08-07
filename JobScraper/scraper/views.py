from django.shortcuts import render, redirect
import requests
from bs4 import BeautifulSoup
from .models import Search, JobListing

def index(request):
    searches = Search.objects.all().order_by('-created_at')[:5]  # Last 5 searches
    return render(request, 'jobs.html', {'searches': searches})

def scrape_jobs(request):
    job_title = None
    if request.method == 'POST':
        job_title = request.POST.get('job_title', '').strip()
    elif request.method == 'GET':
        job_title = request.GET.get('job_title', '').strip()  # For refresh button

    if not job_title:
        return render(request, 'jobs.html', {
            'searches': Search.objects.all().order_by('-created_at')[:5],
            'error': 'Please enter a job title'
        })

    # Save search to database
    search = Search.objects.create(query=job_title)

    # Scrape RemoteOK
    url = f'https://remoteok.com/remote-{job_title.replace(" ", "-")}-jobs'
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        job_table = soup.find('table', id='jobsboard')
        if job_table:
            job_rows = job_table.find_all('tr', class_='job')
            
            for row in job_rows[:10]:  # Limit to 10 jobs for simplicity
                title_elem = row.find('h2', itemprop='title')
                company_elem = row.find('h3', itemprop='name')
                location_elem = row.find('div', class_='location')
                summary_elem = row.find('div', class_='description')
                link_elem = row.find('a', class_='preventLink')

                title = title_elem.text.strip() if title_elem else 'N/A'
                company = company_elem.text.strip() if company_elem else 'N/A'
                location = location_elem.text.strip() if location_elem else 'Remote'
                summary = summary_elem.text.strip() if summary_elem else ''
                job_url = 'https://remoteok.com' + link_elem['href'] if link_elem else ''

                JobListing.objects.create(
                    search=search,
                    title=title,
                    company=company,
                    location=location,
                    summary=summary,
                    url=job_url
                )

    # Get results for the current search
    jobs = JobListing.objects.filter(search=search).order_by('-created_at')
    return render(request, 'jobs.html', {
        'jobs': jobs,
        'job_title': job_title,
        'searches': Search.objects.all().order_by('-created_at')[:5]
    })