from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.db.models import Avg, Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from unicodedata import category

from .forms import ProposalForm, ReviewForm
from .models import LessonRequest, Review, SkillProposal, Profile, Favorites


def home(request):
    proposals = SkillProposal.objects.filter(
        status=SkillProposal.Status.PUBLISHED
    )
    explore = request.GET.get('explore')
    popular = request.GET.get('popular')
    ctr = request.GET.get('category')
    lesson_format = request.GET.get('online')
    rating_threshold = request.GET.get('rating')
    search_query = request.GET.get('q', '').strip()
    level = request.GET.get('level')
    online_or_offline = request.GET.get('online_or_offline')
    if explore:
        proposals = proposals.order_by('-created_at')
    if popular:
        proposals = proposals.filter(rating__gte=4)
    if ctr:
        proposals = proposals.filter(category__slug=ctr.lower())
    if lesson_format in SkillProposal.Format.values:
        proposals = proposals.filter(online=lesson_format)
    if rating_threshold in {'1', '2', '3', '4', '5'}:
        proposals = proposals.filter(rating__gte=rating_threshold)
    if search_query:
        proposals = proposals.filter(name__icontains=search_query)
    if level:
        proposals = proposals.filter(level=level)
    if online_or_offline:
        proposals = proposals.filter(online=online_or_offline)

    return render(request, 'skillswap/home.html', {'proposals': proposals})
@login_required
def my_skills(request):
    proposals = SkillProposal.objects.filter(author=request.user)
    return render(request, 'skillswap/home.html', {'proposals': proposals})

def proposal_detail(request, proposal_id):
    proposal = get_object_or_404(SkillProposal.objects.select_related(
        'author',
        'category'
    ).prefetch_related('reviews'), id=proposal_id)
    if proposal.status != SkillProposal.Status.PUBLISHED:
        if not request.user.is_authenticated:
            raise Http404
        if proposal.author != request.user and not request.user.is_staff:
            raise Http404
    return render(request, 'skillswap/proposal_detail.html', {'proposal': proposal})
@login_required
def lesson_request_create(request, proposal_id):
    proposal = get_object_or_404(SkillProposal.objects.select_related(
        'author',
        'category'
    ).prefetch_related('reviews'), id=proposal_id)
    if proposal.author == request.user:
        raise Http404('Нельзя отправить запрос на собственное предложение.')
    if request.method == 'POST':
        if LessonRequest.objects.filter(
                proposal=proposal,
                status=LessonRequest.Status.PENDING).exists():
            messages.error(request, 'Запрос на это занятие уже отправлен.')
            return redirect('proposal_detail', proposal_id=proposal.id)
        LessonRequest.objects.create(
            proposal=proposal,
            student=request.user,
            status=LessonRequest.Status.PENDING
        )
        messages.success(request, 'Запрос на занятие успешно отправлен.')
        return redirect('proposal_detail', proposal_id=proposal.id)
    else:
        return render(request, 'skillswap/proposal_create.html', {'proposal': proposal})


@login_required
def proposal_create(request):
    if request.method == 'POST':
        form = ProposalForm(request.POST)
        if form.is_valid():
            proposal = form.save(commit=False)
            proposal.author = request.user
            proposal.status = SkillProposal.Status.PENDING
            proposal.save()
            form.save_m2m()
            messages.success(request, 'Предложение успешно создано.')
            return redirect('proposal_detail', proposal_id=proposal.id)
    else:
        form = ProposalForm()
    return render(
        request,
        'skillswap/proposal_create.html',
        {'form': form}
    )

@login_required
def proposal_edit(request, proposal_id):
    proposal = get_object_or_404(SkillProposal, id=proposal_id)
    if proposal.author != request.user:
        messages.error(request, 'У вас нет прав на изменение этого предложения.')
        return redirect('home')
    if request.method == 'POST':
        form = ProposalForm(request.POST, instance=proposal)
        if form.is_valid():
            form.save()
            messages.success(request, 'Предложение успешно изменено.')
            return redirect('proposal_detail', proposal_id=proposal.id)
    else:
        form = ProposalForm(instance=proposal)
    return render(request, 'skillswap/proposal_edit.html', {'form': form})

def review_create(request, request_id):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    lesson_request = get_object_or_404(
        LessonRequest.objects.select_related('proposal'),
        id=request_id,
        student=request.user,
        status=LessonRequest.Status.COMPLETED,
    )
    if Review.objects.filter(lesson_request=lesson_request).exists():
        messages.info(request, 'Вы уже оценили это занятие.')
        return redirect('proposal_detail', proposal_id=lesson_request.proposal_id)

    form = ReviewForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        review = form.save(commit=False)
        review.reviewer = request.user
        review.proposal = lesson_request.proposal
        review.lesson_request = lesson_request
        review.save()

        lesson_request.proposal.rating = lesson_request.proposal.reviews.aggregate(
            Avg('rating')
        )['rating__avg']
        lesson_request.proposal.save(update_fields=['rating'])

        messages.success(request, 'Ваша оценка и отзыв сохранены.')
        return redirect('proposal_detail', proposal_id=lesson_request.proposal_id)

    return render(request, 'skillswap/review_form.html', {'form': form})


@login_required
def lesson_request_status(request, request_id):
    lesson_request = get_object_or_404(
        LessonRequest,
        id=request_id,
        proposal__author=request.user,
    )
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in LessonRequest.Status.values:
            lesson_request.status = status
            try:
                with transaction.atomic():
                    lesson_request.save()
                messages.success(request, 'Статус изменён.')
            except IntegrityError:
                messages.error(request, 'У этого пользователя уже есть активный запрос на это занятие.')
        else:
            messages.error(request, 'Выберите допустимый статус.')
    return redirect('my_lesson_requests')

@login_required
def add_favorite(request, proposal_id):
    proposal = get_object_or_404(SkillProposal, id=proposal_id)
    user = request.user
    favorites = Favorites.objects.filter(owner=request.user.id)
    if request.method == 'POST':
        favorite = Favorites.objects.create(
            proposal=proposal,
            owner=user,
        )
        favorite.save()
        messages.success(request, 'Предложение добавлено в избранное.')
    return render(request, 'skillswap/favorites.html', {'favorite': favorites})

@login_required
def delete_favorite(request, proposal_id):
    favorites = Favorites.objects.filter(owner=request.user.id)
    if request.method == 'POST':
        favorite = Favorites.objects.get(id=proposal_id, owner=request.user)
        if favorite is not None:
            favorite.delete()
            messages.success(request, 'Предложение удалено из избранного.')
    return render(request, 'skillswap/favorites.html', {'favorite': favorites})


@login_required
def favorites_list(request, user_id):
    favorites = Favorites.objects.filter(owner=user_id)
    return render(request, 'skillswap/favorites.html', {'favorite': favorites})



@login_required
def my_lesson_requests(request):
    lesson_requests = LessonRequest.objects.select_related(
        'proposal',
        'proposal__category',
        'student',
    ).filter(
        Q(proposal__author=request.user) | Q(student=request.user)
    ).order_by('-created_at')
    return render(request, 'skillswap/my_lesson_requests.html', {
        'lesson_requests': lesson_requests,
        'status_choices': LessonRequest.Status.choices,
    })

@login_required
def profile(request, user_id):
    my_profile = get_object_or_404(Profile, id=user_id)
    return render(request, 'skillswap/profile.html', {'profile': my_profile})
