"""
Hotel Booking FastAPI Application

A comprehensive REST API for managing hotel rooms and bookings with CRUD operations.
This application provides endpoints to create, read, update, and delete hotel rooms
and bookings with strict validation and filtering capabilities.

Author: AI Assistant
Date: 2025-01-11
"""

from fastapi import FastAPI, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime, date
from enum import Enum
import json
import os

# Data file paths
ROOMS_FILE = "rooms.json"
BOOKINGS_FILE = "bookings.json"

# Error messages
ROOM_NOT_FOUND_MESSAGE = "Room not found"
BOOKING_NOT_FOUND_MESSAGE = "Booking not found"
ROOM_NOT_AVAILABLE_MESSAGE = "Room not available for the selected dates"

# Constants for query parameters
MIN_PRICE_DESC = "Minimum price per night"
MAX_PRICE_DESC = "Maximum price per night"
SORT_ORDER_DESC = "Sort order: asc or desc"


class RoomTypeEnum(str, Enum):
    """Enumeration of room types"""

    SINGLE = "single"
    DOUBLE = "double"
    SUITE = "suite"
    DELUXE = "deluxe"
    PRESIDENTIAL = "presidential"


class BookingStatusEnum(str, Enum):
    """Enumeration of booking statuses"""

    PENDING = "pending"
    CONFIRMED = "confirmed"
    CHECKED_IN = "checked_in"
    CHECKED_OUT = "checked_out"
    CANCELLED = "cancelled"


class Room(BaseModel):
    """
    Room model representing a hotel room.

    Attributes:
        id (int): Unique identifier for the room
        room_number (str): Room number (e.g., "101", "A-205")
        room_type (RoomTypeEnum): Type of room
        price_per_night (float): Price per night in USD
        capacity (int): Maximum number of guests
        amenities (List[str]): List of amenities
        is_available (bool): Whether the room is currently available
        description (str): Description of the room
    """

    id: int
    room_number: str = Field(
        ..., min_length=1, max_length=20, description="Room number"
    )
    room_type: RoomTypeEnum = Field(..., description="Type of room")
    price_per_night: float = Field(..., gt=0, description="Price per night in USD")
    capacity: int = Field(..., ge=1, le=10, description="Maximum number of guests")
    amenities: List[str] = Field(default_factory=list, description="List of amenities")
    is_available: bool = Field(default=True, description="Room availability status")
    description: str = Field(
        ..., min_length=10, max_length=500, description="Room description"
    )

    @validator("room_number")
    def validate_room_number(cls, v):
        if not v.strip():
            raise ValueError("Room number cannot be empty or only whitespace")
        return v.strip()

    @validator("description")
    def validate_description(cls, v):
        if not v.strip():
            raise ValueError("Description cannot be empty or only whitespace")
        return v.strip()


class RoomCreate(BaseModel):
    """Model for creating a new room (without ID)"""

    room_number: str = Field(..., min_length=1, max_length=20)
    room_type: RoomTypeEnum
    price_per_night: float = Field(..., gt=0)
    capacity: int = Field(..., ge=1, le=10)
    amenities: List[str] = Field(default_factory=list)
    is_available: bool = Field(default=True)
    description: str = Field(..., min_length=10, max_length=500)

    @validator("room_number", "description")
    def validate_strings(cls, v):
        if not v.strip():
            raise ValueError("Field cannot be empty or only whitespace")
        return v.strip()


class Booking(BaseModel):
    """
    Booking model representing a hotel booking.

    Attributes:
        id (int): Unique identifier for the booking
        room_id (int): ID of the booked room
        guest_name (str): Name of the guest
        guest_email (str): Email of the guest
        check_in_date (date): Check-in date
        check_out_date (date): Check-out date
        num_guests (int): Number of guests
        total_price (float): Total price for the booking
        status (BookingStatusEnum): Status of the booking
        created_at (datetime): Timestamp when booking was created
        special_requests (Optional[str]): Special requests from guest
    """

    id: int
    room_id: int = Field(..., gt=0, description="ID of the room being booked")
    guest_name: str = Field(..., min_length=2, max_length=100, description="Guest name")
    guest_email: str = Field(
        ..., min_length=5, max_length=100, description="Guest email"
    )
    check_in_date: date = Field(..., description="Check-in date")
    check_out_date: date = Field(..., description="Check-out date")
    num_guests: int = Field(..., ge=1, le=10, description="Number of guests")
    total_price: float = Field(..., gt=0, description="Total price for the booking")
    status: BookingStatusEnum = Field(
        default=BookingStatusEnum.PENDING, description="Booking status"
    )
    created_at: datetime = Field(
        default_factory=datetime.now, description="Creation timestamp"
    )
    special_requests: Optional[str] = Field(
        None, max_length=500, description="Special requests"
    )

    @validator("guest_name")
    def validate_guest_name(cls, v):
        if not v.strip():
            raise ValueError("Guest name cannot be empty or only whitespace")
        return v.strip()

    @validator("guest_email")
    def validate_guest_email(cls, v):
        if "@" not in v or "." not in v:
            raise ValueError("Invalid email format")
        return v.strip().lower()

    @validator("check_out_date")
    def validate_dates(cls, v, values):
        if "check_in_date" in values and v <= values["check_in_date"]:
            raise ValueError("Check-out date must be after check-in date")
        return v

    @validator("check_in_date")
    def validate_check_in_date(cls, v):
        if v < date.today():
            raise ValueError("Check-in date cannot be in the past")
        return v


class BookingCreate(BaseModel):
    """Model for creating a new booking"""

    room_id: int = Field(..., gt=0)
    guest_name: str = Field(..., min_length=2, max_length=100)
    guest_email: str = Field(..., min_length=5, max_length=100)
    check_in_date: date
    check_out_date: date
    num_guests: int = Field(..., ge=1, le=10)
    special_requests: Optional[str] = Field(None, max_length=500)

    @validator("guest_name")
    def validate_guest_name(cls, v):
        if not v.strip():
            raise ValueError("Guest name cannot be empty or only whitespace")
        return v.strip()

    @validator("guest_email")
    def validate_guest_email(cls, v):
        if "@" not in v or "." not in v:
            raise ValueError("Invalid email format")
        return v.strip().lower()

    @validator("check_out_date")
    def validate_dates(cls, v, values):
        if "check_in_date" in values and v <= values["check_in_date"]:
            raise ValueError("Check-out date must be after check-in date")
        return v

    @validator("check_in_date")
    def validate_check_in_date(cls, v):
        if v < date.today():
            raise ValueError("Check-in date cannot be in the past")
        return v


# Initialize FastAPI application
app = FastAPI(
    title="Hotel Booking API",
    description="A comprehensive API for managing hotel rooms and bookings",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Utility functions for data persistence
def load_data_from_json(file_path: str) -> List[dict]:
    """Load data from JSON file"""
    try:
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                return json.load(f)
        else:
            return []
    except Exception as e:
        print(f"Error reading data from {file_path}: {e}")
        return []


def save_data_to_json(data: List[dict], file_path: str):
    """Save data to JSON file"""
    try:
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4, default=str)
    except Exception as e:
        print(f"Error saving data to {file_path}: {e}")


def get_room_by_id(room_id: int) -> Optional[dict]:
    """Get room by ID"""
    rooms = load_data_from_json(ROOMS_FILE)
    return next((room for room in rooms if room["id"] == room_id), None)


def check_room_availability(
    room_id: int,
    check_in: date,
    check_out: date,
    exclude_booking_id: Optional[int] = None,
) -> bool:
    """Check if a room is available for the given dates"""
    bookings = load_data_from_json(BOOKINGS_FILE)

    for booking in bookings:
        # Skip if it's the same booking (for updates)
        if exclude_booking_id and booking["id"] == exclude_booking_id:
            continue

        # Skip cancelled bookings
        if booking["status"] == BookingStatusEnum.CANCELLED:
            continue

        # Check if booking is for the same room
        if booking["room_id"] != room_id:
            continue

        # Convert string dates to date objects
        booking_check_in = datetime.fromisoformat(booking["check_in_date"]).date()
        booking_check_out = datetime.fromisoformat(booking["check_out_date"]).date()

        # Check for date overlap
        if not (check_out <= booking_check_in or check_in >= booking_check_out):
            return False

    return True


def calculate_total_price(room_id: int, check_in: date, check_out: date) -> float:
    """Calculate total price for a booking"""
    room = get_room_by_id(room_id)
    if not room:
        return 0.0

    nights = (check_out - check_in).days
    return room["price_per_night"] * nights


# Root endpoint
@app.get("/", status_code=status.HTTP_200_OK)
def read_root():
    """
    Root endpoint that returns API information.

    Returns:
        dict: API information and available endpoints
    """
    return {
        "message": "Hotel Booking API",
        "version": "1.0.0",
        "endpoints": {"rooms": "/rooms", "bookings": "/bookings", "docs": "/docs"},
    }


# Room CRUD endpoints
@app.get("/rooms", status_code=status.HTTP_200_OK)
def get_rooms(
    room_type: Optional[RoomTypeEnum] = Query(None, description="Filter by room type"),
    min_price: Optional[float] = Query(None, ge=0, description=MIN_PRICE_DESC),
    max_price: Optional[float] = Query(None, ge=0, description=MAX_PRICE_DESC),
    min_capacity: Optional[int] = Query(None, ge=1, description="Minimum capacity"),
    max_capacity: Optional[int] = Query(None, ge=1, description="Maximum capacity"),
    available_only: bool = Query(False, description="Show only available rooms"),
    sort_by: Optional[str] = Query(
        "id", description="Sort by: id, room_number, price_per_night, capacity"
    ),
    order: Optional[str] = Query("asc", description=SORT_ORDER_DESC),
    limit: Optional[int] = Query(
        None, ge=1, le=100, description="Limit number of results"
    ),
    offset: Optional[int] = Query(0, ge=0, description="Offset for pagination"),
):
    """
    Retrieve all rooms with optional filtering, sorting, and pagination.

    Returns:
        dict: Dictionary containing filtered and sorted rooms
    """
    rooms = load_data_from_json(ROOMS_FILE)

    # Apply filters
    filtered_rooms = rooms.copy()

    if room_type:
        filtered_rooms = [
            r for r in filtered_rooms if r["room_type"] == room_type.value
        ]

    if min_price is not None:
        filtered_rooms = [
            r for r in filtered_rooms if r["price_per_night"] >= min_price
        ]

    if max_price is not None:
        filtered_rooms = [
            r for r in filtered_rooms if r["price_per_night"] <= max_price
        ]

    if min_capacity:
        filtered_rooms = [r for r in filtered_rooms if r["capacity"] >= min_capacity]

    if max_capacity:
        filtered_rooms = [r for r in filtered_rooms if r["capacity"] <= max_capacity]

    if available_only:
        filtered_rooms = [r for r in filtered_rooms if r["is_available"]]

    # Sorting
    valid_sort_fields = ["id", "room_number", "price_per_night", "capacity"]
    if sort_by in valid_sort_fields:
        reverse = order.lower() == "desc"
        filtered_rooms.sort(key=lambda x: x[sort_by], reverse=reverse)

    # Pagination
    total_count = len(filtered_rooms)
    if offset:
        filtered_rooms = filtered_rooms[offset:]
    if limit:
        filtered_rooms = filtered_rooms[:limit]

    return {
        "rooms": filtered_rooms,
        "total_count": total_count,
        "returned_count": len(filtered_rooms),
        "offset": offset,
        "limit": limit,
    }


@app.get("/rooms/{room_id}", status_code=status.HTTP_200_OK)
def get_room(room_id: int):
    """
    Retrieve a specific room by its ID.

    Args:
        room_id (int): The unique identifier of the room

    Returns:
        dict: Room data

    Raises:
        HTTPException: 404 if room not found
    """
    room = get_room_by_id(room_id)

    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=ROOM_NOT_FOUND_MESSAGE
        )

    return {"message": "Room found", "room": room}


@app.post("/rooms", status_code=status.HTTP_201_CREATED)
def create_room(room: RoomCreate):
    """
    Create a new room.

    Args:
        room (RoomCreate): Room object containing room details

    Returns:
        dict: Confirmation message and created room data
    """
    rooms = load_data_from_json(ROOMS_FILE)

    # Check if room number already exists
    if any(r["room_number"] == room.room_number for r in rooms):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Room number {room.room_number} already exists",
        )

    # Generate ID
    max_id = max([r["id"] for r in rooms], default=0)
    room_id = max_id + 1

    # Create room dict
    room_dict = room.model_dump()
    room_dict["id"] = room_id

    rooms.append(room_dict)
    save_data_to_json(rooms, ROOMS_FILE)

    return {"message": "Room created", "room": room_dict}


@app.put("/rooms/{room_id}", status_code=status.HTTP_200_OK)
def update_room(room_id: int, updated_room: RoomCreate):
    """
    Update an existing room by its ID.

    Args:
        room_id (int): The unique identifier of the room to update
        updated_room (RoomCreate): Updated room data

    Returns:
        dict: Confirmation message and updated room data

    Raises:
        HTTPException: 404 if room not found, 400 if room number conflicts
    """
    rooms = load_data_from_json(ROOMS_FILE)

    # Check if room number already exists (excluding current room)
    if any(
        r["room_number"] == updated_room.room_number and r["id"] != room_id
        for r in rooms
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Room number {updated_room.room_number} already exists",
        )

    for room in rooms:
        if room["id"] == room_id:
            # Update room fields but preserve ID
            updated_dict = updated_room.model_dump()
            room.update(updated_dict)
            room["id"] = room_id  # Preserve original ID

            save_data_to_json(rooms, ROOMS_FILE)
            return {"message": "Room updated", "room": room}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=ROOM_NOT_FOUND_MESSAGE
    )


@app.delete("/rooms/{room_id}", status_code=status.HTTP_200_OK)
def delete_room(room_id: int):
    """
    Delete a room by its ID. Also cancels all associated bookings.

    Args:
        room_id (int): The unique identifier of the room to delete

    Returns:
        dict: Confirmation message and deleted room data

    Raises:
        HTTPException: 404 if room not found
    """
    rooms = load_data_from_json(ROOMS_FILE)
    bookings = load_data_from_json(BOOKINGS_FILE)

    for room in rooms:
        if room["id"] == room_id:
            # Remove the room
            rooms.remove(room)
            save_data_to_json(rooms, ROOMS_FILE)

            # Cancel all bookings for this room
            cancelled_bookings = 0
            for booking in bookings:
                if (
                    booking["room_id"] == room_id
                    and booking["status"] != BookingStatusEnum.CANCELLED
                ):
                    booking["status"] = BookingStatusEnum.CANCELLED
                    cancelled_bookings += 1

            save_data_to_json(bookings, BOOKINGS_FILE)

            return {
                "message": "Room deleted and associated bookings cancelled",
                "room": room,
                "cancelled_bookings_count": cancelled_bookings,
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=ROOM_NOT_FOUND_MESSAGE
    )


# Booking CRUD endpoints
@app.get("/bookings", status_code=status.HTTP_200_OK)
def get_bookings(
    room_id: Optional[int] = Query(None, description="Filter by room ID"),
    guest_name: Optional[str] = Query(
        None, description="Filter by guest name (case-insensitive)"
    ),
    guest_email: Optional[str] = Query(
        None, description="Filter by guest email (case-insensitive)"
    ),
    status_filter: Optional[BookingStatusEnum] = Query(
        None, description="Filter by booking status"
    ),
    check_in_date: Optional[date] = Query(None, description="Filter by check-in date"),
    sort_by: Optional[str] = Query(
        "created_at",
        description="Sort by: id, room_id, check_in_date, total_price, created_at",
    ),
    order: Optional[str] = Query("desc", description=SORT_ORDER_DESC),
    limit: Optional[int] = Query(
        None, ge=1, le=100, description="Limit number of results"
    ),
    offset: Optional[int] = Query(0, ge=0, description="Offset for pagination"),
):
    """
    Retrieve all bookings with optional filtering, sorting, and pagination.

    Returns:
        dict: Dictionary containing filtered and sorted bookings
    """
    bookings = load_data_from_json(BOOKINGS_FILE)

    # Apply filters
    filtered_bookings = bookings.copy()

    if room_id:
        filtered_bookings = [b for b in filtered_bookings if b["room_id"] == room_id]

    if guest_name:
        filtered_bookings = [
            b
            for b in filtered_bookings
            if guest_name.lower() in b["guest_name"].lower()
        ]

    if guest_email:
        filtered_bookings = [
            b
            for b in filtered_bookings
            if guest_email.lower() in b["guest_email"].lower()
        ]

    if status_filter:
        filtered_bookings = [
            b for b in filtered_bookings if b["status"] == status_filter.value
        ]

    if check_in_date:
        filtered_bookings = [
            b
            for b in filtered_bookings
            if datetime.fromisoformat(b["check_in_date"]).date() == check_in_date
        ]

    # Sorting
    valid_sort_fields = ["id", "room_id", "check_in_date", "total_price", "created_at"]
    if sort_by in valid_sort_fields:
        reverse = order.lower() == "desc"
        if sort_by in ["check_in_date", "created_at"]:
            # Sort by date
            filtered_bookings.sort(
                key=lambda x: (
                    datetime.fromisoformat(x[sort_by].replace("Z", "+00:00"))
                    if isinstance(x[sort_by], str)
                    else x[sort_by]
                ),
                reverse=reverse,
            )
        else:
            filtered_bookings.sort(key=lambda x: x[sort_by], reverse=reverse)

    # Pagination
    total_count = len(filtered_bookings)
    if offset:
        filtered_bookings = filtered_bookings[offset:]
    if limit:
        filtered_bookings = filtered_bookings[:limit]

    return {
        "bookings": filtered_bookings,
        "total_count": total_count,
        "returned_count": len(filtered_bookings),
        "offset": offset,
        "limit": limit,
    }


@app.get("/bookings/{booking_id}", status_code=status.HTTP_200_OK)
def get_booking(booking_id: int):
    """
    Retrieve a specific booking by its ID.

    Args:
        booking_id (int): The unique identifier of the booking

    Returns:
        dict: Booking data if found

    Raises:
        HTTPException: 404 if booking not found
    """
    bookings = load_data_from_json(BOOKINGS_FILE)

    for booking in bookings:
        if booking["id"] == booking_id:
            return {"message": "Booking found", "booking": booking}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=BOOKING_NOT_FOUND_MESSAGE
    )


@app.post("/bookings", status_code=status.HTTP_201_CREATED)
def create_booking(booking: BookingCreate):
    """
    Create a new booking for an existing room.

    Args:
        booking (BookingCreate): Booking object containing booking details

    Returns:
        dict: Confirmation message and created booking data

    Raises:
        HTTPException: 404 if room not found, 400 if room not available
    """
    # Validate that the room exists
    room = get_room_by_id(booking.room_id)
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Room with ID {booking.room_id} not found",
        )

    # Check if room is available for the dates
    if not check_room_availability(
        booking.room_id, booking.check_in_date, booking.check_out_date
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=ROOM_NOT_AVAILABLE_MESSAGE
        )

    # Check room capacity
    if booking.num_guests > room["capacity"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Room capacity is {room['capacity']}, but {booking.num_guests} guests requested",
        )

    bookings = load_data_from_json(BOOKINGS_FILE)

    # Generate ID
    max_id = max([b["id"] for b in bookings], default=0)
    booking_id = max_id + 1

    # Calculate total price
    total_price = calculate_total_price(
        booking.room_id, booking.check_in_date, booking.check_out_date
    )

    # Create booking dict
    booking_dict = booking.model_dump()
    booking_dict["id"] = booking_id
    booking_dict["total_price"] = total_price
    booking_dict["status"] = BookingStatusEnum.PENDING
    booking_dict["created_at"] = datetime.now()

    bookings.append(booking_dict)
    save_data_to_json(bookings, BOOKINGS_FILE)

    return {"message": "Booking created", "booking": booking_dict}


@app.put("/bookings/{booking_id}", status_code=status.HTTP_200_OK)
def update_booking(booking_id: int, updated_booking: BookingCreate):
    """
    Update an existing booking by its ID.

    Args:
        booking_id (int): The unique identifier of the booking to update
        updated_booking (BookingCreate): Updated booking data

    Returns:
        dict: Confirmation message and updated booking data

    Raises:
        HTTPException: 404 if booking or room not found, 400 if room not available
    """
    # Validate that the room exists
    room = get_room_by_id(updated_booking.room_id)
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Room with ID {updated_booking.room_id} not found",
        )

    bookings = load_data_from_json(BOOKINGS_FILE)

    for booking in bookings:
        if booking["id"] == booking_id:
            # Check if room is available for the dates (excluding current booking)
            if not check_room_availability(
                updated_booking.room_id,
                updated_booking.check_in_date,
                updated_booking.check_out_date,
                exclude_booking_id=booking_id,
            ):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=ROOM_NOT_AVAILABLE_MESSAGE,
                )

            # Check room capacity
            if updated_booking.num_guests > room["capacity"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Room capacity is {room['capacity']}, but {updated_booking.num_guests} guests requested",
                )

            # Calculate new total price
            total_price = calculate_total_price(
                updated_booking.room_id,
                updated_booking.check_in_date,
                updated_booking.check_out_date,
            )

            # Update booking fields but preserve ID, status, and created_at
            updated_dict = updated_booking.model_dump()
            original_status = booking["status"]
            original_created_at = booking["created_at"]

            booking.update(updated_dict)
            booking["id"] = booking_id  # Preserve original ID
            booking["status"] = original_status  # Preserve original status
            booking["created_at"] = original_created_at  # Preserve original created_at
            booking["total_price"] = total_price

            save_data_to_json(bookings, BOOKINGS_FILE)
            return {"message": "Booking updated", "booking": booking}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=BOOKING_NOT_FOUND_MESSAGE
    )


@app.delete("/bookings/{booking_id}", status_code=status.HTTP_200_OK)
def delete_booking(booking_id: int):
    """
    Delete a booking by its ID.

    Args:
        booking_id (int): The unique identifier of the booking to delete

    Returns:
        dict: Confirmation message and deleted booking data

    Raises:
        HTTPException: 404 if booking not found
    """
    bookings = load_data_from_json(BOOKINGS_FILE)

    for booking in bookings:
        if booking["id"] == booking_id:
            bookings.remove(booking)
            save_data_to_json(bookings, BOOKINGS_FILE)
            return {"message": "Booking deleted", "booking": booking}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=BOOKING_NOT_FOUND_MESSAGE
    )


# Additional useful endpoints
@app.put("/bookings/{booking_id}/status", status_code=status.HTTP_200_OK)
def update_booking_status(booking_id: int, new_status: BookingStatusEnum):
    """
    Update the status of a booking.

    Args:
        booking_id (int): The unique identifier of the booking
        new_status (BookingStatusEnum): The new status for the booking

    Returns:
        dict: Confirmation message and updated booking data

    Raises:
        HTTPException: 404 if booking not found
    """
    bookings = load_data_from_json(BOOKINGS_FILE)

    for booking in bookings:
        if booking["id"] == booking_id:
            booking["status"] = new_status.value
            save_data_to_json(bookings, BOOKINGS_FILE)
            return {"message": "Booking status updated", "booking": booking}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=BOOKING_NOT_FOUND_MESSAGE
    )


@app.get("/rooms/{room_id}/bookings", status_code=status.HTTP_200_OK)
def get_room_bookings(
    room_id: int,
    status_filter: Optional[BookingStatusEnum] = Query(
        None, description="Filter by booking status"
    ),
    sort_by: Optional[str] = Query(
        "check_in_date", description="Sort by: check_in_date, created_at"
    ),
    order: Optional[str] = Query("asc", description=SORT_ORDER_DESC),
):
    """
    Get all bookings for a specific room.

    Args:
        room_id (int): The unique identifier of the room

    Returns:
        dict: Room information and its bookings

    Raises:
        HTTPException: 404 if room not found
    """
    if not get_room_by_id(room_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=ROOM_NOT_FOUND_MESSAGE
        )

    bookings = load_data_from_json(BOOKINGS_FILE)
    room_bookings = [b for b in bookings if b["room_id"] == room_id]

    # Apply filters
    if status_filter:
        room_bookings = [b for b in room_bookings if b["status"] == status_filter.value]

    # Sorting
    if sort_by in ["check_in_date", "created_at"]:
        reverse = order.lower() == "desc"
        room_bookings.sort(
            key=lambda x: (
                datetime.fromisoformat(x[sort_by].replace("Z", "+00:00"))
                if isinstance(x[sort_by], str)
                else x[sort_by]
            ),
            reverse=reverse,
        )

    return {
        "room_id": room_id,
        "bookings": room_bookings,
        "total_bookings": len(room_bookings),
    }


@app.get("/rooms/availability", status_code=status.HTTP_200_OK)
def check_availability(
    check_in_date: date = Query(..., description="Check-in date"),
    check_out_date: date = Query(..., description="Check-out date"),
    num_guests: Optional[int] = Query(None, ge=1, description="Number of guests"),
    room_type: Optional[RoomTypeEnum] = Query(None, description="Room type"),
):
    """
    Check room availability for specific dates.

    Args:
        check_in_date (date): Check-in date
        check_out_date (date): Check-out date
        num_guests (int, optional): Number of guests
        room_type (RoomTypeEnum, optional): Room type filter

    Returns:
        dict: Available rooms for the specified dates

    Raises:
        HTTPException: 400 if invalid date range
    """
    if check_out_date <= check_in_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Check-out date must be after check-in date",
        )

    rooms = load_data_from_json(ROOMS_FILE)
    available_rooms = []

    for room in rooms:
        # Check if room is generally available
        if not room["is_available"]:
            continue

        # Check capacity if specified
        if num_guests and room["capacity"] < num_guests:
            continue

        # Check room type if specified
        if room_type and room["room_type"] != room_type.value:
            continue

        # Check if room is available for the dates
        if check_room_availability(room["id"], check_in_date, check_out_date):
            # Calculate total price for the stay
            nights = (check_out_date - check_in_date).days
            total_price = room["price_per_night"] * nights

            room_availability = room.copy()
            room_availability["total_price_for_stay"] = total_price
            room_availability["nights"] = nights

            available_rooms.append(room_availability)

    return {
        "check_in_date": check_in_date,
        "check_out_date": check_out_date,
        "available_rooms": available_rooms,
        "total_available": len(available_rooms),
    }


@app.get("/stats", status_code=status.HTTP_200_OK)
def get_stats():
    """
    Get general statistics about rooms and bookings.

    Returns:
        dict: Statistics about the hotel
    """
    rooms = load_data_from_json(ROOMS_FILE)
    bookings = load_data_from_json(BOOKINGS_FILE)

    # Calculate stats
    total_rooms = len(rooms)
    total_bookings = len(bookings)
    available_rooms = len([r for r in rooms if r["is_available"]])

    # Room type distribution
    room_type_counts = {}
    for room in rooms:
        room_type = room["room_type"]
        room_type_counts[room_type] = room_type_counts.get(room_type, 0) + 1

    # Booking status distribution
    booking_status_counts = {}
    for booking in bookings:
        status = booking["status"]
        booking_status_counts[status] = booking_status_counts.get(status, 0) + 1

    # Revenue calculation
    total_revenue = sum(
        booking["total_price"]
        for booking in bookings
        if booking["status"]
        in [
            BookingStatusEnum.CONFIRMED,
            BookingStatusEnum.CHECKED_IN,
            BookingStatusEnum.CHECKED_OUT,
        ]
    )

    return {
        "total_rooms": total_rooms,
        "available_rooms": available_rooms,
        "total_bookings": total_bookings,
        "total_revenue": round(total_revenue, 2),
        "room_type_distribution": room_type_counts,
        "booking_status_distribution": booking_status_counts,
    }
