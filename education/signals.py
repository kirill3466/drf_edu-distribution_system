from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from .models import Access, Group


@receiver(post_save, sender=Access)
def update_groups(sender, instance, created, **kwargs):
    if created:
        product = instance.product
        groups = Group.objects.filter(product=product)
        print(
            f"Сигнал обновления групп для продукта {product.name} был вызван."
        )
        for group in groups:
            students_count = group.students.count()
            if students_count < group.max_students:
                group.students.add(instance.student)
                print(f"Студент {instance.student} был добавлен в группу {group.name}.")
        if product.start_date > timezone.now():
            total_students = sum([group.students.count() for group in groups])
            avg_students_per_group = total_students // len(groups)
            for group in groups:
                students_count = group.students.count()
                if students_count > avg_students_per_group + 1:
                    group.students.remove(instance.student)
                    print(f"Студент {instance.student} был удален из группы {group.name}.")
                elif students_count < avg_students_per_group - 1:
                    group.students.add(instance.student)
                    print(f"Студент {instance.student} был добавлен в группу {group.name}.")
                    break
