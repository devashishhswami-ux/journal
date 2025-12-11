import json
import urllib.request
import urllib.parse
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.contrib.auth.decorators import login_required
from .models import Entry
import zipfile
import io

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@ensure_csrf_cookie
def index(request):
    """Renders the main SPA."""
    from .models import SiteConfiguration
    config = SiteConfiguration.load()
    
    if config.maintenance_mode and not request.user.is_staff:
        return HttpResponse("<h1>Maintenance Mode</h1><p>We are currently upgrading the system. Please try again later.</p>", status=503)

    return render(request, 'journal/index.html', {'config': config})

@login_required
def api_entries(request):
    """API to handle Journal Entries (Load / Save)."""
    if request.method == 'GET':
        entries = Entry.objects.filter(user=request.user)
        data = [{
            'id': entry.id,
            'title': entry.title,
            'content': entry.content,
            'date': entry.created_at.isoformat(),
            'durationStr': entry.duration_str
        } for entry in entries]
        return JsonResponse(data, safe=False)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            ip = get_client_ip(request)
            
            entry_id = data.get('id')
            if entry_id:
                # Update existing
                try:
                    entry = Entry.objects.get(id=entry_id, user=request.user)
                    entry.title = data.get('title', entry.title)
                    entry.content = data.get('content', entry.content)
                    entry.duration_str = data.get('durationStr', entry.duration_str)
                    # Don't update IP on edit? Or do? Let's update it.
                    entry.ip_address = ip
                    entry.save()
                    return JsonResponse({'status': 'updated', 'id': entry.id})
                except Entry.DoesNotExist:
                    pass # Fall through to create if ID is invalid (unlikely)

            # Create new
            entry = Entry.objects.create(
                user=request.user,
                title=data.get('title', 'Untitled'),
                content=data.get('content', ''),
                duration_str=data.get('durationStr', '0s'),
                ip_address=ip
            )
            
            return JsonResponse({'status': 'created', 'id': entry.id})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@login_required
def export_zip(request):
    """Export all user entries as a ZIP file."""
    entries = Entry.objects.filter(user=request.user)
    
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for entry in entries:
            # Create a filename: Date - Title.txt
            date_str = entry.created_at.strftime('%Y-%m-%d')
            safe_title = "".join([c for c in entry.title if c.isalnum() or c in (' ', '-', '_')]).strip()
            filename = f"{date_str} - {safe_title}.html"
            
            # content
            file_content = f"<h1>{entry.title}</h1><p>Date: {date_str}</p><hr>{entry.content}"
            zip_file.writestr(filename, file_content)

    zip_buffer.seek(0)
    response = HttpResponse(zip_buffer, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="my_journal_backup.zip"'
    return response

def proxy_translate(request):
    """Proxy for Google Translate (from original server.py)."""
    text = request.GET.get('text', '')
    target = request.GET.get('target', 'es')
    
    if not text:
        return JsonResponse({'error': 'No text provided'}, status=400)
    
    try:
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={target}&dt=t&q={urllib.parse.quote(text)}"
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0')
        
        with urllib.request.urlopen(req) as response:
            data = response.read()
            raw_json = json.loads(data.decode('utf-8'))
            
            translated_text = ""
            if raw_json and isinstance(raw_json, list):
                for segment in raw_json[0]:
                    if segment:
                        translated_text += segment[0]
            
            return JsonResponse({'translatedText': translated_text})
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


