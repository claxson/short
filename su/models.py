from __future__ import unicode_literals
from django.core.exceptions import ObjectDoesNotExist

from django.db import models
from base58    import base58

# Create your models here.
class Var(models.Model):
    TYPES = (('I', 'Integer'),
             ('S', 'String'),
             ('F', 'Float'))
    key   = models.CharField(max_length=128, help_text='Configuration key')
    value = models.CharField(max_length=128, help_text='Configuration value')
    dtype = models.CharField(max_length=1, choices=TYPES, default='I', help_text='Data type')

    @classmethod
    def get(cls, key, cast=True):
        try:
            c = cls.objects.get(key=key)
        except ObjectDoesNotExist:
            c = None
        if c is not None:
            if cast:
                if c.dtype == 'I':
                    return int(c.value)
                elif c.dtype == 'F':
                    return float(c.value)
                else:
                    return c.value
            else:
                return c.value
        else:
            return None

class Url(models.Model):
    short = models.CharField(max_length=24, help_text='Short Url')
    real  = models.CharField(max_length=2048, help_text='Long url')

    def __unicode__(self):
        return self.short

    @classmethod
    def new_url(cls, bs, real):
        nw = cls()
        nw.real = real
        nw.save()
        if not bs.endswith('/'):
            nw.short = '%s/%s' % (bs, base58.from_int(nw.id))
        else:
            nw.short = '%s%s' % (bs, base58.from_int(nw.id))
        nw.save()
        return nw.short

    @classmethod
    def get(cls, b58id):
        i = base58.to_int(b58id)
        print i
        if i is not None:
            return cls.objects.get(id=i)
        else:
            return None