from aiogram.fsm.state import StatesGroup, State

class BookingStates(StatesGroup):
    choosing_date = State()
    choosing_people = State()
    choosing_time = State()
    confirming = State()
    entering_name = State()
    entering_email = State()
    entering_phone = State()

class SpecialBookingStates(StatesGroup):
    entering_name = State()
    entering_email = State()
    entering_phone = State()
    entering_guests = State()
    entering_info = State()