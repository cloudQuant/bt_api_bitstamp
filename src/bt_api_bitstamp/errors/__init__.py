from bt_api_base.error import ErrorTranslator, UnifiedError, UnifiedErrorCode


class BitstampErrorTranslator(ErrorTranslator):
    ERROR_MAP = {
        "ERROR": (UnifiedErrorCode.INTERNAL_ERROR, "Generic error"),
        "DUST": (UnifiedErrorCode.INVALID_PARAMETER, "Dust quantity"),
        "EAPI:Invalid nonce": (UnifiedErrorCode.INTERNAL_ERROR, "Invalid nonce"),
        "EOrder:Invalid amount": (UnifiedErrorCode.INVALID_VOLUME, "Invalid order amount"),
        "EOrder:Invalid price": (UnifiedErrorCode.INVALID_PARAMETER, "Invalid price"),
        "EOrder:Unknown order": (UnifiedErrorCode.ORDER_NOT_FOUND, "Order not found"),
        "EGeneral:Insufficient funds": (
            UnifiedErrorCode.INSUFFICIENT_BALANCE,
            "Insufficient funds",
        ),
        "EGeneral:Invalid order": (UnifiedErrorCode.INVALID_ORDER_TYPE, "Invalid order"),
    }

    HTTP_STATUS_MAP = {
        400: (UnifiedErrorCode.INVALID_PARAMETER, "Bad request"),
        401: (UnifiedErrorCode.INVALID_API_KEY, "Unauthorized"),
        403: (UnifiedErrorCode.PERMISSION_DENIED, "Forbidden"),
        404: (UnifiedErrorCode.ORDER_NOT_FOUND, "Not found"),
        429: (UnifiedErrorCode.RATE_LIMIT_EXCEEDED, "Too many requests"),
        500: (UnifiedErrorCode.INTERNAL_ERROR, "Internal server error"),
        503: (UnifiedErrorCode.EXCHANGE_OVERLOADED, "Service unavailable"),
    }

    @classmethod
    def translate(cls, raw_error: dict, venue: str) -> UnifiedError | None:
        error = raw_error.get("error", raw_error)
        msg = error.get("message", error.get("reason", error.get("__all__", "")))
        status = error.get("status")

        if isinstance(msg, list):
            msg = "; ".join(str(m) for m in msg)

        if msg and msg in cls.ERROR_MAP:
            unified_code, default_msg = cls.ERROR_MAP[msg]
            return UnifiedError(
                code=unified_code,
                category=cls._get_category(unified_code),
                venue=venue,
                message=msg or default_msg,
                original_error=str(raw_error),
                context={"raw_response": raw_error},
            )

        if status and status in cls.HTTP_STATUS_MAP:
            unified_code, default_msg = cls.HTTP_STATUS_MAP[status]
            return UnifiedError(
                code=unified_code,
                category=cls._get_category(unified_code),
                venue=venue,
                message=msg or default_msg,
                original_error=f"HTTP {status}: {msg}",
                context={"raw_response": raw_error},
            )

        return UnifiedError(
            code=UnifiedErrorCode.INTERNAL_ERROR,
            category=cls._get_category(UnifiedErrorCode.INTERNAL_ERROR),
            venue=venue,
            message=msg or "Unknown error",
            original_error=str(raw_error),
            context={"raw_response": raw_error},
        )
