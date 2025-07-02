from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views import View
from django.utils.decorators import method_decorator
from .models import VersionUpdate
from .forms import VersionUpdateForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
import random
from django.utils import timezone
from collections import Counter
from datetime import timedelta
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
import io
from django.views.decorators.csrf import csrf_exempt
import os
from dotenv import load_dotenv

# Create your views here.

@method_decorator(login_required, name='dispatch')
class DashboardView(View):
    def get(self, request):
        updates = VersionUpdate.objects.filter(user=request.user).order_by('-created_at')
        quotes = [
            "Growth is never by mere chance; it is the result of forces working together.",
            "Every version of you is a step toward your best self.",
            "Small, intentional updates create extraordinary change.",
            "You are the author of your own evolution."
        ]
        quote = random.choice(quotes)
        num_updates = updates.count()
        # Leveling system
        if num_updates <= 0:
            level = 0
            level_name = "Uninitiated"
            next_level = 1
            next_level_at = 1
        elif num_updates <= 3:
            level = 1
            level_name = "Seed"
            next_level = 2
            next_level_at = 4
        elif num_updates <= 7:
            level = 2
            level_name = "Grower"
            next_level = 3
            next_level_at = 8
        elif num_updates <= 12:
            level = 3
            level_name = "Refiner"
            next_level = 4
            next_level_at = 13
        elif num_updates <= 20:
            level = 4
            level_name = "Architect"
            next_level = 5
            next_level_at = 21
        else:
            level = 5
            level_name = "Master Builder"
            next_level = None
            next_level_at = None
        if next_level_at:
            progress = int((num_updates / next_level_at) * 100)
            progress = min(progress, 100)
        else:
            progress = 100
        return render(request, 'dashboard.html', {
            'updates': updates,
            'quote': quote,
            'level': level,
            'level_name': level_name,
            'next_level': next_level,
            'next_level_at': next_level_at,
            'progress': progress,
            'num_updates': num_updates,
        })

@method_decorator(login_required, name='dispatch')
class CreateUpdateView(View):
    def get(self, request):
        form = VersionUpdateForm()
        return render(request, 'create_update.html', {'form': form})

    def post(self, request):
        form = VersionUpdateForm(request.POST)
        if form.is_valid():
            version_update = form.save(commit=False)
            version_update.user = request.user
            version_update.save()
            messages.success(request, "Your update was created successfully!")
            return redirect('dashboard')
        return render(request, 'create_update.html', {'form': form})

class RegisterView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
        return render(request, 'register.html', {'form': form})

class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
        return render(request, 'login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        user = request.user
        updates = VersionUpdate.objects.filter(user=user).order_by('-created_at')
        num_updates = updates.count()
        latest_update = updates.first() if num_updates > 0 else None
        return render(request, 'profile.html', {
            'user_obj': user,
            'num_updates': num_updates,
            'latest_update': latest_update,
        })

@method_decorator(login_required, name='dispatch')
class TimelineView(View):
    def get(self, request):
        updates = VersionUpdate.objects.filter(user=request.user).order_by('-created_at')
        return render(request, 'timeline.html', {'updates': updates})

@method_decorator(login_required, name='dispatch')
class StatsView(View):
    def get(self, request):
        user = request.user
        updates = VersionUpdate.objects.filter(user=user).order_by('created_at')
        total_updates = updates.count()

        # Updates per month (last 6 months)
        now = timezone.now()
        months = []
        updates_per_month = []
        for i in range(5, -1, -1):
            month = (now - timedelta(days=now.day-1)).replace(day=1) - timedelta(days=30*i)
            month_start = month.replace(day=1)
            next_month = (month_start + timedelta(days=32)).replace(day=1)
            count = updates.filter(created_at__gte=month_start, created_at__lt=next_month).count()
            months.append(month_start.strftime('%b %Y'))
            updates_per_month.append(count)
        months = months[::-1]
        updates_per_month = updates_per_month[::-1]

        # Most used words in summaries (optional)
        all_words = []
        for u in updates:
            all_words += u.summary.lower().split()
        common_words = [w for w, c in Counter(all_words).most_common(5) if len(w) > 3]

        # Average time between updates
        if total_updates > 1:
            times = [u.created_at for u in updates]
            deltas = [(times[i] - times[i-1]).total_seconds() for i in range(1, len(times))]
            avg_delta = sum(deltas) / len(deltas)
            avg_days = avg_delta / 86400
        else:
            avg_days = None

        # First and latest update
        first_update = updates.first()
        latest_update = updates.last()

        month_counts = list(zip(months, updates_per_month))
        return render(request, 'stats.html', {
            'total_updates': total_updates,
            'month_counts': month_counts,
            'common_words': common_words,
            'avg_days': avg_days,
            'first_update': first_update,
            'latest_update': latest_update,
        })

@method_decorator(login_required, name='dispatch')
class ExportPDFView(View):
    def get(self, request):
        updates = VersionUpdate.objects.filter(user=request.user).order_by('-created_at')
        html = render_to_string('export_pdf.html', {'updates': updates, 'user': request.user})
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="human_updates.pdf"'
        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse('PDF generation error', status=500)
        return response

@method_decorator(login_required, name='dispatch')
class ExportMarkdownView(View):
    def get(self, request):
        updates = VersionUpdate.objects.filter(user=request.user).order_by('-created_at')
        lines = [f"# Human Updates for {request.user.username}\n"]
        for u in updates:
            lines.append(f"## {u.version} ({u.created_at.strftime('%Y-%m-%d %H:%M')})\n")
            lines.append(f"**Summary:** {u.summary}\n")
            if u.highlights:
                lines.append(f"**Highlights:** {u.highlights}\n")
            lines.append('---\n')
        md_content = '\n'.join(lines)
        response = HttpResponse(md_content, content_type='text/markdown')
        response['Content-Disposition'] = 'attachment; filename="human_updates.md"'
        return response

@method_decorator(csrf_exempt, name='dispatch')
class AskAIView(View):
    def post(self, request):
        version = request.POST.get('version', '')
        summary = request.POST.get('summary', '')
        highlights = request.POST.get('highlights', '')
        user_prompt = (
            "Act as a personal self-development coach. Based on the fact that the user is reflecting on the past week, generate:\n"
            "- a suggested version number (e.g. v1.4)\n"
            "- a short summary (max 4 sentences) that feels supportive and real\n"
            "- 3 highlights focusing on small wins or key insights.\n\n"
            "Tone: optimistic, grounded, emotionally intelligent.\n"
            f"Current input:\nVersion: {version}\nSummary: {summary}\nHighlights: {highlights}\n"
            "Respond in this format:\nVersion: ...\nSummary: ...\nHighlights:\n- ...\n- ...\n- ..."
        )
        load_dotenv()
        import openai
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_prompt}]
        )
        ai_text = response.choices[0].message.content
        import re
        version_match = re.search(r"Version:\s*(.*)", ai_text)
        summary_match = re.search(r"Summary:\s*([\s\S]*?)Highlights:", ai_text)
        highlights_match = re.search(r"Highlights:\s*([\s\S]*)", ai_text)
        version_val = version_match.group(1).strip() if version_match else ''
        summary_val = summary_match.group(1).strip() if summary_match else ''
        highlights_val = highlights_match.group(1).strip() if highlights_match else ''
        return JsonResponse({
            'version': version_val,
            'summary': summary_val,
            'highlights': highlights_val,
            'raw': ai_text
        })

@method_decorator(login_required, name='dispatch')
class EditUpdateView(View):
    def get(self, request, pk):
        update = get_object_or_404(VersionUpdate, pk=pk, user=request.user)
        form = VersionUpdateForm(instance=update)
        return render(request, 'edit_update.html', {'form': form, 'update': update})

    def post(self, request, pk):
        update = get_object_or_404(VersionUpdate, pk=pk, user=request.user)
        form = VersionUpdateForm(request.POST, instance=update)
        if form.is_valid():
            form.save()
            messages.success(request, "Your update was edited successfully!")
            return redirect('dashboard')
        return render(request, 'edit_update.html', {'form': form, 'update': update})

@method_decorator(login_required, name='dispatch')
class DeleteUpdateView(View):
    def get(self, request, pk):
        update = get_object_or_404(VersionUpdate, pk=pk, user=request.user)
        return render(request, 'delete_update.html', {'update': update})

    def post(self, request, pk):
        update = get_object_or_404(VersionUpdate, pk=pk, user=request.user)
        update.delete()
        messages.success(request, "Your update was deleted.")
        return redirect('dashboard')
