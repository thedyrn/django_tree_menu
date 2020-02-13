from django.db import models


class TreePathField(models.CharField):
    def pre_save(self, model_instance, add):
        if add:
            parent = (model_instance.parent or model_instance.part_of)
            parent.seq += 1
            parent.save()
            value = ('{}{:03d}'.format(getattr(parent, self.attname, ''), parent.seq, ))[:255]
            setattr(model_instance, self.attname, value)
            return value
        return models.CharField.pre_save(self, model_instance, add)


class Menu(models.Model):
    name = models.CharField(max_length=50)
    seq = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.name


class Item(models.Model):
    part_of = models.ForeignKey(Menu, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    href = models.CharField(max_length=256)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='child_set', on_delete=models.CASCADE)
    seq = models.PositiveSmallIntegerField(default=0)
    path = TreePathField(max_length=256, blank=True)

    @property
    def level(self):
        return max(0, int(len(self.path) / 3) - 1)

    def __str__(self):
        return self.title
