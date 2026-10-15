from django.contrib import admin
from .models import Category, LessonRequest, Profile, Review, SkillProposal
from django.contrib.auth.models import User

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','slug')
    search_fields = ('name','slug')
    prepopulated_fields = {'slug':('name',)}

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id","reviewer","profile","proposal", "rating","created_at",)
    search_fields = ("review", "reviewer__username")
    list_filter = ("rating", "created_at")
    readonly_fields = ("created_at", "uploaded_at")

@admin.register(SkillProposal)
class SkillProposalAdmin(admin.ModelAdmin):
    list_display = ("name","category", "author", "level","online", "status", "created_at")
    search_fields = ("name","category__name", "author__username")
    list_filter = ("status", "category", "level", "online")
    readonly_fields = ("created_at", "uploaded_at")
    autocomplete_fields = ("author", "category")

    actions = ("publish_proposals", "reject_proposals")
    @admin.action(description="Опубликовать предложения")
    def publish_proposals(self, request, queryset):
        queryset.update(status=SkillProposal.Status.PUBLISHED)
    @admin.action(description="Отклонить предложения")
    def reject_proposals(self, request, queryset):
        queryset.update(status=SkillProposal.Status.REJECTED)

@admin.register(LessonRequest)
class LessonRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "proposal", "status", "created_at")
    search_fields = ("proposal__name", "status", "created_at")
    list_filter = ("status", "created_at")
    readonly_fields = ("created_at", )
    autocomplete_fields = ("proposal","student")

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id","short_bio", "rating", "proposals_count","completed_lessons_count")
    search_fields = ("id","short_bio")
    list_filter = ("rating",)
