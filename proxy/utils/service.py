from copy import copy
from oslash import Left, Right
from django.db import transaction
from raven import breadcrumbs
from attrdict import AttrDict

from .logger import LoggerMixin


class ServiceObject(LoggerMixin):
    _context = AttrDict()

    def success(self, **kwargs):
        self._update_context(**kwargs)

        return Right(copy(self._context))

    def fail(self, fail_obj):
        if isinstance(fail_obj, str):
            message = fail_obj
        elif isinstance(fail_obj, Exception):
            message = str(fail_obj.args)

        self.logger.error(f'Failed with message: \'{message}\' and context {self._context}',
                          stack_info=True)

        return Left(message)

    def fail_with(self, left_instance):
        return left_instance

    def _reset_context(self):
        self._context = AttrDict()

    def _update_context(self, **kwargs):
        self._context = AttrDict(self._context, **kwargs)

    def __call__(self, **kwargs):
        raise NotImplementedError


def transactional(func):
    def wrapper(self, *args, **kwargs):
        with transaction.atomic():
            result = func(self, *args, **kwargs)

            if isinstance(result, Left):
                transaction.set_rollback(True)
                self.logger.info('Transaction rollback')

            return result

    return wrapper


def service_call(func):
    def wrapper(self, *args, **kwargs):
        service_name = self.__class__.__name__

        breadcrumbs.record(message='Call args',
                           category=service_name, level='info',
                           data=dict({'args': args, **kwargs}))

        try:
            self._reset_context()

            return func(self, *args, **kwargs)
        except Exception as e:
            self.logger.error(f'Service {service_name} thrown exception, context: {self._context}',
                              exc_info=e)

            raise

    return wrapper
