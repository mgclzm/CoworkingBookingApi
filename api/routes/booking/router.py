from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from api.app.dependencies import (
    get_command_mediator,
    get_query_mediator,
    require_access_token,
)
from api.routes.booking.schemas import (
    CreateBookingResponseSchema,
    CreateBookingSchema,
    GetMyBookingsQueryParams,
)
from domain.entities.base import ApplicationException, LogicException
from domain.entities.booking import BookingNotFoundError
from domain.values.booking import BookingConflictError
from logic.commands.booking.booking_commands import (
    CancelBookingCommand,
    ConfirmBookingCommand,
    CreateBookingCommand,
)
from logic.mediator.base import ICommandMediator, IQueryMediator
from logic.queries.booking.booking_queries import GetMyBookingsQuery

booking_router = APIRouter(prefix="/v1", tags=["Booking"])


@booking_router.post(
    "/booking/{booking_id}/confirm",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"description": "Booking successfully confirmed"},
        status.HTTP_401_UNAUTHORIZED: {"description": "User is not authenticated"},
        status.HTTP_403_FORBIDDEN: {
            "description": "Booking doesn`t belong to the authenticated user"
        },
        status.HTTP_404_NOT_FOUND: {"description": "Booking not found"},
        status.HTTP_409_CONFLICT: {"description": "Booking is already confirmed"},
    },
    summary="Endpoint to confirm booking",
)
async def confirm_booking(
    booking_id: str,
    user_id: Annotated[str, Depends(require_access_token)],
    command_mediator: Annotated[ICommandMediator, Depends(get_command_mediator)],
):
    confirm_booking_command = ConfirmBookingCommand(booking_id, user_id)
    try:
        await command_mediator.execute_command(confirm_booking_command)
    except ApplicationException as ex:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=ex.message)
    except LogicException as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
            if isinstance(ex, BookingNotFoundError)
            else status.HTTP_403_FORBIDDEN,
            detail=ex.message,
        )


@booking_router.post(
    "/booking/{booking_id}/cancel",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"description": "Booking successfully cancelled"},
        status.HTTP_401_UNAUTHORIZED: {"description": "User is not authenticated"},
        status.HTTP_403_FORBIDDEN: {
            "description": "Booking doesn`t belong to the authenticated user"
        },
        status.HTTP_404_NOT_FOUND: {"description": "Booking not found"},
        status.HTTP_409_CONFLICT: {"description": "Booking is already cancelled"},
    },
    summary="Endpoint to cancel booking",
)
async def cancel_booking(
    booking_id: str,
    user_id: Annotated[str, Depends(require_access_token)],
    command_mediator: Annotated[ICommandMediator, Depends(get_command_mediator)],
):
    cancel_booking_command = CancelBookingCommand(booking_id, user_id)
    try:
        await command_mediator.execute_command(cancel_booking_command)
    except ApplicationException as ex:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=ex.message)
    except LogicException as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
            if isinstance(ex, BookingNotFoundError)
            else status.HTTP_403_FORBIDDEN,
            detail=ex.message,
        )


@booking_router.post(
    "/booking/{workspace_id}/{workplace_number}",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            "description": "Booking successfully created",
            "model": CreateBookingResponseSchema,
        },
        status.HTTP_401_UNAUTHORIZED: {"description": "User is not authenticated"},
        status.HTTP_404_NOT_FOUND: {"description": "Workspace or workplace not found"},
        status.HTTP_409_CONFLICT: {
            "description": "Its not possible to make booking for this time"
        },
    },
    summary="Endpoint to make a booking, require access token",
)
async def create_booking(
    workspace_id: str,
    workplace_number: int,
    create_booking_schema: CreateBookingSchema,
    user_id: Annotated[str, Depends(require_access_token)],
    command_mediator: Annotated[ICommandMediator, Depends(get_command_mediator)],
):
    create_booking_command = CreateBookingCommand(
        user_id,
        workspace_id,
        workplace_number,
        create_booking_schema.start_time,
        create_booking_schema.end_time,
        create_booking_schema.day,
    )
    try:
        response_model = await command_mediator.execute_command(create_booking_command)
    except LogicException as ex:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT
            if isinstance(ex, BookingConflictError)
            else status.HTTP_404_NOT_FOUND,
            detail=ex.message,
        )
    else:
        return response_model


@booking_router.get(
    "/me/booking",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "description": "Return information about bookings which belongs to authenticated user"
        },
        status.HTTP_401_UNAUTHORIZED: {"description": "User is not authenticated"},
    },
    summary="Endpoint to obtain information about bookings which belongs to authenticated user, require access token",
)
async def get_my_bookings(
    query_params: Annotated[GetMyBookingsQueryParams, Query()],
    user_id: Annotated[str, Depends(require_access_token)],
    query_mediator: Annotated[IQueryMediator, Depends(get_query_mediator)],
):
    get_my_bookings_query = GetMyBookingsQuery(
        query_params.page_number, query_params.page_size, user_id
    )
    response_schemas = await query_mediator.execute_query(get_my_bookings_query)
    return response_schemas
