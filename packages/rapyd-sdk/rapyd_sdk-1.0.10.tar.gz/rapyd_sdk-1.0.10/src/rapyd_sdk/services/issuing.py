from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models import (
    BankaccountsBankaccounttransfertobankaccountBody,
    BankaccountsVirtualAccountIdBody,
    CardDetailsCardTokenBody,
    CardsActivateBody,
    CardsPersonalizeBody,
    CardsStatusBody,
    InlineResponse200_10,
    InlineResponse200_11,
    InlineResponse200_43,
    InlineResponse200_44,
    InlineResponse200_45,
    InlineResponse200_46,
    InlineResponse200_47,
    InlineResponse200_5,
    InlineResponse200_6,
    InlineResponse200_7,
    InlineResponse200_8,
    InlineResponse200_9,
    IssuingBankaccountsBody,
    IssuingCardsBody,
)


class IssuingService(BaseService):

    @cast_models
    def create_v1_hosted_issuing_card_details_by_card_token(
        self,
        request_body: CardDetailsCardTokenBody,
        card_token: str,
        access_key: str,
        content_type: str,
        salt: str,
        signature: str,
        timestamp: str,
        idempotency: str = None,
    ) -> InlineResponse200_5:
        """Generate a hosted page that displays details of a virtual issued card directly to the customer. The URL is available for 24 hours after the response is sent, and then it expires.

        :param request_body: The request body.
        :type request_body: CardDetailsCardTokenBody
        :param card_token: ID of the Issued Card Details to Customer.
        :type card_token: str
        :param access_key: Unique access key provided by Rapyd for each authorized user.
        :type access_key: str
        :param content_type: Indicates that the data appears in JSON format. Set to **application/json**.
        :type content_type: str
        :param salt: Random string. Recommended length: 8-16 characters.
        :type salt: str
        :param signature: Signature calculated for each request individually. See [Request Signatures](https://docs.rapyd.net/en/request-signatures.html).
        :type signature: str
        :param timestamp: Timestamp for the request, in Unix time (seconds).
        :type timestamp: str
        :param idempotency: A unique key that prevents the platform from creating the same object twice., defaults to None
        :type idempotency: str, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Display Issued Card Details to Customer.
        :rtype: InlineResponse200_5
        """

        Validator(CardDetailsCardTokenBody).validate(request_body)
        Validator(str).validate(card_token)
        Validator(str).validate(access_key)
        Validator(str).validate(content_type)
        Validator(str).validate(salt)
        Validator(str).validate(signature)
        Validator(str).validate(timestamp)
        Validator(str).is_optional().validate(idempotency)

        serialized_request = (
            Serializer(
                f"{self.base_url}/v1/hosted/issuing/card_details/{{cardToken}}",
                self.get_default_headers(),
            )
            .add_header("access_key", access_key)
            .add_header("Content-Type", content_type)
            .add_header("idempotency", idempotency)
            .add_header("salt", salt)
            .add_header("signature", signature)
            .add_header("timestamp", timestamp)
            .add_path("cardToken", card_token)
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)
        return InlineResponse200_5._unmap(response)

    @cast_models
    def get_card_issuing_list(
        self,
        access_key: str,
        content_type: str,
        salt: str,
        signature: str,
        timestamp: str,
        contact: str = None,
        page_number: float = None,
        page_size: float = None,
        creation_start_date: float = None,
        creation_end_date: float = None,
        activation_start_date: float = None,
        activation_end_date: float = None,
        card_program: str = None,
        status: str = None,
        allow_deleted: bool = None,
        idempotency: str = None,
    ) -> InlineResponse200_6:
        """Retrieve a list of all issuing cards.

        :param access_key: Unique access key provided by Rapyd for each authorized user.
        :type access_key: str
        :param content_type: Indicates that the data appears in JSON format. Set to **application/json**.
        :type content_type: str
        :param salt: Random string. Recommended length: 8-16 characters.
        :type salt: str
        :param signature: Signature calculated for each request individually. See [Request Signatures](https://docs.rapyd.net/en/request-signatures.html).
        :type signature: str
        :param timestamp: Timestamp for the request, in Unix time (seconds).
        :type timestamp: str
        :param contact: ID of a wallet contact. String starting with **cont_**., defaults to None
        :type contact: str, optional
        :param page_number: Page number to retrieve., defaults to None
        :type page_number: float, optional
        :param page_size: Number of results per page., defaults to None
        :type page_size: float, optional
        :param creation_start_date: Start date of card creation., defaults to None
        :type creation_start_date: float, optional
        :param creation_end_date: End date of card creation., defaults to None
        :type creation_end_date: float, optional
        :param activation_start_date: Start date of card activation., defaults to None
        :type activation_start_date: float, optional
        :param activation_end_date: End date of card activation., defaults to None
        :type activation_end_date: float, optional
        :param card_program: Card program token., defaults to None
        :type card_program: str, optional
        :param status: Card status., defaults to None
        :type status: str, optional
        :param allow_deleted: Is card allow delete., defaults to None
        :type allow_deleted: bool, optional
        :param idempotency: A unique key that prevents the platform from creating the same object twice., defaults to None
        :type idempotency: str, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: List of cards.
        :rtype: InlineResponse200_6
        """

        Validator(str).validate(access_key)
        Validator(str).validate(content_type)
        Validator(str).validate(salt)
        Validator(str).validate(signature)
        Validator(str).validate(timestamp)
        Validator(str).is_optional().validate(contact)
        Validator(float).is_optional().validate(page_number)
        Validator(float).is_optional().validate(page_size)
        Validator(float).is_optional().validate(creation_start_date)
        Validator(float).is_optional().validate(creation_end_date)
        Validator(float).is_optional().validate(activation_start_date)
        Validator(float).is_optional().validate(activation_end_date)
        Validator(str).is_optional().validate(card_program)
        Validator(str).is_optional().validate(status)
        Validator(bool).is_optional().validate(allow_deleted)
        Validator(str).is_optional().validate(idempotency)

        serialized_request = (
            Serializer(f"{self.base_url}/v1/issuing/cards", self.get_default_headers())
            .add_header("access_key", access_key)
            .add_header("Content-Type", content_type)
            .add_header("idempotency", idempotency)
            .add_header("salt", salt)
            .add_header("signature", signature)
            .add_header("timestamp", timestamp)
            .add_query("contact", contact, explode=False)
            .add_query("page_number", page_number, explode=False)
            .add_query("page_size", page_size, explode=False)
            .add_query("creation_start_date", creation_start_date, explode=False)
            .add_query("creation_end_date", creation_end_date, explode=False)
            .add_query("activation_start_date", activation_start_date, explode=False)
            .add_query("activation_end_date", activation_end_date, explode=False)
            .add_query("card_program", card_program, explode=False)
            .add_query("status", status, explode=False)
            .add_query("allow_deleted", allow_deleted, explode=False)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)
        return InlineResponse200_6._unmap(response)

    @cast_models
    def issue_card(
        self,
        request_body: IssuingCardsBody,
        access_key: str,
        content_type: str,
        salt: str,
        signature: str,
        timestamp: str,
        idempotency: str = None,
    ) -> InlineResponse200_7:
        """Issue a card to a wallet contact.

        :param request_body: The request body.
        :type request_body: IssuingCardsBody
        :param access_key: Unique access key provided by Rapyd for each authorized user.
        :type access_key: str
        :param content_type: Indicates that the data appears in JSON format. Set to **application/json**.
        :type content_type: str
        :param salt: Random string. Recommended length: 8-16 characters.
        :type salt: str
        :param signature: Signature calculated for each request individually. See [Request Signatures](https://docs.rapyd.net/en/request-signatures.html).
        :type signature: str
        :param timestamp: Timestamp for the request, in Unix time (seconds).
        :type timestamp: str
        :param idempotency: A unique key that prevents the platform from creating the same object twice., defaults to None
        :type idempotency: str, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: List Contacts for a Rapyd Wallet.
        :rtype: InlineResponse200_7
        """

        Validator(IssuingCardsBody).validate(request_body)
        Validator(str).validate(access_key)
        Validator(str).validate(content_type)
        Validator(str).validate(salt)
        Validator(str).validate(signature)
        Validator(str).validate(timestamp)
        Validator(str).is_optional().validate(idempotency)

        serialized_request = (
            Serializer(f"{self.base_url}/v1/issuing/cards", self.get_default_headers())
            .add_header("access_key", access_key)
            .add_header("Content-Type", content_type)
            .add_header("idempotency", idempotency)
            .add_header("salt", salt)
            .add_header("signature", signature)
            .add_header("timestamp", timestamp)
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)
        return InlineResponse200_7._unmap(response)

    @cast_models
    def get_card_issuing_details(
        self,
        card_id: str,
        access_key: str,
        content_type: str,
        salt: str,
        signature: str,
        timestamp: str,
        idempotency: str = None,
    ) -> InlineResponse200_8:
        """Retrieve the details of a card.

        :param card_id: ID of a cardId. String starting with **ci_**.
        :type card_id: str
        :param access_key: Unique access key provided by Rapyd for each authorized user.
        :type access_key: str
        :param content_type: Indicates that the data appears in JSON format. Set to **application/json**.
        :type content_type: str
        :param salt: Random string. Recommended length: 8-16 characters.
        :type salt: str
        :param signature: Signature calculated for each request individually. See [Request Signatures](https://docs.rapyd.net/en/request-signatures.html).
        :type signature: str
        :param timestamp: Timestamp for the request, in Unix time (seconds).
        :type timestamp: str
        :param idempotency: A unique key that prevents the platform from creating the same object twice., defaults to None
        :type idempotency: str, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: get Card details By card Id.
        :rtype: InlineResponse200_8
        """

        Validator(str).validate(card_id)
        Validator(str).validate(access_key)
        Validator(str).validate(content_type)
        Validator(str).validate(salt)
        Validator(str).validate(signature)
        Validator(str).validate(timestamp)
        Validator(str).is_optional().validate(idempotency)

        serialized_request = (
            Serializer(
                f"{self.base_url}/v1/issuing/cards/{{cardId}}",
                self.get_default_headers(),
            )
            .add_header("access_key", access_key)
            .add_header("Content-Type", content_type)
            .add_header("idempotency", idempotency)
            .add_header("salt", salt)
            .add_header("signature", signature)
            .add_header("timestamp", timestamp)
            .add_path("cardId", card_id)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)
        return InlineResponse200_8._unmap(response)

    @cast_models
    def activate_card(
        self,
        request_body: CardsActivateBody,
        access_key: str,
        content_type: str,
        salt: str,
        signature: str,
        timestamp: str,
        idempotency: str = None,
    ) -> InlineResponse200_9:
        """Activate a card that was issued via the Rapyd issuing platform.

        :param request_body: The request body.
        :type request_body: CardsActivateBody
        :param access_key: Unique access key provided by Rapyd for each authorized user.
        :type access_key: str
        :param content_type: Indicates that the data appears in JSON format. Set to **application/json**.
        :type content_type: str
        :param salt: Random string. Recommended length: 8-16 characters.
        :type salt: str
        :param signature: Signature calculated for each request individually. See [Request Signatures](https://docs.rapyd.net/en/request-signatures.html).
        :type signature: str
        :param timestamp: Timestamp for the request, in Unix time (seconds).
        :type timestamp: str
        :param idempotency: A unique key that prevents the platform from creating the same object twice., defaults to None
        :type idempotency: str, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: List Contacts for a Rapyd Wallet.
        :rtype: InlineResponse200_9
        """

        Validator(CardsActivateBody).validate(request_body)
        Validator(str).validate(access_key)
        Validator(str).validate(content_type)
        Validator(str).validate(salt)
        Validator(str).validate(signature)
        Validator(str).validate(timestamp)
        Validator(str).is_optional().validate(idempotency)

        serialized_request = (
            Serializer(
                f"{self.base_url}/v1/issuing/cards/activate", self.get_default_headers()
            )
            .add_header("access_key", access_key)
            .add_header("Content-Type", content_type)
            .add_header("idempotency", idempotency)
            .add_header("salt", salt)
            .add_header("signature", signature)
            .add_header("timestamp", timestamp)
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)
        return InlineResponse200_9._unmap(response)

    @cast_models
    def modify_card(
        self,
        request_body: CardsPersonalizeBody,
        access_key: str,
        content_type: str,
        salt: str,
        signature: str,
        timestamp: str,
        idempotency: str = None,
    ) -> InlineResponse200_9:
        """Create a connection between an issued card and a wallet contact. Relevant to cards that are issued in bulk and not assigned to any specific person. This method can be used only once per card.

        :param request_body: The request body.
        :type request_body: CardsPersonalizeBody
        :param access_key: Unique access key provided by Rapyd for each authorized user.
        :type access_key: str
        :param content_type: Indicates that the data appears in JSON format. Set to **application/json**.
        :type content_type: str
        :param salt: Random string. Recommended length: 8-16 characters.
        :type salt: str
        :param signature: Signature calculated for each request individually. See [Request Signatures](https://docs.rapyd.net/en/request-signatures.html).
        :type signature: str
        :param timestamp: Timestamp for the request, in Unix time (seconds).
        :type timestamp: str
        :param idempotency: A unique key that prevents the platform from creating the same object twice., defaults to None
        :type idempotency: str, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: List Contacts of a Rapyd Wallet.
        :rtype: InlineResponse200_9
        """

        Validator(CardsPersonalizeBody).validate(request_body)
        Validator(str).validate(access_key)
        Validator(str).validate(content_type)
        Validator(str).validate(salt)
        Validator(str).validate(signature)
        Validator(str).validate(timestamp)
        Validator(str).is_optional().validate(idempotency)

        serialized_request = (
            Serializer(
                f"{self.base_url}/v1/issuing/cards/personalize",
                self.get_default_headers(),
            )
            .add_header("access_key", access_key)
            .add_header("Content-Type", content_type)
            .add_header("idempotency", idempotency)
            .add_header("salt", salt)
            .add_header("signature", signature)
            .add_header("timestamp", timestamp)
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)
        return InlineResponse200_9._unmap(response)

    @cast_models
    def update_card_status(
        self,
        request_body: CardsStatusBody,
        access_key: str,
        content_type: str,
        salt: str,
        signature: str,
        timestamp: str,
        idempotency: str = None,
    ) -> InlineResponse200_9:
        """Block or unblock a card that was issued via the Rapyd issuing platform.

        :param request_body: The request body.
        :type request_body: CardsStatusBody
        :param access_key: Unique access key provided by Rapyd for each authorized user.
        :type access_key: str
        :param content_type: Indicates that the data appears in JSON format. Set to **application/json**.
        :type content_type: str
        :param salt: Random string. Recommended length: 8-16 characters.
        :type salt: str
        :param signature: Signature calculated for each request individually. See [Request Signatures](https://docs.rapyd.net/en/request-signatures.html).
        :type signature: str
        :param timestamp: Timestamp for the request, in Unix time (seconds).
        :type timestamp: str
        :param idempotency: A unique key that prevents the platform from creating the same object twice., defaults to None
        :type idempotency: str, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: List Contacts for a Rapyd Wallet,
        :rtype: InlineResponse200_9
        """

        Validator(CardsStatusBody).validate(request_body)
        Validator(str).validate(access_key)
        Validator(str).validate(content_type)
        Validator(str).validate(salt)
        Validator(str).validate(signature)
        Validator(str).validate(timestamp)
        Validator(str).is_optional().validate(idempotency)

        serialized_request = (
            Serializer(
                f"{self.base_url}/v1/issuing/cards/status", self.get_default_headers()
            )
            .add_header("access_key", access_key)
            .add_header("Content-Type", content_type)
            .add_header("idempotency", idempotency)
            .add_header("salt", salt)
            .add_header("signature", signature)
            .add_header("timestamp", timestamp)
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)
        return InlineResponse200_9._unmap(response)

    @cast_models
    def get_card_issuing_transactions(
        self,
        card_id: str,
        page_size: str,
        page_number: str,
        access_key: str,
        content_type: str,
        salt: str,
        signature: str,
        timestamp: str,
        end_date: str = None,
        min_amount: str = None,
        max_amount: str = None,
        merchant_name_search: str = None,
        start_date: str = None,
        idempotency: str = None,
    ) -> InlineResponse200_10:
        """Use the GET method to retrieve a list of transactions for a specific issued card.

        :param card_id: ID of the issued card. String starting with **card_**.
        :type card_id: str
        :param page_size: ID of the transaction, as appears in the array of transactions in the response to 'Retrieve Virtual Account History'.
        :type page_size: str
        :param page_number: Page number to retrieve.
        :type page_number: str
        :param access_key: Unique access key provided by Rapyd for each authorized user.
        :type access_key: str
        :param content_type: Indicates that the data appears in JSON format. Set to **application/json**.
        :type content_type: str
        :param salt: Random string. Recommended length: 8-16 characters.
        :type salt: str
        :param signature: Signature calculated for each request individually. See [Request Signatures](https://docs.rapyd.net/en/request-signatures.html).
        :type signature: str
        :param timestamp: Timestamp for the request, in Unix time (seconds).
        :type timestamp: str
        :param end_date: Timestamp of the last transaction or later, in Unix time., defaults to None
        :type end_date: str, optional
        :param min_amount: Transactions greater than a specific amount., defaults to None
        :type min_amount: str, optional
        :param max_amount: Transactions smaller than a specific amount., defaults to None
        :type max_amount: str, optional
        :param merchant_name_search: Filters the results to return only transactions that have this string as part of the name or location., defaults to None
        :type merchant_name_search: str, optional
        :param start_date: ID of the transaction, as appears in the array of transactions in the response to 'Retrieve Virtual Account History'., defaults to None
        :type start_date: str, optional
        :param idempotency: A unique key that prevents the platform from creating the same object twice., defaults to None
        :type idempotency: str, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Retrieve a list of transactions for a specific issued card.
        :rtype: InlineResponse200_10
        """

        Validator(str).validate(card_id)
        Validator(str).validate(page_size)
        Validator(str).validate(page_number)
        Validator(str).validate(access_key)
        Validator(str).validate(content_type)
        Validator(str).validate(salt)
        Validator(str).validate(signature)
        Validator(str).validate(timestamp)
        Validator(str).is_optional().validate(end_date)
        Validator(str).is_optional().validate(min_amount)
        Validator(str).is_optional().validate(max_amount)
        Validator(str).is_optional().validate(merchant_name_search)
        Validator(str).is_optional().validate(start_date)
        Validator(str).is_optional().validate(idempotency)

        serialized_request = (
            Serializer(
                f"{self.base_url}/v1/issuing/cards/{{cardId}}/transactions",
                self.get_default_headers(),
            )
            .add_header("access_key", access_key)
            .add_header("Content-Type", content_type)
            .add_header("idempotency", idempotency)
            .add_header("salt", salt)
            .add_header("signature", signature)
            .add_header("timestamp", timestamp)
            .add_path("cardId", card_id)
            .add_query("end_date", end_date, explode=False)
            .add_query("min_amount", min_amount, explode=False)
            .add_query("max_amount", max_amount, explode=False)
            .add_query("merchant_name_search", merchant_name_search, explode=False)
            .add_query("page_size", page_size, explode=False)
            .add_query("page_number", page_number, explode=False)
            .add_query("start_date", start_date, explode=False)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)
        return InlineResponse200_10._unmap(response)

    @cast_models
    def get_card_issuing_transaction(
        self,
        card_id: str,
        transaction_id: str,
        access_key: str,
        content_type: str,
        salt: str,
        signature: str,
        timestamp: str,
        idempotency: str = None,
    ) -> InlineResponse200_11:
        """Use the GET method to retrieve details of a specific transaction from a specific issued card.

        :param card_id: Card id
        :type card_id: str
        :param transaction_id: Card transaction id
        :type transaction_id: str
        :param access_key: Unique access key provided by Rapyd for each authorized user.
        :type access_key: str
        :param content_type: Indicates that the data appears in JSON format. Set to **application/json**.
        :type content_type: str
        :param salt: Random string. Recommended length: 8-16 characters.
        :type salt: str
        :param signature: Signature calculated for each request individually. See [Request Signatures](https://docs.rapyd.net/en/request-signatures.html).
        :type signature: str
        :param timestamp: Timestamp for the request, in Unix time (seconds).
        :type timestamp: str
        :param idempotency: A unique key that prevents the platform from creating the same object twice., defaults to None
        :type idempotency: str, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: List Contacts for a Rapyd Wallet.
        :rtype: InlineResponse200_11
        """

        Validator(str).validate(card_id)
        Validator(str).validate(transaction_id)
        Validator(str).validate(access_key)
        Validator(str).validate(content_type)
        Validator(str).validate(salt)
        Validator(str).validate(signature)
        Validator(str).validate(timestamp)
        Validator(str).is_optional().validate(idempotency)

        serialized_request = (
            Serializer(
                f"{self.base_url}/v1/issuing/cards/{{cardId}}/transactions/{{transactionId}}",
                self.get_default_headers(),
            )
            .add_header("access_key", access_key)
            .add_header("Content-Type", content_type)
            .add_header("idempotency", idempotency)
            .add_header("salt", salt)
            .add_header("signature", signature)
            .add_header("timestamp", timestamp)
            .add_path("cardId", card_id)
            .add_path("transactionId", transaction_id)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)
        return InlineResponse200_11._unmap(response)

    @cast_models
    def create_issuing(
        self,
        request_body: IssuingBankaccountsBody,
        access_key: str,
        content_type: str,
        salt: str,
        signature: str,
        timestamp: str,
        idempotency: str = None,
    ) -> InlineResponse200_43:
        """Issue a virtual account number to an existing wallet.

        :param request_body: The request body.
        :type request_body: IssuingBankaccountsBody
        :param access_key: Unique access key provided by Rapyd for each authorized user.
        :type access_key: str
        :param content_type: Indicates that the data appears in JSON format. Set to **application/json**.
        :type content_type: str
        :param salt: Random string. Recommended length: 8-16 characters.
        :type salt: str
        :param signature: Signature calculated for each request individually. See [Request Signatures](https://docs.rapyd.net/en/request-signatures.html).
        :type signature: str
        :param timestamp: Timestamp for the request, in Unix time (seconds).
        :type timestamp: str
        :param idempotency: A unique key that prevents the platform from creating the same object twice., defaults to None
        :type idempotency: str, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Virtual Account,
        :rtype: InlineResponse200_43
        """

        Validator(IssuingBankaccountsBody).validate(request_body)
        Validator(str).validate(access_key)
        Validator(str).validate(content_type)
        Validator(str).validate(salt)
        Validator(str).validate(signature)
        Validator(str).validate(timestamp)
        Validator(str).is_optional().validate(idempotency)

        serialized_request = (
            Serializer(
                f"{self.base_url}/v1/issuing/bankaccounts", self.get_default_headers()
            )
            .add_header("access_key", access_key)
            .add_header("Content-Type", content_type)
            .add_header("idempotency", idempotency)
            .add_header("salt", salt)
            .add_header("signature", signature)
            .add_header("timestamp", timestamp)
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)
        return InlineResponse200_43._unmap(response)

    @cast_models
    def simulate_complete_bank_account_issuing_transaction(
        self,
        request_body: BankaccountsBankaccounttransfertobankaccountBody,
        access_key: str,
        content_type: str,
        salt: str,
        signature: str,
        timestamp: str,
        idempotency: str = None,
    ) -> InlineResponse200_44:
        """Imulate a deposit to a virtual account number that was issued to a wallet. This method is relevant only for testing in the sandbox. The currency of the transfer must be supported by the specific virtual account. This method triggers the Deposit Completed webhook.

        :param request_body: The request body.
        :type request_body: BankaccountsBankaccounttransfertobankaccountBody
        :param access_key: Unique access key provided by Rapyd for each authorized user.
        :type access_key: str
        :param content_type: Indicates that the data appears in JSON format. Set to **application/json**.
        :type content_type: str
        :param salt: Random string. Recommended length: 8-16 characters.
        :type salt: str
        :param signature: Signature calculated for each request individually. See [Request Signatures](https://docs.rapyd.net/en/request-signatures.html).
        :type signature: str
        :param timestamp: Timestamp for the request, in Unix time (seconds).
        :type timestamp: str
        :param idempotency: A unique key that prevents the platform from creating the same object twice., defaults to None
        :type idempotency: str, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: List Contacts for a Rapyd Wallet,
        :rtype: InlineResponse200_44
        """

        Validator(BankaccountsBankaccounttransfertobankaccountBody).validate(
            request_body
        )
        Validator(str).validate(access_key)
        Validator(str).validate(content_type)
        Validator(str).validate(salt)
        Validator(str).validate(signature)
        Validator(str).validate(timestamp)
        Validator(str).is_optional().validate(idempotency)

        serialized_request = (
            Serializer(
                f"{self.base_url}/v1/issuing/bankaccounts/bankaccounttransfertobankaccount",
                self.get_default_headers(),
            )
            .add_header("access_key", access_key)
            .add_header("Content-Type", content_type)
            .add_header("idempotency", idempotency)
            .add_header("salt", salt)
            .add_header("signature", signature)
            .add_header("timestamp", timestamp)
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)
        return InlineResponse200_44._unmap(response)

    @cast_models
    def get_remitter_details(
        self,
        virtual_account_id: str,
        transaction_id: str,
        access_key: str,
        content_type: str,
        salt: str,
        signature: str,
        timestamp: str,
        idempotency: str = None,
    ) -> InlineResponse200_45:
        """Retrieve the details of the remitter of a transfer to a virtual bank account.

        :param virtual_account_id: ID of the Virtual Account Number object. String starting with **issuing_**.
        :type virtual_account_id: str
        :param transaction_id: ID of the transaction, as appears in the array of transactions in the response to 'Retrieve Virtual Account History'.
        :type transaction_id: str
        :param access_key: Unique access key provided by Rapyd for each authorized user.
        :type access_key: str
        :param content_type: Indicates that the data appears in JSON format. Set to **application/json**.
        :type content_type: str
        :param salt: Random string. Recommended length: 8-16 characters.
        :type salt: str
        :param signature: Signature calculated for each request individually. See [Request Signatures](https://docs.rapyd.net/en/request-signatures.html).
        :type signature: str
        :param timestamp: Timestamp for the request, in Unix time (seconds).
        :type timestamp: str
        :param idempotency: A unique key that prevents the platform from creating the same object twice., defaults to None
        :type idempotency: str, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: List Contacts for a Rapyd Wallet,
        :rtype: InlineResponse200_45
        """

        Validator(str).validate(virtual_account_id)
        Validator(str).validate(transaction_id)
        Validator(str).validate(access_key)
        Validator(str).validate(content_type)
        Validator(str).validate(salt)
        Validator(str).validate(signature)
        Validator(str).validate(timestamp)
        Validator(str).is_optional().validate(idempotency)

        serialized_request = (
            Serializer(
                f"{self.base_url}/v1/issuing/bankaccounts/remitters/{{virtualAccountId}}/transactions/{{transaction_id}}",
                self.get_default_headers(),
            )
            .add_header("access_key", access_key)
            .add_header("Content-Type", content_type)
            .add_header("idempotency", idempotency)
            .add_header("salt", salt)
            .add_header("signature", signature)
            .add_header("timestamp", timestamp)
            .add_path("virtualAccountId", virtual_account_id)
            .add_path("transaction_id", transaction_id)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)
        return InlineResponse200_45._unmap(response)

    @cast_models
    def retrieve_issuing_by_rapyd_token(
        self,
        virtual_account_id: str,
        access_key: str,
        content_type: str,
        salt: str,
        signature: str,
        timestamp: str,
        idempotency: str = None,
    ) -> InlineResponse200_44:
        """Retrieve a Virtual Account Number object for a wallet.

        :param virtual_account_id: ID of the Virtual Account Number object. String starting with **issuing_**.
        :type virtual_account_id: str
        :param access_key: Unique access key provided by Rapyd for each authorized user.
        :type access_key: str
        :param content_type: Indicates that the data appears in JSON format. Set to **application/json**.
        :type content_type: str
        :param salt: Random string. Recommended length: 8-16 characters.
        :type salt: str
        :param signature: Signature calculated for each request individually. See [Request Signatures](https://docs.rapyd.net/en/request-signatures.html).
        :type signature: str
        :param timestamp: Timestamp for the request, in Unix time (seconds).
        :type timestamp: str
        :param idempotency: A unique key that prevents the platform from creating the same object twice., defaults to None
        :type idempotency: str, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Virtual Account,
        :rtype: InlineResponse200_44
        """

        Validator(str).validate(virtual_account_id)
        Validator(str).validate(access_key)
        Validator(str).validate(content_type)
        Validator(str).validate(salt)
        Validator(str).validate(signature)
        Validator(str).validate(timestamp)
        Validator(str).is_optional().validate(idempotency)

        serialized_request = (
            Serializer(
                f"{self.base_url}/v1/issuing/bankaccounts/{{virtualAccountId}}",
                self.get_default_headers(),
            )
            .add_header("access_key", access_key)
            .add_header("Content-Type", content_type)
            .add_header("idempotency", idempotency)
            .add_header("salt", salt)
            .add_header("signature", signature)
            .add_header("timestamp", timestamp)
            .add_path("virtualAccountId", virtual_account_id)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)
        return InlineResponse200_44._unmap(response)

    @cast_models
    def update_receiving_currency(
        self,
        virtual_account_id: str,
        access_key: str,
        content_type: str,
        salt: str,
        signature: str,
        timestamp: str,
        request_body: BankaccountsVirtualAccountIdBody = None,
        idempotency: str = None,
    ) -> InlineResponse200_46:
        """Update Receiving Currency

        :param request_body: The request body., defaults to None
        :type request_body: BankaccountsVirtualAccountIdBody, optional
        :param virtual_account_id: ID of the Virtual Account Number object. String starting with **issuing_**.
        :type virtual_account_id: str
        :param access_key: Unique access key provided by Rapyd for each authorized user.
        :type access_key: str
        :param content_type: Indicates that the data appears in JSON format. Set to **application/json**.
        :type content_type: str
        :param salt: Random string. Recommended length: 8-16 characters.
        :type salt: str
        :param signature: Signature calculated for each request individually. See [Request Signatures](https://docs.rapyd.net/en/request-signatures.html).
        :type signature: str
        :param timestamp: Timestamp for the request, in Unix time (seconds).
        :type timestamp: str
        :param idempotency: A unique key that prevents the platform from creating the same object twice., defaults to None
        :type idempotency: str, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: List Contacts of Wallet
        :rtype: InlineResponse200_46
        """

        Validator(BankaccountsVirtualAccountIdBody).is_optional().validate(request_body)
        Validator(str).validate(virtual_account_id)
        Validator(str).validate(access_key)
        Validator(str).validate(content_type)
        Validator(str).validate(salt)
        Validator(str).validate(signature)
        Validator(str).validate(timestamp)
        Validator(str).is_optional().validate(idempotency)

        serialized_request = (
            Serializer(
                f"{self.base_url}/v1/issuing/bankaccounts/{{virtualAccountId}}",
                self.get_default_headers(),
            )
            .add_header("access_key", access_key)
            .add_header("Content-Type", content_type)
            .add_header("idempotency", idempotency)
            .add_header("salt", salt)
            .add_header("signature", signature)
            .add_header("timestamp", timestamp)
            .add_path("virtualAccountId", virtual_account_id)
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)
        return InlineResponse200_46._unmap(response)

    @cast_models
    def retrieve_issuing_transaction(
        self,
        virtual_account_id: str,
        transaction_id: str,
        access_key: str,
        content_type: str,
        salt: str,
        signature: str,
        timestamp: str,
        idempotency: str = None,
    ) -> InlineResponse200_47:
        """Retrieve a virtual account transaction.

        :param virtual_account_id: ID of the Virtual Account Number object. String starting with **issuing_**.
        :type virtual_account_id: str
        :param transaction_id: ID of the transaction, as appears in the array of transactions in the response to 'Retrieve Virtual Account History'.
        :type transaction_id: str
        :param access_key: Unique access key provided by Rapyd for each authorized user.
        :type access_key: str
        :param content_type: Indicates that the data appears in JSON format. Set to **application/json**.
        :type content_type: str
        :param salt: Random string. Recommended length: 8-16 characters.
        :type salt: str
        :param signature: Signature calculated for each request individually. See [Request Signatures](https://docs.rapyd.net/en/request-signatures.html).
        :type signature: str
        :param timestamp: Timestamp for the request, in Unix time (seconds).
        :type timestamp: str
        :param idempotency: A unique key that prevents the platform from creating the same object twice., defaults to None
        :type idempotency: str, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: List Contacts for a Rapyd Wallet,
        :rtype: InlineResponse200_47
        """

        Validator(str).validate(virtual_account_id)
        Validator(str).validate(transaction_id)
        Validator(str).validate(access_key)
        Validator(str).validate(content_type)
        Validator(str).validate(salt)
        Validator(str).validate(signature)
        Validator(str).validate(timestamp)
        Validator(str).is_optional().validate(idempotency)

        serialized_request = (
            Serializer(
                f"{self.base_url}/v1/issuing/bankaccounts/{{virtualAccountId}}/transactions/{{transactionId}}",
                self.get_default_headers(),
            )
            .add_header("access_key", access_key)
            .add_header("Content-Type", content_type)
            .add_header("idempotency", idempotency)
            .add_header("salt", salt)
            .add_header("signature", signature)
            .add_header("timestamp", timestamp)
            .add_path("virtualAccountId", virtual_account_id)
            .add_path("transactionId", transaction_id)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)
        return InlineResponse200_47._unmap(response)
