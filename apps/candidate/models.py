from django.core.exceptions import ValidationError
from django.db import models, transaction


class Candidate(models.Model):
    name = models.CharField(max_length=255)
    party = models.CharField(max_length=255, blank=True, null=True)
    votes = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = (self.name or "").strip()
        if self.party:
            self.party = self.party.strip()
        self._ensure_not_registered_as_voter()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        from apps.vote.models import Vote
        from apps.voter.models import Voter

        with transaction.atomic():
            voter_ids = list(
                Vote.objects.filter(candidate=self).values_list("voter_id", flat=True)
            )
            if voter_ids:
                Voter.objects.filter(pk__in=voter_ids).update(has_voted=False)
            return super().delete(*args, **kwargs)

    def _ensure_not_registered_as_voter(self):
        from apps.voter.models import Voter

        if not self.name:
            raise ValidationError({"name": "El nombre es obligatorio."})
        if Voter.objects.filter(name__iexact=self.name).exists():
            raise ValidationError(
                {"name": "Un candidato no puede estar registrado como votante."}
            )
