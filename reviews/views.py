
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from perfumes.models import Perfume
from .forms import ReviewForm


@login_required
@require_http_methods(["GET", "POST"])
def submit_review(request, perfume_id):
    perfume = get_object_or_404(Perfume, id=perfume_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.perfume = perfume

            try:
                review.save()
                messages.success(
                    request,
                    'Your review has been submitted successfully.'
                )
                return redirect(perfume.get_absolute_url())

            except Exception:
                messages.error(
                    request,
                    'You have already reviewed this perfume.'
                )
    else:
        form = ReviewForm()

    return render(
        request,
        'reviews/submit_review.html',
        {
            'form': form,
            'perfume': perfume,
        }
    )