from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST

from perfumes.models import Perfume
from .forms import ReviewForm
from .models import Review

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

@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    if review.user != request.user and not request.user.is_staff:
        messages.error(request, 'You are not authorised to edit this review.')
        return redirect(review.perfume.get_absolute_url())

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)

        if form.is_valid():
            form.save()
            messages.success(request, 'Review updated successfully.')
            return redirect(review.perfume.get_absolute_url())

    else:
        form = ReviewForm(instance=review)

    return render(
        request,
        'reviews/edit_review.html',
        {
            'form': form,
            'review': review,
        }
    )

@login_required
@require_POST
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    if review.user != request.user and not request.user.is_staff:
        messages.error(request, 'You are not authorised to delete this review.')
        return redirect(review.perfume.get_absolute_url())

    perfume_url = review.perfume.get_absolute_url()
    review.delete()

    messages.success(request, 'Review deleted successfully.')

    return redirect(perfume_url)
