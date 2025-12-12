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
    """Exports user entries as a ZIP file of text files."""
    from django.utils.html import strip_tags
    import zipfile
    import io
    
    entries = Entry.objects.filter(user=request.user)
    
    if not entries.exists():
        return JsonResponse({'error': 'No entries to export'}, status=404)

    # Create zip buffer
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for entry in entries:
            # Format: 'Title - Date.txt'
            date_str = entry.created_at.strftime('%Y-%m-%d')
            # Safe filename: replace non-alphanumeric chars (keep spaces/dashes)
            safe_title = "".join([c for c in entry.title if c.isalnum() or c in (' ', '-', '_')]).strip()
            filename = f"{date_str} - {safe_title}.txt"
            
            # Content: Title, Date, Content
            clean_content = strip_tags(entry.content)
            file_content = f"Title: {entry.title}\nDate: {entry.created_at.strftime('%Y-%m-%d %H:%M')}\nDuration: {entry.duration_str}\n\n{clean_content}"
            
            zip_file.writestr(filename, file_content)
    
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="journal_backup.zip"'
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


@login_required
def delete_entry(request, entry_id):
    """Delete a journal entry (only owner can delete)."""
    if request.method == 'DELETE' or request.method == 'POST':
        try:
            entry = Entry.objects.get(id=entry_id, user=request.user)
            entry.delete()
            return JsonResponse({'status': 'deleted', 'message': 'Entry deleted successfully'})
        except Entry.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Entry not found or you do not have permission'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


from allauth.account.views import PasswordResetView
from django.contrib import messages
from django.shortcuts import redirect

class RateLimitedPasswordResetView(PasswordResetView):
    """Custom password reset view with rate limiting (once per 24 hours)"""
    
    def form_valid(self, form):
        from .models import PasswordResetRequest
        
        email = form.cleaned_data.get('email')
        ip_address = get_client_ip(self.request)
        
        # Check rate limiting
        can_request, hours_remaining = PasswordResetRequest.can_request_reset(email)
        
        if not can_request:
            # User has already requested a reset within 24 hours
            hours = int(hours_remaining)
            minutes = int((hours_remaining - hours) * 60)
            
            messages.error(
                self.request,
                f"You can only request a password reset once per 24 hours. "
                f"Please try again in {hours}h {minutes}m."
            )
            return redirect('account_reset_password')
        
        # Create reset request record
        PasswordResetRequest.create_request(email, ip_address)
        
        # Proceed with normal password reset
        return super().form_valid(form)
