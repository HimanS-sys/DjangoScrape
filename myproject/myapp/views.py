from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import DomainForm
from .data_extraction import scrape_content, normalize_url, scrape_content_2
import json

def data_sources(request):
    if request.method == 'POST':
        form = DomainForm(request.POST)
        if form.is_valid():
            domain_url = form.cleaned_data['name']
            domain_url = normalize_url(domain_url)
            scraped_content = scrape_content_2(domain_url)
            if len(scraped_content):
                with open(f'scraped_content_11.json', 'w') as f:
                    json.dump(scraped_content, f)
                return render(request, 'success.html')
            else:
                return render(request, 'error.html')
    else:
        form = DomainForm()
    return render(request, 'data_sources.html', {'form': form})


