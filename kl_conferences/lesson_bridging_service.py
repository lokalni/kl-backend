from django.contrib.auth.models import User
from django.db import transaction

from kl_conferences.bbb_api import BigBlueButtonAPI, RoomAlreadyExistsError
from kl_conferences.models import ServerNode, Room


@transaction.atomic
def start_lesson(group, moderator):
    """"""
    server = ServerNode.assign_server(group=group)
    room, _ = Room.objects.get_or_create(server_node=server, group=group)

    api = BigBlueButtonAPI(server.hostname, server.api_secret)

    try:
        bbb_room = api.create_room(
            meeting_id=room.bbb_meeting_id,
            welcome_msg='Witojcie',
            attendee_secret=User.objects.make_random_password(),
            moderator_secret=User.objects.make_random_password(),
        )
        room.attendee_secret = bbb_room.attendeePW
        room.moderator_secret = bbb_room.moderatorPW
        room.save()
    except RoomAlreadyExistsError:
        pass

    redirect_url = api.join(
        meeting_id=room.bbb_meeting_id,
        password=room.moderator_secret,
        join_as=moderator.display_name,
        assing_user_id=moderator.uuid,
    )
    return redirect_url
