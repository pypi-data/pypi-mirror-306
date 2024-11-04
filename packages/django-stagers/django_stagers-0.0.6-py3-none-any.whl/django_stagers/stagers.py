from collections import defaultdict
import logging
from typing import Any, Generic, TypeVar

from django.db.models import Model, QuerySet


M = TypeVar('M', bound=Model)


class Stager(Generic[M]):

    existing: dict[str, M]
    seen: set[str]
    key: str

    existing_related: dict[str, dict[str, QuerySet]]

    to_create: dict[str, M]
    to_update: dict[str, M]
    to_delete: set[str]

    to_update_fields: set[str]

    def __init__(
        self,
        queryset: QuerySet[M],
        key: str = 'pk',
        load_related: list[str] = []
    ) -> None:

        self.queryset = queryset
        self.model = self.queryset.model
        self.key = key
        self.seen = set()
        self.to_create = {}
        self.to_update = {}
        self.to_delete = set()
        self.to_update_fields = set()

        self.existing = {getattr(m, key): m for m in self.queryset}

        self.existing_related = defaultdict(dict)
        for key in load_related:
            for existing_key, existing_model in self.existing.items():
                self.existing_related[key][existing_key] = getattr(existing_model, key).all()

    def create(self, qs_or_instance: QuerySet[M] | M):
        if isinstance(qs_or_instance, QuerySet):
            for instance in qs_or_instance:
                self.create(instance)
        else:
            key = str(getattr(qs_or_instance, self.key))
            self.to_create[key] = qs_or_instance
            if not key in self.existing:
                self.existing[key] = qs_or_instance
            else:
                raise Exception(f"Tried to create a duplicate model with key = {key}")

    def update(self, qs_or_instance: QuerySet[M] | M, field: str, value: Any):
        if isinstance(qs_or_instance, QuerySet):
            for instance in qs_or_instance:
                self.update(instance, field, value)
        else:
            key = str(getattr(qs_or_instance, self.key))

            if key in self.to_create:
                to_create = self.to_create[key]
                if getattr(to_create, field) != value:
                    setattr(to_create, field, value)

            if key in self.existing:
                existing = self.existing[key]
                if getattr(existing, field) != value:
                    setattr(existing, field, value)
                    self.to_update_fields.add(field)
                    self.to_update[key] = existing

    def delete(self, qs_or_instance: QuerySet[M] | M):
        if isinstance(qs_or_instance, QuerySet):
            for instance in qs_or_instance:
                self.delete(instance)
        else:
            self.to_delete.add(str(qs_or_instance.pk))

    def add_seen(self, key: str):
        self.seen.add(key)

    @property
    def unseen_instances(self):
        return list({str(model.pk) for key, model in self.existing.items() if key not in self.seen})

    def commit(self):

        # Determine type of provided type argument `M`
        logging.info(f'Committing staged {self.model.__name__} instances.')

        if self.to_create:
            self.model.objects.bulk_create(list(self.to_create.values()))
            logging.info(f'Created {len(self.to_create):6,} {self.model.__name__} instances.')

        if self.to_update:
            self.model.objects.bulk_update(list(self.to_update.values()), fields=list(self.to_update_fields))
            logging.info(f'Updated {len(self.to_update):6,} {self.model.__name__} instances.')
            logging.info(f'Updated Fields: {self.to_update_fields}')

        if self.to_delete:
            self.model.objects.filter(id__in=self.to_delete).delete()
            logging.info(f'Deleted {len(self.to_delete):6,} {self.model.__name__} instances.')
