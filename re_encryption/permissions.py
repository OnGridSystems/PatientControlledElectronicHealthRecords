from rest_framework import permissions

from users.models import (
    Patient,
    Recepient
)


class OnlyPatientPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            view.patient = Patient.objects.get(user=request.user)
            
            return True
        except Patient.DoesNotExist:
            return False


class OnlyRecepientPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            view.recepient = Recepient.objects.get(user=request.user)

            return True
        except Recepient.DoesNotExist:
            return False


class RecepientHasReadPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, records_set):
        recepient = view.recepient
        delegations = Delegation.objects.filter(recepient=recepient)

        for delegation in delegations:
            if delegation.records_set == records_set:
                if delegation.type in ['read', 'write', 'add']:
                    return True

        return False


class RecepientHasWritePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, records_set):
        recepient = view.recepient
        delegations = Delegation.objects.filter(recepient=recepient)

        for delegation in delegations:
            if delegation.records_set == records_set or delegation.type in ['write', 'add']:
                return True

        return False


class RecepientHasAddPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        recepient = view.recepient
        delegation = Delegation.objects.filter(
            type='add',
            recepient=recepient,
            patient_id=request.data['patient_id']
        )

        if delegation.exists():
            return True
        else:
            return False
