import logging

from django.contrib.auth.models import User
from django.db import transaction

from kl_conferences.bbb_api import BigBlueButtonAPI, RoomAlreadyExistsError, BBBServerUnreachable
from kl_conferences.models import ServerNode, Room


logger = logging.getLogger()

CHECK_SERVERS_CNT = 2


def start_lesson(group, moderator):
    """Attempt to start a lesson, keep in mind that server might be down."""
    for _ in range(CHECK_SERVERS_CNT):
        try:
            return _start_lesson(group, moderator)
        except BBBServerUnreachable as e:
            logger.exception(f'BBB Server unreachable, disconnecting from pool.')
            server = ServerNode.objects.get(hostname=e.hostname)
            server.disconnect_from_pool()

    raise ServerNode.DoesNotExist


def get_or_create_room(group):
    """"Returns active room for a group or assigns new one."""
    room = group.last_meeting_room()

    # Room already exists, got to probe it
    if room:
        server = room.server_node
        api = BigBlueButtonAPI(server.hostname, server.api_secret)

        if api.is_meeting_running(room.bbb_meeting_id):
            logger.info(f'Meeting for group {group} already in progress.')
            return room

    # Room not found or not active, assign new from refreshed pool
    if not room:
        server = ServerNode.assign_server(group=group)
        room, _ = Room.objects.get_or_create(server_node=server, group=group)

    return room


@transaction.atomic
def _start_lesson(group, moderator):
    room = get_or_create_room(group)
    server = room.server_node
    api = BigBlueButtonAPI(server.hostname, server.api_secret)

    try:
        bbb_room = api.create_room(
            meeting_id=room.bbb_meeting_id,
            attendee_secret=User.objects.make_random_password(),
            moderator_secret=User.objects.make_random_password(),
        )
        room.attendee_secret = bbb_room.attendeePW
        room.moderator_secret = bbb_room.moderatorPW
        room.save()
    except RoomAlreadyExistsError:
        pass

    # Connect to room
    redirect_url = api.get_join_url(
        meeting_id=room.bbb_meeting_id,
        password=room.moderator_secret,
        # TODO - temporary, until RODO is sorted out
        join_as='Prowadzący',
        # join_as=moderator.display_name,
        assing_user_id=moderator.uuid,
    )
    return redirect_url
