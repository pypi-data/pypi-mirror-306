"""
Invoice resource, it includes the class Resource, a request
class to create the resource and a class to represent an
Invoice Item.

"""

import datetime as dt
from typing import ClassVar, Dict, List, Optional, Union, cast

from pydantic import BaseModel, validator, ValidationError
from pydantic.dataclasses import dataclass

from facturapi.types.enums import InvoiceType

from ..types import InvoiceRelation, InvoiceUse, PaymentForm, PaymentMethod
from ..types.general import (
    CustomerAddress,
    CustomerBasicInfo,
    ItemPart,
    Namespace,
    ProductBasicInfo,
    InvoiceDocuments,
    InvoiceStamp
)
from .base import Creatable, Deletable, Downloadable, Queryable, Retrievable
from .customers import Customer, CustomerRequest
from .resources import retrieve_property


class InvoiceItem(BaseModel):
    """
    Class representing an Item from an Invoice.

    Attributes:
        quantity (str): Number of items of this type. Defaults
            to `1`.
        discount (float): Discount on the item price if any.
            Defaults to `0`.
        product (Union[str, ProductBasicInfo, Dict]): Product
            ID, info or request to create a resource.
        custom_keys (List[str]): List of custom product keys.
            Optional.
        complement (str): XML code with additional info to add
            to the invoice. Optional.
        parts (List[ItemParts]): If the concept includes parts.
            Optional.
        property_tax_account (str): 'Predial' number. Optional.

    """

    quantity: Optional[int] = 1
    discount: Optional[float] = 0
    product: Union[
        str, ProductBasicInfo, Dict
    ]  # TO DO: Change Dict for ProductRequest
    custom_keys: Optional[List[str]]
    complement: Optional[str]
    parts: Optional[List[ItemPart]]
    property_tax_account: Optional[str]

class RelatedDocument(BaseModel):
    """
    Represents a related document for payment type invoices.
    """
    uuid: str
    amount: float
    installment: Optional[int]
    last_balance: float
    taxes: Optional[List[Dict]]


class PaymentData(BaseModel):
    """
    Represents the payment information for a complement.
    """
    payment_form: PaymentForm
    currency: str
    exchange: float
    related_documents: List[RelatedDocument]
    date: Optional[str]

class PaymentComplement(BaseModel):
    """
    Represents the complement for payments.
    """
    type: str = "pago"  # Type is fixed to "pago" for this complement.
    data: List[PaymentData]

class GlobalData(BaseModel):
    """
    Data for global invoices.
    
    Attributes:
        periodicity (str): Periodicity of the invoice. Can be 'day', 'week', 'fortnight', 'month', 'two_months'.
        months (str): Months of the invoice. More info: https://docs.facturapi.io/api/#tag/sat_keys (Meses y Bimestres)
        year (int): Year of the invoice.
    """
    
    periodicity: str
    months: str
    year: int


class InvoiceRequest(BaseModel):
    """
    This request must be filled to `create` an Invoice.
    It contains all information necessary to create this resource.

    Attributes:
        type (str): Type of invoice (e.g., 'I' for Ingreso, 'P' for Pago).
        customer (Union[str, CustomerRequest]): Customer ID or a
            CustomerRequest to create a new one.
        items (List[InvoiceItem]): List of items of the invoice (Optional for payment invoices).
        payment_form (PaymentForm): Form of payment (Optional for payment invoices).
        payment_method (PaymentMethod): Method of payment. Defaults to `PaymentMethod.contado`.
        use (InvoiceUse): Invoice SAT CFDI use. Defaults to `InvoiceUse.adquisicion_mercancias`.
        currency (str): Currency of the invoice in ISO format. Defaults to `MXN`.
        exchange (float): Exchange value to Mexican Pesos. Defaults to `1.0`.
        conditions (str): Payment conditions. Optional.
        complements (List[PaymentComplement]): List of payment complements (Required for payment invoices).
    """

    type: Optional[str] = InvoiceType.ingreso
    items: Optional[List[InvoiceItem]]  # Items are optional for payment invoices
    payment_form: Optional[PaymentForm] # Optional for payment type invoices
    payment_method: Optional[PaymentMethod] = PaymentMethod.contado
    use: Optional[InvoiceUse] = InvoiceUse.adquisicion_mercancias
    currency: Optional[str] = 'MXN'
    exchange: Optional[float] = 1.0
    conditions: Optional[str]
    
    customer: Union[str, CustomerRequest]
    folio_number: Optional[int]
    series: Optional[str]
    foreign_trade: Optional[Dict]
    related: Optional[List[str]]
    relation: Optional[InvoiceRelation]
    related_documents: Optional[List[InvoiceDocuments]]

    pdf_custom_section: Optional[str]
    addenda: Optional[str]
    namespaces: Optional[Namespace]
    global_data: Optional[GlobalData]
    complements: Optional[List[PaymentComplement]]  # Required for payment invoices

    # Validador para verificar los campos según el tipo de factura
    # Validación para facturas de ingreso
    @validator('payment_form', 'payment_method', 'use', 'date', pre=True, always=True, check_fields=False)
    def validate_ingreso_fields(cls, v, values, field):
        if values.get('type') == 'I' and v is None:
            raise ValueError(f'{field.name} is required for Ingreso invoices')
        return v

    # Validación para facturas de egreso
    @validator('related_documents', pre=True, always=True, check_fields=False)
    def validate_egreso_fields(cls, v, values):
        if values.get('type') == 'E' and not v:
            raise ValueError('related_documents is required for Egreso invoices')
        return v

    # Validación para facturas de pago
    @validator('complements', pre=True, always=True, check_fields=False)
    def validate_pago_complement(cls, v, values):
        if values.get('type') == 'P' and not v:
            raise ValueError('complements are required for Pago invoices')
        return v

    # Validador para productos según el tipo de factura
    @validator('items', each_item=True)
    def validate_product_items(cls, item, values):
        invoice_type = values.get('type')
        product = item.product

        if invoice_type == 'I':  # Factura de ingreso
            required_fields = ['product_key', 'tax_included', 'taxability', 'unit_key']
            missing_fields = [field for field in required_fields if getattr(product, field) is None]
            if missing_fields:
                raise ValueError(f'Missing required fields for Ingreso: {missing_fields}')
        elif invoice_type == 'E':  # Factura de egreso
            extra_fields = ['product_key', 'tax_included', 'taxability', 'unit_key']
            if any(getattr(product, field) is not None for field in extra_fields):
                raise ValueError('Extra fields are not allowed for Egreso invoices.')

        return item

@dataclass
class Invoice(Creatable, Deletable, Downloadable, Queryable, Retrievable):
    """Invoice resource

    Resource for an Invoice. It inherits from `Creatable`, `Deletable`,
    `Downloadable`, `Queryable` and `Retrievable`.

    Attributes:
        created_at (datetime.datetime): The datetime in which the
            resource was created.
        livemode (bool): If the resource was created in test or live
            mode.
        status (str): Status of the invoice.
        customer_info (CustomerBasicInfo): Basic info of the Customer.
        customer_uri (str): URI representing how to fetch a Customer
            resource related to the Invoice.
        total (float): Invoice total.
        uuid (str): 'Folio fiscal' assigned by SAT.
        payment_form (PaymentForm): Form of payment of the Invoice.
        items (List[InvoiceItem]): List of items of the Invoice.
        currency (str): Currency of the invoice in ISO format.
        exchange (float): Exchange value to Mexican Pesos.
        cancellation_status (str): If the Invoice was cancelled, the
            status of the cancellation. Optional.
        folio_number (int): Folio number. Optional.
        series (str): Custom series string. Optional. Defaults to `None`.
        related (List[str]): UUID of related invoices. Defaults to
            `None`.
        relation (InvoiceRelation): Relation key from the SAT catalogue.
            Defaults to `None`.

    """

    _resource: ClassVar = 'invoices'
    _relations: ClassVar = ['customer']

    created_at: dt.datetime
    livemode: bool
    status: str
    cancellation_status: Optional[str]
    verification_url: str
    address : CustomerAddress
    type : str
    customer_info: CustomerBasicInfo
    customer_uri : str
    total: float
    uuid: str
    folio_number: Optional[int]
    payment_form: Optional[PaymentForm]
    items: List[InvoiceItem]

    currency: str
    exchange: float
    stamp : Optional[InvoiceStamp]

    @classmethod
    def create(cls, data: InvoiceRequest) -> 'Invoice':
        """Create an invoice.

        Args:
            data: All the request data to create an invoice.

        Returns:
            Invoice: The created resource.
        """
        cleaned_data = data.dict(exclude_unset=True, exclude_none=True)

        if cleaned_data.get('type') == InvoiceType.ingreso:
            # Change 'global_data' key to 'global' due global is a reserved word in Python
            if 'global_data' in cleaned_data:
                cleaned_data['global'] = cleaned_data.pop('global_data')
            
            print(cleaned_data)

            return cast('Invoice', cls._create(**cleaned_data))
        elif cleaned_data.get('type') == InvoiceType.pago:
            return cast('Invoice', cls._createPayment(**cleaned_data))
        elif cleaned_data.get('type') == InvoiceType.egreso:
            return cast('Invoice', cls._createPayment(**cleaned_data))

    @classmethod
    def cancel(cls, invoice_id: str, motive: str, substitute_uuid: Optional[str] = None) -> 'Invoice':
        """Cancel an invoice by providing the ID and a motive.

        Args:
            invoice_id: The ID of the invoice to cancel.
            motive: The reason for the cancellation.
            substitute_uuid: Optional. UUID of a substitute invoice, if applicable.

        Returns:
            Invoice: The cancelled invoice resource.
        """
        query_params = {"motive": motive}
        if substitute_uuid:
            query_params["substitute_uuid"] = substitute_uuid

        # Delegar al método _delete para realizar la solicitud
        return cls._delete(invoice_id, **query_params)

    @property
    def customer(self) -> Customer:
        """Fetch and access Customer resource.

        This property fetches and maps the customer
        related to an invoice so it can be accessed
        through a simple property instead of making a
        manual retrieve.

        Returns:
            Customer: Customer related to the invoice.

        """
        return cast(Customer, retrieve_property(self.customer_uri))
