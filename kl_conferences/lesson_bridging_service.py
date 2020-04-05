from django.contrib.auth.models import User
from django.db import transaction

from kl_conferences.bbb_api import BigBlueButtonAPI, RoomAlreadyExistsError
from kl_conferences.models import ServerNode, Room


def get_group_active_meeting(group):
    room = Room.objects.filter(group=group).last()
    if room:
        server = room.server_node
        api = BigBlueButtonAPI(server.hostname, server.api_secret)
        if api.is_meeting_running(room.bbb_meeting_id):
            return room

    return None


@transaction.atomic
def start_lesson(group, moderator):
    """"""
    room = get_group_active_meeting(group)

    # group does not have running meeting, create one
    if not group:
        server = ServerNode.assign_server(group=group)
        room, _ = Room.objects.get_or_create(server_node=server, group=group)

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

    redirect_url = api.get_join_url(
        meeting_id=room.bbb_meeting_id,
        password=room.moderator_secret,
        join_as=moderator.display_name,
        assing_user_id=moderator.uuid,
    )
    return redirect_url
