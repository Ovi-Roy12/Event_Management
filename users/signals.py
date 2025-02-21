from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group, Permission
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from events.models import Event, Category

@receiver(post_migrate)
def create_roles(sender, **kwargs):
    if sender.name == "users":
        # Create Groups
        admin_group, _ = Group.objects.get_or_create(name="Admin")
        organizer_group, _ = Group.objects.get_or_create(name="Organizer")
        participant_group, _ = Group.objects.get_or_create(name="Participant")

        # Assign Permissions to Organizer
        event_ct = ContentType.objects.get_for_model(Event)
        category_ct = ContentType.objects.get_for_model(Category)

        organizer_permissions = [
            "add_event",
            "change_event",
            "delete_event",
            "add_category",
            "change_category",
            "delete_category",
        ]

        for perm in organizer_permissions:
            permission = Permission.objects.get(codename=perm, content_type__in=[event_ct, category_ct])
            organizer_group.permissions.add(permission)

        print("Roles and permissions assigned successfully!")
