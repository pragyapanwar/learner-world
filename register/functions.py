from .models import subject


def add_mmkey(subj,user):
    subject_=subject.objects.get(id=subj.id)
    subject_.userid=user
    subject_save()
