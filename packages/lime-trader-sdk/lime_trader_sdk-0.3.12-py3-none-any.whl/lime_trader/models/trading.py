import datetime
import enum
from _decimal import Decimal
from dataclasses import dataclass
from typing import Union, List


class OrderStatus(enum.Enum):
    NEW = "new"
    PENDING_NEW = "pending_new"
    PARTIALLY_FILLED = "partially_filled"
    FILLED = "filled"
    PENDING_CANCEL = "pending_cancel"
    CANCELED = "canceled"
    REPLACED = "replaced"
    REJECTED = "rejected"
    DONE_FOR_DAY = "done_for_day"
    SUSPENDED = "suspended"


class TimeInForce(enum.Enum):
    DAY = "day"
    EXT = "ext"
    ON_OPEN = "on-open"
    ON_CLOSE = "on-close"
    IOC = "ioc"
    FOK = "fok"


class OrderType(enum.Enum):
    MARKET = "market"
    LIMIT = "limit"


class OrderSide(enum.Enum):
    BUY = "buy"
    SELL = "sell"


@dataclass(frozen=True)
class OrderLeg:
    """Leg in the multi-leg order

    Attributes:
        symbol: The leg security symbol
        quantity: Positive integer, leg ratio quantity
        side: The leg cost basis
    """

    symbol: str
    quantity: int
    side: OrderSide


@dataclass(frozen=True)
class Order:
    """
    Represents order

    Attributes:
        account_number: Account number this order belongs to.
        symbol: The security symbol, stocks in Nasdaq CMS convention, options in OCC.
        quantity: The positive decimal, number of shares, options contracts or multi-leg orders.
        exchange: Optional, auto by default. The routing instructions for order execution.
                  The actual values are dynamic and depend on the account settings.
                  Some of the possible values are NASDAQ or ARCA
        client_order_id: Optional, automatically generated if not set. A unique order identifier that is
                         used to prevent duplicate orders from being submitted.
                         Maximum length of 32 alphanumeric characters
        tag: Optional. Any comment to specify with an order.
             Maximum length of 32 characters: 0-9, a-z, A-Z,  , !, #, $, (, ), *, +, -, ., ,, /, :, ;, = and _
        price: Positive decimal if the order_type is limit or stop_limit

        time_in_force: Optional, day by default. Specifies how long the order remains in effect
        order_type: Optional, market by default
        side: Optional, buy by default. Available values are buy and sell.
              Buy opens long position, sell closes the position.
              The system will determine the proper side according to the current position,
              but you are still required to place two orders to revert the position from
              long to short and the other way around.
              For multi-leg order use buy, if net debit or even. Use sell, if net credit
        legs: Required for a multi-leg order, array of leg elements
    """

    account_number: str
    symbol: str
    quantity: Decimal
    exchange: str = "auto"
    client_order_id: Union[str, None] = None
    tag: Union[str, None] = None
    price: Decimal | None = None
    time_in_force: TimeInForce = TimeInForce.DAY

    order_type: OrderType = OrderType.MARKET
    side: OrderSide = OrderSide.BUY
    legs: Union[List[OrderLeg], None] = None

    def __post_init__(self):
        if (
                self.price is None
                or self.price < Decimal(0)
        ) and self.order_type in (OrderType.LIMIT,):
            raise ValueError("Price must be positive decimal if the order_type is LIMIT")


@dataclass(frozen=True)
class OrderDetails:
    """
    Represents order details after order has been submitted

    Attributes:
        account_number: Account number this order belongs to
        client_id: Order id
        exchange: The routing instructions
        quantity: Number of shares or contracts requested by the order
        executed_quantity: Number of shares or contracts executed by this time
        order_status: Order status
        price: Limit price if applicable
        stop_price: Stop price if applicable
        time_in_force: Order duration instructions
        order_type: Type of the order
        order_side: Side of the order
        symbol: Security symbol
        client_order_id: The client order id
        tag: Order tag if specified
        executed_timestamp: Timestamp of the last execution, only populated when an order has been executed,
                            partially or fully
        legs: Array of legs in a multi-leg order
    """

    account_number: str
    client_id: str
    exchange: str
    quantity: Decimal
    executed_quantity: Decimal
    order_status: OrderStatus
    price: Decimal
    time_in_force: TimeInForce
    order_type: OrderType
    order_side: OrderSide
    symbol: str
    client_order_id: Union[str, None] = None
    tag: Union[str, None] = None
    stop_price: Union[Decimal, None] = None
    executed_timestamp: Union[datetime.datetime | None] = None
    legs: Union[List[OrderLeg] | None] = None

    @property
    def id(self) -> str:
        return self.client_id

    @property
    def order_id(self) -> str:
        return self.client_id


@dataclass(frozen=True)
class PlaceOrderResponse:
    """
    Order place response

    Attributes:
        success: Indicator if order place was success
        data: ID that is assigned to the order

    """

    success: bool
    data: str

    @property
    def order_id(self) -> str:
        return self.data


@dataclass(frozen=True)
class ValidateOrderResponse:
    """
    Order validation response

    Attributes:
        is_valid: Status of validation
        validation_message: Optional reject reason
    """

    is_valid: bool
    validation_message: str | None = None


@dataclass(frozen=True)
class CancelOrderResponse:
    """
    Order cancellation response

    Attributes:
        success: Indicator if cancel was success
        data: Cancellation request id
    """

    success: bool
    data: str


@dataclass(frozen=True)
class OrderFee:
    """
    Order fee

    Attributes:
        amount: Dollar amount
        type: Charge description
    """

    amount: Decimal
    type: str
