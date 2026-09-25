from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models, transaction
from django.db.models import F


class Voter(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    has_voted = models.BooleanField(default=False)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.name} <{self.email}>"

    def save(self, *args, **kwargs):
        self.name = (self.name or "").strip()
        self.email = (self.email or "").strip().lower()
        self._ensure_not_registered_as_candidate()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        from apps.candidate.models import Candidate

        with transaction.atomic():
            try:
                vote = self.vote
            except ObjectDoesNotExist:
                vote = None
            if vote is not None:
                Candidate.objects.filter(pk=vote.candidate_id, votes__gt=0).update(
                    votes=F("votes") - 1
                )
            return super().delete(*args, **kwargs)

    def _ensure_not_registered_as_candidate(self):
        from apps.candidate.models import Candidate

        if not self.name:
            raise ValidationError({"name": "El nombre es obligatorio."})
        if Candidate.objects.filter(name__iexact=self.name).exists():
            raise ValidationError(
                {"name": "Un votante no puede estar registrado como candidato."}
            )
