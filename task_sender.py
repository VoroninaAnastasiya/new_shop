from typing import Any, Dict, List, Optional
from uuid import UUID

from django.conf import settings

from common.logger import get_logger
from common.queue import Exchange, Queue
from common.rabbitmq_pusher import RabbitMQPusher
from entities.guest_payments.models.payments_settings_choices import PaymentsSettingsVersion
from project.settings import PMS_INTEGRATION_SYNC_TASK_URL
from values.origin.models import Origin

logger = get_logger("Send tasks")


def send_update_apaleo_reservation_task(user_id, input_data):
    logger.info(f"Send update reservation to Apaleo service {input_data}")

    routing_key = f"{settings.UPDATER_V2['ROUTING_KEY_TO_UPDATER_V2']}"
    exchange = Exchange(settings.UPDATER_V2['EXCHANGE_TO_UPDATER_V2'], type='topic')
    pusher = RabbitMQPusher()

    data = {
        "url": f"/apaleo/users/{user_id}/update-pms-reservation/",
        "method": "POST",
        "changes":  input_data
    }
    pusher.send(data, exchange, routing_key)

    logger.info("Update reservation to Apaleo service task sent")


def send_move_user_contracts_task(input_data):
    logger.info(f"Send move user contracts task. Data: {input_data}")

    routing_key = f"{settings.UPDATER_V2['ROUTING_KEY_TO_UPDATER_V2']}"
    exchange = Exchange(settings.UPDATER_V2['EXCHANGE_TO_UPDATER_V2'], type='topic')
    pusher = RabbitMQPusher()

    data = {
        "url": "/documents/contracts/move-contracts/",
        "method": "POST",
        "changes":  input_data
    }
    pusher.send(data, exchange, routing_key)

    logger.info("Move user contracts task sent")


def send_document_task(input_data):
    logger.info(f"Send document task. Data: {input_data}")

    routing_key = f"{settings.UPDATER_V2['ROUTING_KEY_TO_UPDATER_V2']}"
    exchange = Exchange(settings.UPDATER_V2['EXCHANGE_TO_UPDATER_V2'], type='topic')
    pusher = RabbitMQPusher()

    enty_form_data = {
        "url": "/documents/entry-forms/",
        "method": "POST",
        "changes":  input_data
    }
    pusher.send(enty_form_data, exchange, routing_key)

    logger.info("Document task sent.")


def send_entry_form_retrieve_and_create_task(input_data):
    logger.info(f"Send document task. Data: {input_data}")

    routing_key = f"{settings.UPDATER_V2['ROUTING_KEY_TO_UPDATER_V2']}"
    exchange = Exchange(settings.UPDATER_V2['EXCHANGE_TO_UPDATER_V2'], type='topic')
    pusher = RabbitMQPusher()

    entry_form_data = {
        "url": "/documents/entry-forms/retrieve-and-create/",
        "method": "POST",
        "changes":  input_data
    }
    logger.info(f"Sending to: {routing_key}, {exchange}, {pusher}")
    pusher.send(entry_form_data, exchange, routing_key)

    logger.info("Document task sent.")


def send_waivo_terms_retrieve_and_create_task(input_data):
    logger.info(f"Send waivo terms task. Data: {input_data}")

    routing_key = f"{settings.UPDATER_V2['ROUTING_KEY_TO_UPDATER_V2']}"
    exchange = Exchange(settings.UPDATER_V2['EXCHANGE_TO_UPDATER_V2'], type='topic')
    pusher = RabbitMQPusher()

    waivo_terms_data = {
        "url": "/documents/guest-waivo-terms/retrieve-and-create/",
        "method": "POST",
        "changes":  input_data
    }
    pusher.send(waivo_terms_data, exchange, routing_key)

    logger.info("Document task sent.")


def send_entry_form_deleted_reservation(input_data):
    logger.info(f"Send deleted reservation event. Data: {input_data}")

    routing_key = f"{settings.UPDATER_V2['ROUTING_KEY_TO_UPDATER_V2']}"
    exchange = Exchange(settings.UPDATER_V2['EXCHANGE_TO_UPDATER_V2'], type='topic')
    pusher = RabbitMQPusher()

    entry_form_data = {
        "url": "/documents/entry-forms/deleted-reservation/",
        "method": "POST",
        "changes":  input_data
    }
    pusher.send(entry_form_data, exchange, routing_key)

    logger.info("Deleted reservation event sent in entry forms.")


def send_entry_form_restored_reservation(input_data):
    logger.info(f"Send deleted reservation event. Data: {input_data}")

    routing_key = f"{settings.UPDATER_V2['ROUTING_KEY_TO_UPDATER_V2']}"
    exchange = Exchange(settings.UPDATER_V2['EXCHANGE_TO_UPDATER_V2'], type='topic')
    pusher = RabbitMQPusher()

    entry_form_data = {
        "url": "/documents/entry-forms/restored-reservation/",
        "method": "POST",
        "changes":  input_data
    }
    pusher.send(entry_form_data, exchange, routing_key)

    logger.info("Restored reservation event sent in entry forms.")


def send_entry_form_housings_restored(input_data):
    logger.info(f"Send housing restored event. Data: {input_data}")

    routing_key = f"{settings.UPDATER_V2['ROUTING_KEY_TO_UPDATER_V2']}"
    exchange = Exchange(settings.UPDATER_V2['EXCHANGE_TO_UPDATER_V2'], type='topic')
    pusher = RabbitMQPusher()

    entry_form_data = {
        "url": "/documents/entry-forms/housings-restored/",
        "method": "POST",
        "changes":  input_data
    }
    pusher.send(entry_form_data, exchange, routing_key)

    logger.info("Housing restored event sent.")


def send_entry_form_housing_deactivated(input_data):
    logger.info(f"Send housing deactivated event. Data: {input_data}")

    routing_key = f"{settings.UPDATER_V2['ROUTING_KEY_TO_UPDATER_V2']}"
    exchange = Exchange(settings.UPDATER_V2['EXCHANGE_TO_UPDATER_V2'], type='topic')
    pusher = RabbitMQPusher()

    entry_form_data = {
        "url": "/documents/entry-forms/hide-deactivated-housing-documents/",
        "method": "POST",
        "changes":  input_data
    }
    pusher.send(entry_form_data, exchange, routing_key)

    logger.info("Housing deactivated event sent.")


def send_guestbook_settings_task(housing_id, starting_num):
    logger.info(f"Send guestbook settings task. Data: {housing_id}, {starting_num}")

    routing_key = f"{settings.UPDATER_V2['ROUTING_KEY_TO_UPDATER_V2']}"
    exchange = Exchange(settings.UPDATER_V2['EXCHANGE_TO_UPDATER_V2'], type='topic')
    pusher = RabbitMQPusher()

    settings_data = {
        "url": f"/documents/guest-book-settings/{str(housing_id)}/",
        "method": "PATCH",
        "changes": {
            "starting_num": starting_num,
        }
    }
    pusher.send(settings_data, exchange, routing_key)

    logger.info("Guestbook settings task sent.")


def send_document_police_check_in_at(input_data):
    logger.info(f"Send police-guest-checked-in. Data: {input_data}")

    routing_key = f"{settings.UPDATER_V2['ROUTING_KEY_TO_UPDATER_V2']}"
    exchange = Exchange(settings.UPDATER_V2['EXCHANGE_TO_UPDATER_V2'], type='topic')
    pusher = RabbitMQPusher()

    data = {
        "url": "/documents/entry-forms/police-guest-checked-in/",
        "changes":  input_data
    }
    pusher.send(data, exchange, routing_key)

    logger.info("police-guest-checked-in data sent to documents")


def send_contract_task(input_data):
    logger.info(f"Send contract task. Data: {input_data}")

    routing_key = f"{settings.UPDATER_V2['ROUTING_KEY_TO_UPDATER_V2']}"
    exchange = Exchange(settings.UPDATER_V2['EXCHANGE_TO_UPDATER_V2'], type='topic')
    pusher = RabbitMQPusher()

    contract_data = {
        "url": "/documents/contracts/",
        "method": "POST",
        "changes":  input_data
    }
    pusher.send(contract_data, exchange, routing_key)

    logger.info("Contract task sent.")


def send_contract_retrieve_and_create_task(input_data):
    logger.info(f"Send contract task. Data: {input_data}")

    routing_key = f"{settings.UPDATER_V2['ROUTING_KEY_TO_UPDATER_V2']}"
    exchange = Exchange(settings.UPDATER_V2['EXCHANGE_TO_UPDATER_V2'], type='topic')
    pusher = RabbitMQPusher()

    contract_data = {
        "url": "/documents/contracts/retrieve-and-create/",
        "method": "POST",
        "changes":  input_data
    }
    pusher.send(contract_data, exchange, routing_key)

    logger.info("Contract task sent.")


def send_contract_deleted_reservation(input_data):
    logger.info(f"Send deleted reservation event. Data: {input_data}")

    routing_key = f"{settings.UPDATER_V2['ROUTING_KEY_TO_UPDATER_V2']}"
    exchange = Exchange(settings.UPDATER_V2['EXCHANGE_TO_UPDATER_V2'], type='topic')
    pusher = RabbitMQPusher()

    entry_form_data = {
        "url": "/documents/contracts/deleted-reservation/",
        "method": "POST",
        "changes": input_data
    }
    pusher.send(entry_form_data, exchange, routing_key)

    logger.info("Deleted reservation event sent in contracts.")


def send_contract_restored_reservation(input_data):
    logger.info(f"Send restored reservation event. Data: {input_data}")

    routing_key = f"{settings.UPDATER_V2['ROUTING_KEY_TO_UPDATER_V2']}"
    exchange = Exchange(settings.UPDATER_V2['EXCHANGE_TO_UPDATER_V2'], type='topic')
    pusher = RabbitMQPusher()

    entry_form_data = {
        "url": "/documents/contracts/restored-reservation/",
        "method": "POST",
        "changes": input_data
    }
    pusher.send(entry_form_data, exchange, routing_key)

    logger.info("Restored reservation event sent in contracts.")


def send_entry_form_deleted_guest(input_data):
    logger.info(f"Send deleted reservation event. Data: {input_data}")

    routing_key = f"{settings.UPDATER_V2['ROUTING_KEY_TO_UPDATER_V2']}"
    exchange = Exchange(settings.UPDATER_V2['EXCHANGE_TO_UPDATER_V2'], type='topic')
    pusher = RabbitMQPusher()

    entry_form_data = {
        "url": "/documents/entry-forms/deleted-guest/",
        "method": "POST",
        "changes": input_data
    }
    pusher.send(entry_form_data, exchange, routing_key)

    logger.info("Deleted guest event sent.")


def send_contract_housings_restored(input_data):
    logger.info(f"Send housing restored event. Data: {input_data}")

    routing_key = f"{settings.UPDATER_V2['ROUTING_KEY_TO_UPDATER_V2']}"
    exchange = Exchange(settings.UPDATER_V2['EXCHANGE_TO_UPDATER_V2'], type='topic')
    pusher = RabbitMQPusher()

    entry_form_data = {
        "url": "/documents/contracts/housings-restored/",
        "method": "POST",
        "changes": input_data
    }
    pusher.send(entry_form_data, exchange, routing_key)

    logger.info("Housing restored event sent.")


def send_contract_housing_deactivated(input_data):
    logger.info(f"Send housing deactivated event. Data: {input_data}")

    routing_key = f"{settings.UPDATER_V2['ROUTING_KEY_TO_UPDATER_V2']}"
    exchange = Exchange(settings.UPDATER_V2['EXCHANGE_TO_UPDATER_V2'], type='topic')
    pusher = RabbitMQPusher()

    entry_form_data = {
        "url": "/documents/contracts/hide-deactivated-housing-documents/",
        "method": "POST",
        "changes": input_data
    }
    pusher.send(entry_form_data, exchange, routing_key)

    logger.info("Housing deactivated event sent.")


def send_new_guest_to_cloudbeds(reservation_id, input_data):
    data = {
        'url': f"/cloudbeds/reservations/{reservation_id}/add_guest/",
        "changes": input_data
    }

    logger.info(f"Send new guest to cloudbeds> Data: {data}")

    routing_key = f"{settings.UPDATER_V2['ROUTING_KEY_TO_UPDATER_V2']}"
    exchange = Exchange(settings.UPDATER_V2['EXCHANGE_TO_UPDATER_V2'], type='topic')
    pusher = RabbitMQPusher()
    pusher.send(data, exchange, routing_key)

    logger.info("Send new guest to cloudbeds> sent")


def send_task_to_police_worker(input_data, rk_postfix: str, priority=0):
    logger.info(f"Started task to police worker with rk_postfix: {rk_postfix}.")

    if hasattr(rk_postfix, 'option'):
        rk_postfix = rk_postfix.option

    routing_key = f"{settings.POLICE_WORKERS['ROUTING_KEY_TO_POLICE_REGISTRATION']}_{rk_postfix}"
    exchange = Exchange(settings.POLICE_WORKERS['EXCHANGE_TO_POLICE_REGISTRATION'], type='topic')
    pusher = RabbitMQPusher()

    pusher.send(input_data, exchange, routing_key, priority=priority)
    logger.info(f"Task sent to police worker with routing_key: {routing_key}; exchange: {exchange}")


def send_task_to_stat_worker(data, routing_key):
    logger.info(f'Send task to stat worker with routing_key: {routing_key}')
    exchange = Exchange(settings.STAT_WORKERS['EXCHANGE_TO_STAT_REGISTRATION'], type='topic')
    pusher = RabbitMQPusher()
    pusher.send(data, exchange, routing_key)


def send_ntak_task(input_data, housing_id):

    routing_key = f"{settings.UPDATER_V2['ROUTING_KEY_TO_UPDATER_V2']}"
    exchange = Exchange(settings.UPDATER_V2['EXCHANGE_TO_UPDATER_V2'], type='topic')
    pusher = RabbitMQPusher()

    ntak_event_data = {
        "url": f"/ntak/housings/{housing_id}/process-ntak-reservation/",
        "method": "POST",
        "changes":  input_data
    }
    pusher.send(ntak_event_data, exchange, routing_key)

    logger.info("NTAK task sent.")


def send_ntak_payments_task(input_data):
    logger.info(f"Send ntak payments. Data: {input_data}")

    routing_key = f"{settings.UPDATER_V2['ROUTING_KEY_TO_UPDATER_V2']}"
    exchange = Exchange(settings.UPDATER_V2['EXCHANGE_TO_UPDATER_V2'], type='topic')
    pusher = RabbitMQPusher()

    ntak_event_data = {
        "url": "/ntak/periods/process-payments/",
        "method": "POST",
        "changes": input_data
    }
    pusher.send(ntak_event_data, exchange, routing_key)

    logger.info("NTAK payments task sent.")


def send_email_to_the_queue(instance, prepare_function):
    """Deprecated: use celery task SendAutoEmailsTask."""
    routing_key = 'to_email_builder'
    exchange = Exchange('exchange_to_email_builder', type='direct')
    queue = Queue(
        'queue_to_email_builder',
        exchange,
        routing_key=routing_key,
    )
    pusher = RabbitMQPusher()

    message = prepare_function(instance)

    pusher.send(message, exchange, routing_key, queue)
    logger.info(f"{instance._meta.object_name} id: {instance.id} sent to email workers")


def send_guesty_task(input_data, reservation_external_id):
    data = {
        # reservation or guest
        'url': f"/guesty/reservations/{reservation_external_id}/send-note/?token={settings.GUESTY_SERVICE_TOKEN}",
        "changes": input_data,
    }

    logger.info(f"Send Guesty task. Data: {data}")

    routing_key = f"{settings.UPDATER_V2['ROUTING_KEY_TO_UPDATER_V2']}"
    exchange = Exchange(settings.UPDATER_V2['EXCHANGE_TO_UPDATER_V2'], type='topic')
    pusher = RabbitMQPusher()
    pusher.send(data, exchange, routing_key)

    logger.info("Guesty task sent.")


def send_guesty_2_task(input_data, url=None):
    data = {
        # reservation or guest
        'method': 'POST',
        'url': url or '/pms-integrations/guesty/send-note/',
        'changes': input_data,
    }

    logger.info(f'Send Guesty task. Data: {data}')

    routing_key = f'{settings.UPDATER_V2["ROUTING_KEY_TO_UPDATER_V2"]}'
    exchange = Exchange(settings.UPDATER_V2['EXCHANGE_TO_UPDATER_V2'], type='topic')
    pusher = RabbitMQPusher()
    pusher.send(data, exchange, routing_key)

    logger.info('Guesty task sent.')


def send_bookingsync_task(bookingsync_input_data, reservation_external_id):
    data = {
        # reservation or guest
        'url': f"/bookingsync/reservations/{reservation_external_id}/updated-guest/"
               f"?token={settings.BOOKINGSYNC_SERVICE_TOKEN}",
        "changes": bookingsync_input_data,
    }

    logger.info(f"Send BookingSync task. Data: {data}")

    routing_key = f"{settings.UPDATER_V2['ROUTING_KEY_TO_UPDATER_V2']}"
    exchange = Exchange(settings.UPDATER_V2['EXCHANGE_TO_UPDATER_V2'], type='topic')
    pusher = RabbitMQPusher()
    pusher.send(data, exchange, routing_key)

    logger.info("BookingSync task sent.")


def send_mews_task(mews_input_data, reservation_external_id):
    data = {
        # reservation or guest
        'url': f"/mews/reservations/{reservation_external_id}/updated-guest/"
               f"?token={settings.MEWS_SERVICE_TOKEN}",
        "changes": mews_input_data,
    }

    logger.info(f"Send Mews task. Data: {data}")

    routing_key = f"{settings.UPDATER_V2['ROUTING_KEY_TO_UPDATER_V2']}"
    exchange = Exchange(settings.UPDATER_V2['EXCHANGE_TO_UPDATER_V2'], type='topic')
    pusher = RabbitMQPusher()
    pusher.send(data, exchange, routing_key)

    logger.info("Mews task sent.")


def send_apaleo_task(apaleo_input_data, reservation_external_id):
    data = {
        'url': f"/apaleo/reservations/{reservation_external_id}/updated-guest/"
               f"?token={settings.APALEO_SERVICE_TOKEN}",
        'changes': apaleo_input_data,
    }

    logger.info(f'Send Apaleo task. Data: {data}')

    routing_key = f"{settings.UPDATER_V2['ROUTING_KEY_TO_UPDATER_V2']}"
    exchange = Exchange(settings.UPDATER_V2['EXCHANGE_TO_UPDATER_V2'], type='topic')
    pusher = RabbitMQPusher()
    pusher.send(data, exchange, routing_key)

    logger.info("Apaleo task sent.")


def send_cloudbeds_task(cloudbeds_input_data, reservation_external_id):
    data = {
        # reservation or guest
        'url': f"/cloudbeds/reservations/{reservation_external_id}/updated-guest/"
               f"?token={settings.CLOUDBEDS_SERVICE_TOKEN}",
        "changes": cloudbeds_input_data,
    }

    logger.info(f"Send Cloudbeds task. Data: {data}")

    routing_key = f"{settings.UPDATER_V2['ROUTING_KEY_TO_UPDATER_V2']}"
    exchange = Exchange(settings.UPDATER_V2['EXCHANGE_TO_UPDATER_V2'], type='topic')
    pusher = RabbitMQPusher()
    pusher.send(data, exchange, routing_key)

    logger.info("Temp stop send tasks to Cloudbeds.")


def send_eviivo_task(eviivo_input_data, reservation_external_id):
    data = {
        # reservation or guest
        'url': f"/eviivo/reservations/{reservation_external_id}/updated-guest/"
               f"?token={settings.EVIIVO_SERVICE_TOKEN}",
        "changes": eviivo_input_data,
    }

    logger.info(f"Send Eviivo task. Data: {data}")

    routing_key = f"{settings.UPDATER_V2['ROUTING_KEY_TO_UPDATER_V2']}"
    exchange = Exchange(settings.UPDATER_V2['EXCHANGE_TO_UPDATER_V2'], type='topic')
    pusher = RabbitMQPusher()
    pusher.send(data, exchange, routing_key)

    logger.info("Eviivo task sent.")


def send_ulyses_task(ulyses_input_data, reservation_external_id):
    data = {
        'url': f"/ulyses/reservations/{reservation_external_id}/updated-guest/"
               f"?token={settings.ULYSES_SERVICE_TOKEN}",
        "changes": ulyses_input_data,
    }

    logger.info(f"Send Ulyses task. Data: {data}")

    routing_key = f"{settings.UPDATER_V2['ROUTING_KEY_TO_UPDATER_V2']}"
    exchange = Exchange(settings.UPDATER_V2['EXCHANGE_TO_UPDATER_V2'], type='topic')
    pusher = RabbitMQPusher()
    pusher.send(data, exchange, routing_key)

    logger.info("Ulyses task sent.")


def send_task_to_guesty_worker(input_data):

    routing_key = settings.GUESTY_WORKER['ROUTING_KEY_TO_GUESTY_WORKER']
    exchange = Exchange(settings.GUESTY_WORKER['EXCHANGE_TO_GUESTY_WORKER'], type='topic')
    pusher = RabbitMQPusher()

    pusher.send(input_data, exchange, routing_key)
    logger.info(f"Task sent to guesty worker. Data {input_data}")


def send_task_to_lodgify_worker(input_data):

    routing_key = settings.LODGIFY_WORKER['ROUTING_KEY_TO_LODGIFY_WORKER']
    exchange = Exchange(settings.LODGIFY_WORKER['EXCHANGE_TO_LODGIFY_WORKER'], type='topic')
    pusher = RabbitMQPusher()

    pusher.send(input_data, exchange, routing_key)
    logger.info(f"Task sent to lodgify worker. Data {input_data}")


def send_task_to_villas_365_worker(input_data, reservation_external_id, core_housing_id: Optional[str]):
    data = {
        # reservation or guest
        'url': f"/villas-365/reservations/{reservation_external_id}/updated-reservation/"
               f"?token={settings.VILLAS_365_SERVICE_TOKEN}&core_housing_id={core_housing_id}",
        "changes": input_data,
    }

    logger.info(f"Send BookingSync task. Data: {data}")

    routing_key = f"{settings.UPDATER_V2['ROUTING_KEY_TO_UPDATER_V2']}"
    exchange = Exchange(settings.UPDATER_V2['EXCHANGE_TO_UPDATER_V2'], type='topic')
    pusher = RabbitMQPusher()
    pusher.send(data, exchange, routing_key)


def send_new_pms_service_task(input_data):
    """
    Creates task on on new PMS service.
    """
    data = {
        # reservation or guest
        'method': 'POST',
        'url': PMS_INTEGRATION_SYNC_TASK_URL,
        'changes': input_data,
    }
    routing_key = f"{settings.UPDATER_V2['ROUTING_KEY_TO_UPDATER_V2']}_pms"
    exchange = Exchange(settings.UPDATER_V2['EXCHANGE_TO_UPDATER_V2'], type='topic')
    pusher = RabbitMQPusher()
    pusher.send(data, exchange, routing_key)
    logger.info(f"{input_data['pms_provider']} task sent to updater. Data: {data}")


def send_task_to_vreasy_worker(input_data):

    routing_key = settings.VREASY_WORKER['ROUTING_KEY_TO_VREASY_WORKER']
    exchange = Exchange(settings.VREASY_WORKER['EXCHANGE_TO_VREASY_WORKER'], type='topic')
    pusher = RabbitMQPusher()

    pusher.send(input_data, exchange, routing_key)
    logger.info(f"Task sent to vreasy worker. Data {input_data}")


def send_email_creation_task(input_data):
    logger.info(f"Send data to updater. Data: {input_data}")

    routing_key = f"{settings.UPDATER_V2['ROUTING_KEY_TO_UPDATER_V2']}"
    exchange = Exchange(settings.UPDATER_V2['EXCHANGE_TO_UPDATER_V2'], type='topic')
    pusher = RabbitMQPusher()

    email_data = {
        "url": "/auto-email-notifications/",
        "method": "POST",
        "changes":  input_data
    }
    pusher.send(email_data, exchange, routing_key)

    logger.info("Email task sent.")


def send_reservations_aggregated_status_recalculation_task(input_data):
    logger.info(f"Send data to updater. Data: {input_data}")

    routing_key = f"{settings.UPDATER_V2['ROUTING_KEY_TO_UPDATER_V2']}"
    exchange = Exchange(settings.UPDATER_V2['EXCHANGE_TO_UPDATER_V2'], type='topic')
    pusher = RabbitMQPusher()

    email_data = {
        "url": "/reservations-statuses/",
        "method": "POST",
        "changes":  input_data
    }
    pusher.send(email_data, exchange, routing_key)

    logger.info("Email task sent.")


def send_reservations_unlock_links_task(input_data: Dict):
    logger.info(f"Send data to updater. Data: {input_data}")

    routing_key = f"{settings.UPDATER_V2['ROUTING_KEY_TO_UPDATER_V2']}"
    exchange = Exchange(settings.UPDATER_V2['EXCHANGE_TO_UPDATER_V2'], type='topic')
    pusher = RabbitMQPusher()

    email_data = {
        "url": "/reservations-unlock-links/",
        "method": "POST",
        "changes":  input_data
    }
    pusher.send(email_data, exchange, routing_key)

    logger.info("Unlock links task sent.")


def send_updated_user(origin: Origin, user_id: UUID, data):
    host = origin.option.lower().replace('_', '-')
    data = {
        'url': f'/{host}/users/{user_id.hex}/',
        'method': 'PATCH',
        'changes': data,
    }

    logger.info(f'Send user update task. Data: {data}')

    routing_key = settings.UPDATER_V2['ROUTING_KEY_TO_UPDATER_V2']
    exchange = Exchange(settings.UPDATER_V2['EXCHANGE_TO_UPDATER_V2'], type='topic')
    pusher = RabbitMQPusher()
    pusher.send(data, exchange, routing_key)


def send_update_email_to_documents(look_up_field: str, data):
    data = {
        'url': f'http://localhost:8000/documents/users/{look_up_field}/update-email/',
        'method': 'POST',
        'changes': data,
    }

    logger.info(f'Send user update task. Data: {data}')

    routing_key = settings.UPDATER_V2['ROUTING_KEY_TO_UPDATER_V2']
    exchange = Exchange(settings.UPDATER_V2['EXCHANGE_TO_UPDATER_V2'], type='topic')
    pusher = RabbitMQPusher()
    pusher.send(data, exchange, routing_key)


def send_task_to_salesforce_worker(input_data):
    routing_key = settings.SALESFORCE_WORKER['ROUTING_KEY_TO_SALESFORCE_WORKER']
    exchange = Exchange(settings.SALESFORCE_WORKER['EXCHANGE_TO_SALESFORCE_WORKER'], type='topic')
    pusher = RabbitMQPusher()

    pusher.send(input_data, exchange, routing_key)
    logger.info(f"Task sent to salesforce worker. Data {input_data}")


def send_task_to_payments_worker(
    input_data,
    rk_postfix: str,
    payments_settings_version: PaymentsSettingsVersion = PaymentsSettingsVersion.VERSION_1,
):
    if payments_settings_version != PaymentsSettingsVersion.VERSION_1:
        logger.info(
            f"Task sender v1 disabled payments settings with version {payments_settings_version.option}"
        )
        return

    logger.info(f"Started task to payments worker with rk_postfix: {rk_postfix}. Data {input_data}")

    if hasattr(rk_postfix, 'option'):
        rk_postfix = rk_postfix.option

    routing_key = f"{settings.PAYMENTS_WORKER['ROUTING_KEY_TO_PAYMENTS_WORKER']}_{rk_postfix}"
    exchange = Exchange(settings.PAYMENTS_WORKER['EXCHANGE_TO_PAYMENTS_WORKER'], type='topic')
    pusher = RabbitMQPusher()

    pusher.send(input_data, exchange, routing_key)
    logger.info(f"Task sent to payments worker, routing_key: {routing_key}; exchange: {exchange}. Data {input_data}")


def send_task_to_payments_worker_v2(
    task_data,
    payments_settings_version: PaymentsSettingsVersion = PaymentsSettingsVersion.VERSION_2,
):
    if payments_settings_version != PaymentsSettingsVersion.VERSION_2:
        logger.info(
            f"Task sender v2 disabled payments settings with version {payments_settings_version.option}"
        )
        return

    kwargs = {
        "routing_key": settings.PAYMENTS_WORKER_V2["ROUTING_KEY_TO_PAYMENTS_WORKER_V2"],
        "exchange": Exchange(
            settings.PAYMENTS_WORKER_V2["EXCHANGE_TO_PAYMENTS_WORKER_V2"], type="topic"
        ),
    }
    logger.info(f"Task sent to payments worker V2 {kwargs}.\nData: {task_data}")

    pusher = RabbitMQPusher()
    pusher.send(message=task_data, **kwargs)


def send_guestbook_generation_task(housing_id: str):
    logger.info(f"Send guestbook generation task. Data: {housing_id}")

    routing_key = f"{settings.UPDATER_V2['ROUTING_KEY_TO_UPDATER_V2']}"
    exchange = Exchange(settings.UPDATER_V2['EXCHANGE_TO_UPDATER_V2'], type='topic')
    pusher = RabbitMQPusher()

    settings_data = {
        "url": "/documents/guest-book-generation-task/",
        "method": "POST",
        "changes": {
            "housing_id": housing_id,
        }
    }
    pusher.send(settings_data, exchange, routing_key)

    logger.info("Guestbook generation task sent.")


def send_task_to_hubspot_worker(input_data):
    routing_key = settings.HUBSPOT_WORKER['ROUTING_KEY_TO_HUBSPOT_WORKER']
    exchange = Exchange(settings.HUBSPOT_WORKER['EXCHANGE_TO_HUBSPOT_WORKER'], type='topic')
    pusher = RabbitMQPusher()

    pusher.send(input_data, exchange, routing_key)
    logger.info("Task sent to hubspot worker.")


def send_task_to_amplitude_worker(input_data):
    routing_key = settings.AMPLITUDE_WORKER['ROUTING_KEY_TO_AMPLITUDE_WORKER']
    exchange = Exchange(settings.AMPLITUDE_WORKER['EXCHANGE_TO_AMPLITUDE_WORKER'], type='topic')
    pusher = RabbitMQPusher()

    pusher.send(input_data, exchange, routing_key)
    logger.info('Task sent to amplitude_worker')


def send_user_report_task(input_data: dict):
    logger.info("Send user report task.")
    routing_key = settings.USER_REPORT_WORKER['ROUTING_KEY_TO_USER_REPORT_WORKER']
    exchange = Exchange(settings.USER_REPORT_WORKER['EXCHANGE_TO_USER_REPORT_WORKER'], type='topic')
    pusher = RabbitMQPusher()

    pusher.send(input_data, exchange, routing_key)
    logger.info("Task sent to user report worker")


def send_hook_event(event_type, input_data):
    logger.info(f"Send {event_type}")
    exchange = Exchange(settings.EVENT_HOOK_EXCHANGE, type='direct')
    pusher = RabbitMQPusher()
    pusher.send(input_data, exchange, routing_key=event_type)


def send_custom_email(message):
    """Deprecated: use celery task SendCustomEmailsTask."""
    routing_key = settings.EMAIL_SENDER_ROUTING_KEY
    exchange = Exchange(settings.EMAIL_SENDER_EXCHANGE, type='direct')
    queue = Queue(
        settings.EMAIL_SENDER_QUEUE,
        exchange,
        routing_key=routing_key,
    )
    pusher = RabbitMQPusher()

    pusher.send(message, exchange, routing_key, queue)
    logger.info("Custom email sent to email sender")


def send_create_payment_pms_task(pms_name: Origin, user_id: str, input_data: dict):
    pms_name_lower = pms_name.option.lower()
    logger.info(f"Send task create payment in PMS {pms_name_lower} service {input_data}")

    routing_key = f"{settings.UPDATER_V2['ROUTING_KEY_TO_UPDATER_V2']}"
    exchange = Exchange(settings.UPDATER_V2['EXCHANGE_TO_UPDATER_V2'], type='topic')
    pusher = RabbitMQPusher()

    data = {
        "url": f"/{pms_name_lower}/users/{user_id}/create-pms-payment/",
        "method": "POST",
        "changes":  input_data
    }
    pusher.send(data, exchange, routing_key)

    logger.info(f"Create payment in PMS {pms_name_lower} service task sent")


def send_user_subscription_changed_task_to_pms_integration_svc(
    user_id: UUID,
    subscription_status_option: str,
    origin: Origin
):
    """
        Pms integration svc should store user subscription status;
    Integrations will work only still user got 'ACTIVE' or 'TRIAL'
    subscription statuses.

        All pms should contain action in 'users' endpoint,  named
    '/users/{user core id}/subscription/', handling data:

        {"subscription_status": {valid SubscriptionStatus choice}}

    """
    if not subscription_status_option:
        return

    pms_svc_endpoint = origin.option.lower().replace('_', '-')
    data = {
        'url': f"/{pms_svc_endpoint}/users/{user_id.hex}/subscriptions/",
        "method": "PATCH",
        "changes": {'subscription_status': subscription_status_option}
    }

    logger.info(f"Send user subscription changed task for pms {pms_svc_endpoint}, user id: {user_id.hex}, data: {data}")

    routing_key = f"{settings.UPDATER_V2['ROUTING_KEY_TO_UPDATER_V2']}"
    exchange = Exchange(settings.UPDATER_V2['EXCHANGE_TO_UPDATER_V2'], type='topic')
    pusher = RabbitMQPusher()
    pusher.send(data, exchange, routing_key)

    logger.info("User subscription changed task for pms sent")


def send_event_to_invalidator(payload: List[Dict[str, Any]]):
    exchange = Exchange(settings.CACHE_INVALIDATOR_EXCHANGE)
    rk = settings.CACHE_INVALIDATOR_ROUTING_KEY

    pusher = RabbitMQPusher()
    pusher.send(message=payload, exchange=exchange, routing_key=rk)
    logger.info(f"Events set {payload} are sent to invalidator")


def send_update_lock_task_to_hostaway(input_data: dict, reservation_external_id: str):
    logger.info(f"Send update lock task to Hostaway service {input_data}")

    routing_key = f"{settings.UPDATER_V2['ROUTING_KEY_TO_UPDATER_V2']}"
    exchange = Exchange(settings.UPDATER_V2['EXCHANGE_TO_UPDATER_V2'], type='topic')
    pusher = RabbitMQPusher()

    data = {
        "url": f"/hostaway/reservations/{reservation_external_id}/locks/",
        "method": "POST",  # updater can't send PUTs(
        "changes":  input_data
    }
    pusher.send(data, exchange, routing_key)

    logger.info("Update lock task to Hostaway service sent")


def send_create_guest_payment_invoice_task(guest_payment):
    from entities.guest.serializers.v3 import GuestSerializer
    from entities.guest_payments.serializers.v3 import GuestPaymentAccountSerializer, GuestPaymentSerializer

    def prepare_data_to_invoice_gen() -> dict:
        leader = guest_payment.reservation.guest_group.leader
        leader_data = GuestSerializer(instance=leader).data if leader else None
        manager = guest_payment.reservation._housing_manager
        guest_payment_account = getattr(guest_payment.reservation, 'guest_payment_account', None)
        if guest_payment_account:
            guest_payment_account = GuestPaymentAccountSerializer(instance=guest_payment_account).data

        extra_data = {
            "guest_payment_data": GuestPaymentSerializer(instance=guest_payment).data,
            "user_id": manager.id.hex,
            "user_email": manager.email,
            "guest_id": leader.id.hex if leader else None,
            "guest_data": leader_data,
            "guest_payment_account": guest_payment_account,
        }
        return {
            "guest_payment_id": guest_payment.id.hex,
            "reservation_id": guest_payment.reservation.id.hex,
            "extra_data": extra_data,
        }

    input_data = prepare_data_to_invoice_gen()
    logger.info(f"Send task to generate guest-payment-invoice with data: {input_data}")

    routing_key = f"{settings.UPDATER_V2['ROUTING_KEY_TO_UPDATER_V2']}"
    exchange = Exchange(settings.UPDATER_V2['EXCHANGE_TO_UPDATER_V2'], type='topic')
    pusher = RabbitMQPusher()

    data = {
        "url": "/documents/guest-payment-invoice-tasks/",
        "method": "POST",
        "changes":  input_data
    }
    pusher.send(data, exchange, routing_key)

    logger.info("Generate guest-payment-invoice task sent")


def send_housing_added_to_siteminder_task(input_data):
    logger.info(f"Send created housing to Site Minder. Data: {input_data}")

    routing_key = f"{settings.UPDATER_V2['ROUTING_KEY_TO_UPDATER_V2']}"
    exchange = Exchange(settings.UPDATER_V2['EXCHANGE_TO_UPDATER_V2'], type='topic')
    pusher = RabbitMQPusher()

    settings_data = {
        "url": f"/siteminder/housings/?token={settings.SITEMINDER_SERVICE_TOKEN}",
        "method": "POST",
        "changes": input_data
    }
    pusher.send(settings_data, exchange, routing_key)

    logger.info("Created housing to Site Minder task sent.")


def send_guest_payment_upselling_task(input_data):
    logger.info(f"Send guest_payment to upselling. Data: {input_data}")

    routing_key = f"{settings.UPDATER['ROUTING_KEY_TO_UPDATER']}"
    exchange = Exchange(settings.UPDATER['EXCHANGE_TO_UPDATER'], type='topic')
    pusher = RabbitMQPusher()

    settings_data = {
        "url": "/upselling/deals/confirm-payment/",
        "method": "POST",
        "changes": input_data
    }
    pusher.send(settings_data, exchange, routing_key)

    logger.info("Guest payment to upselling task sent.")


def send_update_entity_upselling_task(input_data, url):
    logger.info(f"Send updated entity to upselling. Data: {input_data}")

    routing_key = f"{settings.UPDATER_V2['ROUTING_KEY_TO_UPDATER_V2']}"
    exchange = Exchange(settings.UPDATER_V2['EXCHANGE_TO_UPDATER_V2'], type='topic')
    pusher = RabbitMQPusher()

    settings_data = {
        "url": url,  # /upselling/deals/update-guest-name/ or /upselling/deals/update-housing-name/
        "method": "POST",
        "changes": input_data
    }
    pusher.send(settings_data, exchange, routing_key)

    logger.info("Update entity to upselling task sent.")


def send_create_update_reservation_smart_locks(reservation_id: UUID, action_url: str):
    data = {
        'url': f"/reservations/{reservation_id.hex}/{action_url}/",
        "method": "POST",
        "changes": {},
    }

    logger.info(f"Send create/update reservation smart locks task. Data: {data}")

    routing_key = f"{settings.UPDATER['ROUTING_KEY_TO_UPDATER']}"
    exchange = Exchange(settings.UPDATER['EXCHANGE_TO_UPDATER'], type='topic')
    pusher = RabbitMQPusher()
    pusher.send(data, exchange, routing_key)


def send_generate_admin_housings_report(data_to_send):
    logger.info(f"send_generate_admin_housings_report. Data: {data_to_send}")

    routing_key = f"{settings.ADMIN_HOUSINGS_REPORT_WORKER['ROUTING_KEY_TO_ADMIN_HOUSINGS_REPORT_WORKER']}"
    exchange = Exchange(
        settings.ADMIN_HOUSINGS_REPORT_WORKER['EXCHANGE_TO_ADMIN_HOUSINGS_REPORT_WORKER'],
        type='topic'
    )
    pusher = RabbitMQPusher()
    pusher.send(data_to_send, exchange, routing_key)

    logger.info("generate_admin_housings task sent.")


def send_generate_admin_upselling_report(data_to_send):
    logger.info(f"send_generate_admin_upselling_report. Data: {data_to_send}")

    routing_key = f"{settings.ADMIN_UPSELLING_REPORT_WORKER['ROUTING_KEY_TO_ADMIN_UPSELLING_REPORT_WORKER']}"
    exchange = Exchange(
        settings.ADMIN_UPSELLING_REPORT_WORKER['EXCHANGE_TO_ADMIN_UPSELLING_REPORT_WORKER'],
        type='topic'
    )
    pusher = RabbitMQPusher()
    pusher.send(data_to_send, exchange, routing_key)

    logger.info("generate_admin_upselling task sent.")


def send_task_to_documents_creator(data_to_send):
    """
    Send task to documents creator worker.
    The repo of this worker is at https://github.com/invibeme/chekin-worker-documents-creator.
    """
    logger.info(f"send_task_to_documents_creator. Data: {data_to_send}")

    routing_key = settings.DOCUMENTS_CREATOR_WORKER['ROUTING_KEY_TO_DOCUMENTS_CREATOR_WORKER']
    exchange = Exchange(settings.DOCUMENTS_CREATOR_WORKER['EXCHANGE_TO_DOCUMENTS_CREATOR_WORKER'], type='topic')
    pusher = RabbitMQPusher()
    pusher.send(data_to_send, exchange, routing_key)

    logger.info("send_task_to_documents_creator task sent.")


def send_hpi_task(data_to_send):
    """
    Send task to HPI worker.
    The repo of this worker is at https://github.com/invibeme/chekin-worker-hpi
    """
    logger.info(f"send_task_hpi_worker. Data: {data_to_send}")

    routing_key = settings.HPI_WORKER['ROUTING_KEY_TO_HPI_WORKER']
    exchange = Exchange(settings.HPI_WORKER['EXCHANGE_TO_HPI_WORKER'], type='topic')
    pusher = RabbitMQPusher()
    pusher.send(data_to_send, exchange, routing_key)

    logger.info("send_hpi_task task sent.")


def send_guestbook_housing_deactivated(input_data):
    logger.info(f"Send housing deactivated event. Data: {input_data}")

    routing_key = f"{settings.UPDATER_V2['ROUTING_KEY_TO_UPDATER_V2']}"
    exchange = Exchange(settings.UPDATER_V2['EXCHANGE_TO_UPDATER_V2'], type='topic')
    pusher = RabbitMQPusher()

    entry_form_data = {
        "url": "/documents/guest-books/hide-deactivated-housing-documents/",
        "method": "POST",
        "changes": input_data
    }
    pusher.send(entry_form_data, exchange, routing_key)

    logger.info("Housing deactivated event sent.")
