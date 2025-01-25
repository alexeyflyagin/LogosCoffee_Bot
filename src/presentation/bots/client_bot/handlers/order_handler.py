from aiogram import Router, F
from aiogram.enums import ParseMode, ContentType
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from src.loggers import bot_logger as logger

from src.data.logoscoffee.exceptions import DatabaseError, UnknownError, InvalidTokenError, \
    OtherOrderIsPlacedAlreadyError
from src.data.logoscoffee.interfaces.client_service import ClientService
from src.data.logoscoffee.models import PlaceOrderData
from src.data.logoscoffee.services.client_order_service_impl import ClientOrderServiceImpl
from src.presentation.bots.client_bot.handlers.utils import get_token, unknown_error, invalid_token_error, reset_state
from src.presentation.bots.client_bot.states import MainStates, MakeOrderStates
from src.presentation.checks.checks import check_content_type
from src.presentation.checks.exceptions import ContentTypeError
from src.presentation.resources import strings

router = Router(name=__name__)
client_service: ClientService
order_service: ClientOrderServiceImpl


@router.message(MainStates(), F.text == strings.BTN.MAKE_ORDER)
async def make_order_handler(msg: Message, state: FSMContext):
    try:
        token = await get_token(state)
        await order_service.can_place_order(token)
        await state.set_state(MakeOrderStates.EnterDetails)
        await msg.answer(text=strings.CLIENT.MAKE_ORDER.ENTER_DETAILS, parse_mode=ParseMode.MARKDOWN,
                         reply_markup=ReplyKeyboardRemove())
    except OtherOrderIsPlacedAlreadyError as e:
        logger.debug(e)
        await msg.answer(text=strings.CLIENT.MAKE_ORDER.ANOTHER_ORDER_ALREADY_PLACED)
    except InvalidTokenError as e:
        logger.debug(e)
        await invalid_token_error(msg, state)
    except (DatabaseError, UnknownError, Exception) as e:
        logger.error(e)
        await unknown_error(msg, state)


@router.message(MakeOrderStates.EnterDetails)
async def make_order__details__handler(msg: Message, state: FSMContext):
    try:
        token = await get_token(state)
        await client_service.validate_token(token)
        check_content_type(msg, ContentType.TEXT)
        await order_service.place_order(token, PlaceOrderData(details=msg.text))
        await reset_state(msg, state, msg_text=strings.CLIENT.MAKE_ORDER.SUCCESS)
    except ContentTypeError as e:
        logger.debug(e.log_msg)
        await msg.answer(e.msg)
    except OtherOrderIsPlacedAlreadyError as e:
        logger.debug(e)
        await msg.answer(text=strings.CLIENT.MAKE_ORDER.ANOTHER_ORDER_ALREADY_PLACED)
    except InvalidTokenError as e:
        logger.debug(e)
        await invalid_token_error(msg, state)
    except (DatabaseError, UnknownError, Exception) as e:
        logger.error(e)
        await unknown_error(msg, state)
