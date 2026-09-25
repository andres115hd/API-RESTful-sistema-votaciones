from django.core.exceptions import ValidationError
from django.db import IntegrityError, models, transaction
from django.db.models import Count, F


class Vote(models.Model):
    voter = models.OneToOneField(
        "voter.Voter",
        on_delete=models.CASCADE,
        related_name="vote",
    )
    candidate = models.ForeignKey(
        "candidate.Candidate",
        on_delete=models.CASCADE,
        related_name="vote_records",
    )

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"Vote {self.pk}: voter={self.voter_id} → candidate={self.candidate_id}"

    def save(self, *args, **kwargs):
        if not self._state.adding:
            raise ValidationError("Los votos no pueden modificarse.")

        from apps.candidate.models import Candidate
        from apps.voter.models import Voter

        try:
            voter = Voter.objects.get(pk=self.voter_id)
        except (Voter.DoesNotExist, ValueError, TypeError) as exc:
            raise ValidationError({"voter_id": "El votante no existe."}) from exc

        try:
            candidate = Candidate.objects.get(pk=self.candidate_id)
        except (Candidate.DoesNotExist, ValueError, TypeError) as exc:
            raise ValidationError({"candidate_id": "El candidato no es válido."}) from exc

        if voter.has_voted:
            raise ValidationError({"voter_id": "El votante ya ha emitido un voto."})

        try:
            with transaction.atomic():
                super().save(*args, **kwargs)
                updated = Voter.objects.filter(pk=voter.pk, has_voted=False).update(
                    has_voted=True
                )
                if updated != 1:
                    raise ValidationError(
                        {"voter_id": "El votante ya ha emitido un voto."}
                    )
                Candidate.objects.filter(pk=candidate.pk).update(votes=F("votes") + 1)
        except IntegrityError as exc:
            raise ValidationError(
                {"voter_id": "El votante ya ha emitido un voto."}
            ) from exc

    def delete(self, *args, **kwargs):
        raise ValidationError("No se pueden eliminar votos.")

    @classmethod
    def get_statistics(cls):
        from apps.candidate.models import Candidate
        from apps.voter.models import Voter

        total_votes = cls.objects.count()
        by_candidate = []
        candidates = Candidate.objects.annotate(total_votes=Count("vote_records")).order_by(
            "id"
        )
        for candidate in candidates:
            votes = candidate.total_votes
            percentage = (votes / total_votes * 100) if total_votes else 0
            by_candidate.append(
                {
                    "candidate_id": candidate.id,
                    "name": candidate.name,
                    "party": candidate.party,
                    "votes": votes,
                    "percentage": round(percentage, 2),
                }
            )
        return {
            "votes_by_candidate": by_candidate,
            "voters_who_voted": Voter.objects.filter(has_voted=True).count(),
        }
