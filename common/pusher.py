import logging

from django.conf import settings
from django.db.models import F
from pyfcm import FCMNotification

log = logging.getLogger('errors')


class Pusher:

    @property
    def fcm(self):
        push_service = FCMNotification(api_key=settings.FIREBASE_API_KEY)
        return push_service

    def send_notification(self, model, user_objects, ids, message_title):
        data_message = {
            'message_title': message_title,
            'basename': model.basename,
        }
        registration_ids = user_objects.exclude(device=None).values_list('device__token', flat=True)
        valid_registration_ids = self.fcm.clean_registration_ids(registration_ids)
        users_data = user_objects.exclude(device=None).filter(
            device__token__in=valid_registration_ids).values('id', 'device__token')

        subscription_is_main_path = f'{model.related_subscription_path}is_main'
        prefix_user_path = 'user'
        for item in users_data:
            user_id = item['id']

            noisy_ids = model.objects.annotate(
                u_id=F(f'{model.related_subscription_path}{prefix_user_path}'),
                subscription_is_main=F(subscription_is_main_path),
            ).filter(id__in=ids, u_id__in=[user_id], subscription_is_main=True).values_list('id', flat=True)

            silent_ids = model.objects.annotate(
                u_id=F(f'{model.related_subscription_path}{prefix_user_path}'),
                subscription_is_main=F(subscription_is_main_path),
            ).filter(id__in=ids, u_id__in=[user_id], subscription_is_main=False).values_list('id', flat=True)

            registration_id = item['device__token']
            data_message.update({'user_id': user_id, 'noisy_ids': list(noisy_ids), 'silent_ids': list(silent_ids)})

            result = self.fcm.single_device_data_message(registration_id=registration_id, data_message=data_message)

            if result['failure'] > 0:
                push_error = {}
                push_error.update({'token': registration_id, 'errors': result['results'], 'data_message': data_message})
                log.error(f'Push error: {push_error}')
