import logging

from django.conf import settings
from django.contrib.auth.models import User
from django.db import transaction
from django.utils.timezone import now

from kl_conferences.bbb_api import (
    BigBlueButtonAPI,
    BBBServerUnreachable,
    BBBRequestFailed,
    RoomAlreadyExistsError,
    apibool,
)
from kl_conferences.models import ServerNode, Room
from kl_participants.models import Student


logger = logging.getLogger()


__all__ = ['start_lesson', 'get_student_access_url']


def start_lesson(group, moderator):
    """
    Attempt to start a lesson, keep in mind that server might be down.

    :param group:
    :param moderator:
    :return: redirect url for mod
    """

    for _ in range(settings.NEW_LESSON_TRY_SERVERS_CNT):
        try:
            return _start_lesson(group, moderator)
        except BBBServerUnreachable as e:
            server = ServerNode.objects.get(hostname=e.hostname)
            logger.error(f'BBB Server {server.hostname} unreachable, disconnecting from pool.')
            server.disconnect_from_pool()

    raise ServerNode.DoesNotExist


def _get_or_create_room(group):
    """"Returns active room for a group or assigns new one."""
    room = group.last_meeting_room()

    # Room already exists, got to probe it
    if room:
        server = room.server_node
        api = BigBlueButtonAPI(server.hostname, server.api_secret)

        if api.is_meeting_running(room.bbb_meeting_id):
            logger.info(f'Meeting for group {group} already in progress.')
            return room
        else:
            # Room leftover, clean it from BBB and let assign new
            Room.objects.filter(id=room.id).delete()
            room = None

    # Room not found or not active, assign new from refreshed pool
    if not room:
        server = ServerNode.assign_server(group=group)
        room, _ = Room.objects.get_or_create(server_node=server, group=group)

    return room


@transaction.atomic
def _start_lesson(group, moderator):
    room = _get_or_create_room(group)
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
    logger.debug(f'Mod {moderator.id} start_lesson room {room.id} for {group.display_name}@{server.hostname}')
    return redirect_url


def get_student_access_url(token):
    """
    Get access url for student, perform checks.
    :param token: Student access token
    :return: redirect url for student or None
    """
    # Token & Student
    try:
        student = Student.objects.get(access_token__iexact=token)
        student.last_accessed = now()
        student.save()
    except Student.DoesNotExist:
        logger.warning(f"Token {token} has no associated student.")
        return None

    # Get meeting details
    try:
        lesson = Room.objects.filter(group=student.group).latest('id')

        bbb_api = BigBlueButtonAPI(lesson.server_node.hostname, lesson.server_node.api_secret)
        room_details, attendees = bbb_api.get_meeting_info(lesson.bbb_meeting_id)
    except Room.DoesNotExist:
        logger.warning(f"Token {token} has no associated lesson.")
        return None
    except BBBRequestFailed as e:
        logger.error(f"Unable to fetch meeting {lesson.bbb_meeting_id} info: {e}")
        return None

    # Check: meeeting not running, remove from pool
    if room_details.running != apibool(True):
        logger.error(f"Meeting {lesson.bbb_meeting_id} is not running.")
        return None

    # Check: max sessions for token
    student_sessions = [a.userID for a in attendees].count(student.uuid)
    if student_sessions >= settings.MAX_STUDENT_TOKEN_SESSIONS:
        logger.warning(
            f"Student {student.uuid} token {token} has max number of active sessions.")
        return None

    try:
        return bbb_api.get_join_url(
            meeting_id=lesson.bbb_meeting_id,
            password=lesson.attendee_secret,
            join_as=student.display_name,
            assing_user_id=student.uuid,
        )
    except BBBRequestFailed as e:
        logger.error(f"Unable to fetch redirect url {lesson.bbb_meeting_id}: {e}")
        return None



