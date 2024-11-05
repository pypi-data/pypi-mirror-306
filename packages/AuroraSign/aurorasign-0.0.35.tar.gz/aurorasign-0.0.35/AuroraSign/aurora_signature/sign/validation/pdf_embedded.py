from typing import Optional
from collections import namedtuple

from ...pdf_utils import generic
from ...pdf_utils.reader import PdfFileReader
from ...sign.fields import (
    MDPPerm,
)

from .errors import (
    SignatureValidationError,
)

__all__ = [
    'DocMDPInfo',
    'read_certification_data',
]


DocMDPInfo = namedtuple('DocMDPInfo', ['permission', 'author_sig'])

def _extract_reference_dict(
    signature_obj, method
) -> Optional[generic.DictionaryObject]:
    try:
        sig_refs = signature_obj['/Reference']
    except KeyError:
        return None
    for ref in sig_refs:
        ref = ref.get_object()
        if ref['/TransformMethod'] == method:
            return ref
    return None

def _extract_docmdp_for_sig(signature_obj) -> Optional[MDPPerm]:
    ref = _extract_reference_dict(signature_obj, '/DocMDP')
    if ref is None:
        return None
    try:
        raw_perms = ref['/TransformParams'].raw_get('/P')
        return MDPPerm(raw_perms)
    except (ValueError, KeyError) as e:  # pragma: nocover
        raise SignatureValidationError(
            "Failed to read document permissions"
        ) from e

def read_certification_data(reader: PdfFileReader) -> Optional[DocMDPInfo]:
    """
    Read the certification information for a PDF document, if present.

    :param reader:
        Reader representing the input document.
    :return:
        A :class:`.DocMDPInfo` object containing the relevant data, or ``None``.
    """
    try:
        certification_sig = reader.root['/Perms']['/DocMDP']
    except KeyError:
        return None

    perm = _extract_docmdp_for_sig(certification_sig)
    return DocMDPInfo(perm, certification_sig)
